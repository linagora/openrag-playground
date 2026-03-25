# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Chat routes — partition discovery, SSE streaming, sources."""

import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import httpx
from flask import (
    Blueprint, render_template, request, session, Response, current_app,
    stream_with_context, jsonify,
)

from app.yaml_store import load_config as load_yaml_config

from app.i18n import t

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


def _get_credentials():
    """Get token and API URL from session."""
    return session.get("user_token"), session.get("user_api_url", "").rstrip("/")


def _fetch_partitions(token, api_url):
    """Fetch partitions from GET /v1/models, with roles from GET /partition/{name}."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = httpx.get(f"{api_url}/v1/models", headers=headers, timeout=10.0)
        if resp.status_code != 200:
            return []
        data = resp.json()
        models = data.get("data", [])
        partitions = []
        for m in models:
            mid = m.get("id", "")
            if mid.startswith("openrag-"):
                partitions.append({"id": mid, "role": None})
        # Sort: openrag-all first, then alphabetical
        partitions.sort(key=lambda x: ("0" if x["id"] == "openrag-all" else "1") + x["id"])
        # Fetch roles from GET /partition/ (list all with roles)
        try:
            r = httpx.get(f"{api_url}/partition/", headers=headers, timeout=5.0)
            if r.status_code == 200:
                body = r.json()
                # Build role map from response
                role_map = {}
                items = body if isinstance(body, list) else body.get("partitions", [])
                for item in items:
                    pname = item.get("partition", item.get("name", ""))
                    role = item.get("role", "")
                    if pname and role:
                        role_map[pname] = role
                for p in partitions:
                    name = p["id"].replace("openrag-", "")
                    p["role"] = role_map.get(name)
        except Exception:
            pass
        return partitions
    except Exception:
        return []


def _common_prefix(partitions):
    """Find common prefix among non-all partitions. Only strip if it ends with - _ or /."""
    children = [p["id"].replace("openrag-", "") for p in partitions if p["id"] != "openrag-all"]
    if len(children) < 2:
        return ""
    import os
    prefix = os.path.commonprefix(children)
    if prefix and prefix[-1] in "-_/":
        return prefix
    # Trim to last separator
    for sep in "-_/":
        idx = prefix.rfind(sep)
        if idx >= 0:
            return prefix[: idx + 1]
    return ""


@chat_bp.route("/partitions")
def partitions():
    """Return partition tree as HTML fragment."""
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    parts = _fetch_partitions(token, api_url)
    active = session.get("active_partition", parts[0]["id"] if parts else "openrag-all")
    prefix = _common_prefix(parts)
    session["partition_prefix"] = prefix
    # OOB swap to update header label on initial load too
    display = active.replace("openrag-", "")
    if prefix and active != "openrag-all":
        display = display[len(prefix):]
    active_role = ""
    for p in parts:
        if p["id"] == active:
            active_role = p.get("role") or ""
            break
    oob = f'<span id="partition-label" hx-swap-oob="true" class="text-base font-semibold" data-role="{active_role}">{display}</span>'
    return render_template("app/partitions.html", partitions=parts, active=active, strip_prefix=prefix) + oob


def _role_badge(is_admin):
    if is_admin:
        return '<span class="inline-block mt-0.5 rounded-full px-1.5 py-px text-[10px] font-semibold" style="background:rgba(199,31,69,0.15);color:var(--accent);">admin</span>'
    return '<span class="inline-block mt-0.5 rounded-full px-1.5 py-px text-[10px] font-semibold" style="background:rgba(34,211,164,0.15);color:var(--success);">user</span>'


def _check_role(api_url, token):
    """Call GET /users/info and return is_admin bool or None on failure."""
    try:
        resp = httpx.get(
            f"{api_url}/users/info",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
        if resp.status_code == 200:
            return resp.json().get("is_admin", False)
    except Exception:
        pass
    return None


def _file_icon(filename):
    """Return a Lucide icon name based on file extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ("mp3", "wav", "ogg", "flac", "m4a", "aac"):
        return "audio-lines"
    if ext in ("mp4", "webm", "mov", "avi", "mkv"):
        return "file-play"
    if ext in ("jpg", "jpeg", "png", "gif", "webp", "svg", "bmp"):
        return "image"
    if ext in ("eml", "msg"):
        return "mail"
    return "file-text"


def _file_media_type(filename):
    """Return 'audio', 'video', 'image', 'pdf', or 'text' for display."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ("mp3", "wav", "ogg", "flac", "m4a", "aac"):
        return "audio"
    if ext in ("mp4", "webm", "mov", "avi", "mkv"):
        return "video"
    if ext in ("jpg", "jpeg", "png", "gif", "webp", "svg", "bmp"):
        return "image"
    if ext == "pdf":
        return "pdf"
    return "text"


@chat_bp.route("/partition-stats")
def partition_stats():
    """Return doc + chunk counts, type pie chart, and growth sparkline."""

    token, api_url = _get_credentials()
    if not token:
        return "", 401
    partition = session.get("active_partition", "openrag-all").replace("openrag-", "")
    headers = {"Authorization": f"Bearer {token}"}

    def _fetch_files():
        try:
            r = httpx.get(f"{api_url}/partition/{partition}", headers=headers, timeout=10.0)
            return r.json().get("files", []) if r.status_code == 200 else []
        except Exception:
            return []

    def _count_chunks():
        try:
            r = httpx.get(
                f"{api_url}/partition/{partition}/chunks",
                params={"include_embedding": "false"},
                headers=headers, timeout=15.0,
            )
            if r.status_code != 200:
                return 0
            data = r.json()
            items = data if isinstance(data, list) else data.get("chunks", data.get("documents", []))
            return len(items)
        except Exception:
            return 0

    with ThreadPoolExecutor(max_workers=2) as pool:
        f_files = pool.submit(_fetch_files)
        f_chunks = pool.submit(_count_chunks)
        files = f_files.result()
        chunk_count = f_chunks.result()

    file_count = len(files)
    if file_count == 0 and chunk_count == 0:
        return '<span id="partition-stats" class="text-[11px]" style="color:var(--text-subtle);">—</span>'

    sep = ' <span class="opacity-40">·</span> '
    counts = []
    charts = []

    # Doc + chunk counts
    if file_count:
        label = t("stats.files") if file_count != 1 else t("stats.file")
        counts.append(f'<i data-lucide="file" class="w-2.5 h-2.5 inline" style="vertical-align:-1px;"></i> {file_count} {label}')
    if chunk_count:
        label = t("stats.chunks") if chunk_count != 1 else t("stats.chunk")
        counts.append(f'<i data-lucide="puzzle" class="w-2.5 h-2.5 inline" style="vertical-align:-1px;"></i> {chunk_count} {label}')

    # Pie chart per doc type
    type_counter = Counter()
    for f in files:
        fname = f.get("original_filename", f.get("filename", f.get("file_id", "")))
        ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else "other"
        type_counter[ext] += 1
    if type_counter:
        for ext, count in type_counter.most_common(6):
            pct = min(100, int(count / file_count * 100))
            charts.append(
                f'<span title="{ext}: {count}" style="white-space:nowrap;">'
                f'<span class="chart text-xl" style="vertical-align:-3px;">{{p:{pct}}}</span>'
                f'&nbsp;<span class="text-[9px]" style="color:var(--text-subtle);">{ext}</span>'
                f'</span>'
            )

    # Growth sparkline
    now = datetime.utcnow()
    day_counts = [0] * 10
    for f in files:
        created = f.get("created_at", "")
        if not created:
            continue
        try:
            dt = datetime.fromisoformat(created.replace("Z", "").split("+")[0])
            delta = (now - dt).days
            if 0 <= delta < 10:
                day_counts[9 - delta] += 1
        except Exception:
            pass
    for i in range(1, len(day_counts)):
        day_counts[i] += day_counts[i - 1]
    gmax = max(day_counts) if day_counts else 1
    growth_values = [min(100, int(v / gmax * 100)) if gmax else 0 for v in day_counts]
    if any(v > 0 for v in growth_values):
        charts.append(f'<span class="chart text-xl" style="vertical-align:-3px;">{{l:{",".join(str(v) for v in growth_values)}}}</span>')

    text = sep.join(counts)
    if charts:
        text += sep + sep.join(charts)
    return f'<span id="partition-stats" class="text-[11px]" style="color:var(--text-muted);">{text}</span>'


@chat_bp.route("/partition-files/<partition>")
def partition_files(partition):
    """Return last 10 files for a partition as HTML fragment."""
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    try:
        resp = httpx.get(
            f"{api_url}/partition/{partition}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            files = data.get("files", [])
            files = sorted(files, key=lambda f: f.get("created_at", ""), reverse=True)[:10]
            for f in files:
                fname = f.get("original_filename", f.get("filename", f.get("file_id", "")))
                f["icon"] = _file_icon(fname)
                f["media_type"] = _file_media_type(fname)
            return render_template("app/files.html", files=files, partition=partition)
    except Exception:
        pass
    return '<div class="text-xs px-6 py-1" style="color:var(--text-subtle);">—</div>'


@chat_bp.route("/file-chunks/<partition>/<path:file_id>")
def file_chunks(partition, file_id):
    """Return first 10 chunks for a file as HTML fragment."""
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # Step 1: get document links
        resp = httpx.get(
            f"{api_url}/partition/{partition}/file/{file_id}",
            headers=headers, timeout=10.0,
        )
        if resp.status_code != 200:
            return '<div class="text-xs px-8 py-1" style="color:var(--text-subtle);">—</div>'
        data = resp.json()
        docs = data.get("documents", [])[:10]
        # Step 2: fetch each chunk's page_content from its extract link
        chunks = []
        for doc in docs:
            link = doc.get("link", "")
            if not link:
                continue
            # Normalize: match the API URL scheme (http→https if needed)
            if api_url.startswith("https://") and link.startswith("http://"):
                link = "https://" + link[7:]
            try:
                r = httpx.get(link, headers=headers, timeout=10.0)
                if r.status_code == 200:
                    extract = r.json()
                    text = extract.get("page_content", "")
                    # Strip [CONTEXT] prefix
                    if text.startswith("[CONTEXT] "):
                        text = text[10:]
                    elif text.startswith("[CONTEXT]"):
                        text = text[9:]
                    chunks.append({
                        "text": text,
                        "page": extract.get("metadata", {}).get("page"),
                    })
            except Exception:
                pass
        return render_template("app/chunks.html", chunks=chunks, partition=partition, file_id=file_id)
    except Exception:
        pass
    return '<div class="text-xs px-8 py-1" style="color:var(--text-subtle);">—</div>'


@chat_bp.route("/delete-file/<partition>/<path:file_id>", methods=["DELETE"])
def delete_file(partition, file_id):
    """Delete a file from a partition via the indexer API."""
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    try:
        resp = httpx.delete(
            f"{api_url}/indexer/partition/{partition}/file/{file_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        if resp.status_code in (200, 204):
            return "", 204
        return "", resp.status_code
    except Exception:
        return "", 500


@chat_bp.route("/file-proxy/<partition>/<path:file_id>")
def file_proxy(partition, file_id):
    """Proxy a file from the OpenRAG server via /static/ endpoint."""
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    # Build static URL from source field: replace /app/data/ with /static/
    source = request.args.get("source", "")
    if source:
        static_path = source.replace("/app/data/", "/static/", 1)
    else:
        static_path = f"/static/{file_id}"
    try:
        resp = httpx.get(
            f"{api_url}{static_path}",
            params={"token": token},
            timeout=30.0,
            follow_redirects=True,
        )
        if resp.status_code == 200 and len(resp.content) > 0:
            from flask import make_response
            r = make_response(resp.content)
            ct = resp.headers.get("content-type", "application/octet-stream")
            r.headers["Content-Type"] = ct
            r.headers["Content-Disposition"] = f'inline; filename="{file_id}"'
            return r
    except Exception:
        pass
    return "", 404


def _resolve_openrag_uid(user_cfg, password):
    """Decrypt a demo user's token and call /users/info to get their OpenRAG user_id."""
    from app.crypto import decrypt_token as do_decrypt
    try:
        tok = do_decrypt(user_cfg["token"], password, user_cfg["id"])
        api = user_cfg.get("api_url", "").rstrip("/")
        resp = httpx.get(f"{api}/users/info",
                         headers={"Authorization": f"Bearer {tok}"}, timeout=5.0)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("user_id", data.get("id", ""))
    except Exception:
        pass
    return ""


@chat_bp.route("/partition-access/<partition>")
def partition_access(partition):
    """Get all group members with their access level for this partition."""
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    password = current_app.config.get("ADMIN_PASSWORD")
    # Fetch current partition users
    role_map = {}
    try:
        resp = httpx.get(
            f"{api_url}/partition/{partition}/users",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            items = data if isinstance(data, list) else data.get("members", data.get("users", []))
            for u in items:
                uid = u.get("user_id", u.get("id", ""))
                if uid:
                    role_map[uid] = u.get("role", "viewer")
    except Exception:
        pass
    # Build unified list from same-group demo users, resolving their OpenRAG user_id
    config = load_yaml_config()
    demo_user = session.get("demo_user", {})
    group = demo_user.get("group", "")
    current_id = demo_user.get("id", "")
    members = []
    if config and password:
        for u in config.get("demo_users", []):
            if u.get("group") == group and u.get("id") != current_id:
                openrag_uid = _resolve_openrag_uid(u, password)
                if openrag_uid:
                    members.append({
                        "user_id": openrag_uid,
                        "name": u.get("name", openrag_uid),
                        "role": role_map.get(openrag_uid, "none"),
                    })
    return render_template("app/access.html", members=members, partition=partition)


@chat_bp.route("/partition-access/<partition>/set", methods=["POST"])
def set_access(partition):
    """Set a user's role: none → revoke, new role on no-access → grant, else → update."""
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    user_id = request.form.get("user_id", "").strip()
    new_role = request.form.get("role", "none")
    old_role = request.form.get("old_role", "none")
    if not user_id:
        return "", 400
    headers = {"Authorization": f"Bearer {token}"}
    try:
        if new_role == "none" and old_role != "none":
            httpx.delete(f"{api_url}/partition/{partition}/users/{user_id}",
                         headers=headers, timeout=10.0)
        elif new_role != "none" and old_role == "none":
            httpx.post(f"{api_url}/partition/{partition}/users",
                       headers=headers, data={"user_id": user_id, "role": new_role},
                       timeout=10.0)
        elif new_role != "none" and new_role != old_role:
            httpx.patch(f"{api_url}/partition/{partition}/users/{user_id}",
                        headers=headers, data={"role": new_role}, timeout=10.0)
    except Exception:
        pass
    return partition_access(partition)


@chat_bp.route("/upload", methods=["POST"])
def upload_file():
    """Upload a file to the active partition."""
    token, api_url = _get_credentials()
    if not token or not api_url:
        return jsonify({"error": "Not authenticated"}), 401

    partition = session.get("active_partition", "openrag-all").replace("openrag-", "")
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "No file selected"}), 400

    file_id = file.filename
    try:
        resp = httpx.post(
            f"{api_url}/indexer/partition/{partition}/file/{file_id}",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (file.filename, file.stream, file.content_type)},
            timeout=60.0,
        )
        if resp.status_code in (200, 201, 202):
            data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            task_id = data.get("task_id", "")
            return jsonify({"ok": True, "task_id": task_id})
        return jsonify({"error": f"Upload failed (HTTP {resp.status_code})"}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_bp.route("/upload/status/<task_id>")
def upload_status(task_id):
    """Poll indexing task status."""
    token, api_url = _get_credentials()
    if not token or not api_url:
        return jsonify({"status": "error"}), 401
    try:
        resp = httpx.get(
            f"{api_url}/indexer/task/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
        if resp.status_code == 200:
            return resp.json()
        return jsonify({"status": "error"}), resp.status_code
    except Exception:
        return jsonify({"status": "error"}), 500


@chat_bp.route("/source-chunk")
def source_chunk():
    """Fetch a chunk by its extract URL and return rendered markdown."""
    import markdown as md

    token, api_url = _get_credentials()
    if not token:
        return "", 401
    chunk_url = request.args.get("url", "")
    if not chunk_url:
        return "", 400
    # Normalize http→https if needed
    if api_url.startswith("https://") and chunk_url.startswith("http://"):
        chunk_url = "https://" + chunk_url[7:]
    try:
        resp = httpx.get(
            chunk_url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            text = data.get("page_content", "")
            if text.startswith("[CONTEXT] "):
                text = text[10:]
            elif text.startswith("[CONTEXT]"):
                text = text[9:]
            return md.markdown(text, extensions=["tables", "fenced_code"])
    except Exception:
        pass
    return '<span style="color:var(--text-subtle);">—</span>'


def _normalize(text):
    """Remove accents for accent-insensitive matching (French collation)."""
    import unicodedata
    return unicodedata.normalize("NFD", text.lower()).encode("ascii", "ignore").decode()


@chat_bp.route("/render-markdown", methods=["POST"])
def render_markdown():
    """Render markdown text to HTML."""
    import markdown
    text = request.form.get("text", "")
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return html


@chat_bp.route("/save-prompt", methods=["POST"])
def save_prompt():
    """Save a prompt from chat history to config.yaml."""
    prompt_text = request.form.get("prompt", "").strip()
    scope = request.form.get("scope", "global")
    if not prompt_text:
        return "", 400
    config = load_yaml_config()
    if not config:
        return "", 500
    prompts = config.get("demo_prompts", [])
    prompts.append({"scope": scope, "prompt": prompt_text})
    config["demo_prompts"] = prompts
    from app.yaml_store import save_config
    save_config(config)
    return '<span class="text-[10px]" style="color:var(--success);">&#10003;</span>'


@chat_bp.route("/suggestions")
def suggestions():
    """Return prompt suggestions filtered by scope for the current user."""
    query = _normalize(request.args.get("q", "").lstrip("/"))
    config = load_yaml_config()
    if not config:
        return ""
    demo_user = session.get("demo_user", {})
    user_id = demo_user.get("id", "")
    user_group = demo_user.get("group", "")

    active_partition = session.get("active_partition", "openrag-all").replace("openrag-", "")
    prefix = session.get("partition_prefix", "")

    prompts = config.get("demo_prompts", [])
    filtered = []
    for p in prompts:
        scope = p.get("scope", "global")
        if scope == "global":
            pass
        elif scope.startswith("group:") and scope.split(":", 1)[1] != user_group:
            continue
        elif scope.startswith("partition:"):
            pname = scope.split(":", 1)[1]
            if pname != active_partition and pname != active_partition.replace(prefix, "", 1):
                continue
        elif scope.startswith("user:") and scope.split(":", 1)[1] != user_id:
            continue
        if query and query not in _normalize(p.get("prompt", "")):
            continue
        filtered.append(p)

    if not filtered:
        return f'<div class="suggestion-empty text-xs px-3 py-2" style="color:var(--text-subtle);">{t("app.no_prompts")}</div>'
    return render_template("app/suggestions.html", prompts=filtered)


@chat_bp.route("/health-check")
def health_check():
    """Check OpenRAG API health via GET /health_check."""
    token, api_url = _get_credentials()
    if not token or not api_url:
        return ""
    from markupsafe import escape
    health_url = f"{api_url}/health"
    safe_url = escape(health_url)
    try:
        resp = httpx.get(
            f"{api_url}/health_check",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
        if resp.status_code == 200:
            return f' <span class="separator">&middot;</span> <a href="{safe_url}" target="_blank" rel="noopener" style="color:var(--success);">&#9679; online</a>'
        return f' <span class="separator">&middot;</span> <a href="{safe_url}" target="_blank" rel="noopener" style="color:var(--danger);">&#9679; error</a>'
    except Exception:
        return f' <span class="separator">&middot;</span> <a href="{safe_url}" target="_blank" rel="noopener" style="color:var(--danger);">&#9679; offline</a>'


@chat_bp.route("/user-role")
def user_role():
    """Check if current session user is admin via GET /users/info."""
    token, api_url = _get_credentials()
    if not token or not api_url:
        return ""
    result = _check_role(api_url, token)
    if result is None:
        return ""
    return _role_badge(result)


@chat_bp.route("/user-role/<user_id>")
def user_role_by_id(user_id):
    """Check if a specific demo user is admin (for login page)."""
    from app.yaml_store import load_config
    from app.crypto import decrypt_token as do_decrypt
    config = load_config()
    password = current_app.config.get("ADMIN_PASSWORD")
    if not config or not password:
        return ""
    user = None
    for u in config.get("demo_users", []):
        if u["id"] == user_id:
            user = u
            break
    if not user:
        return ""
    try:
        token = do_decrypt(user["token"], password, user["id"])
    except Exception:
        return ""
    api_url = user.get("api_url", "").rstrip("/")
    result = _check_role(api_url, token)
    if result is None:
        return ""
    return _role_badge(result)


@chat_bp.route("/api-version")
def api_version():
    """Fetch OpenRAG version from /version endpoint."""
    token, api_url = _get_credentials()
    if not token or not api_url:
        return ""
    try:
        resp = httpx.get(
            f"{api_url}/version",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            version = data.get("version", data.get("app_version", str(data)))
            from markupsafe import escape
            safe_url = escape(api_url)
            safe_ver = escape(version)
            return (
                f' <span class="separator">&middot;</span> '
                f'<a href="{safe_url}/indexerui/" target="_blank" rel="noopener">OpenRAG {safe_ver}</a>'
            )
    except Exception:
        pass
    return ""


@chat_bp.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear conversation history for the active partition."""
    partition = session.get("active_partition", "openrag-all")
    session.pop(f"chat_history_{partition}", None)
    return "", 204


@chat_bp.route("/select-partition", methods=["POST"])
def select_partition():
    """Set active partition in session."""
    partition = request.form.get("partition", "openrag-all")
    old_partition = session.get("active_partition")
    session["active_partition"] = partition
    if old_partition and old_partition != partition:
        session.pop(f"chat_history_{old_partition}", None)
    token, api_url = _get_credentials()
    parts = _fetch_partitions(token, api_url)
    prefix = _common_prefix(parts)
    session["partition_prefix"] = prefix
    display = partition.replace("openrag-", "")
    if prefix and partition != "openrag-all":
        display = display[len(prefix):]
    active_role = ""
    for p in parts:
        if p["id"] == partition:
            active_role = p.get("role") or ""
            break
    tree_html = render_template("app/partitions.html", partitions=parts, active=partition, strip_prefix=prefix)
    oob = f'<span id="partition-label" hx-swap-oob="true" class="text-base font-semibold" data-role="{active_role}">{display}</span>'
    return tree_html + oob


def _friendly_error(status_code, body):
    """Turn an API error into a human-readable message in the user's language."""
    detail = ""
    try:
        err = json.loads(body)
        detail = err.get("detail", "")
    except Exception:
        pass

    if "EMBEDDING" in detail.upper() or "embedding" in detail.lower():
        return t("chat.error.embedding")
    if status_code in (401, 403):
        return t("chat.error.auth")
    if status_code == 503 or "unavailable" in detail.lower():
        return t("chat.error.unavailable")
    return t("chat.error.generic")


@chat_bp.route("/search")
def semantic_search():
    """Semantic search — returns chunks as HTML."""
    import markdown as md

    query = request.args.get("text", "").strip()
    if not query:
        return "", 400
    token, api_url = _get_credentials()
    if not token:
        return "", 401
    partition = session.get("active_partition", "openrag-all").replace("openrag-", "")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        if partition and partition != "all":
            resp = httpx.get(f"{api_url}/search/partition/{partition}",
                             params={"text": query, "top_k": 10}, headers=headers, timeout=15.0)
        else:
            resp = httpx.get(f"{api_url}/search",
                             params={"text": query, "top_k": 10}, headers=headers, timeout=15.0)
        if resp.status_code != 200:
            return jsonify([])
        results = resp.json()
        items = results if isinstance(results, list) else results.get("documents", results.get("results", results.get("chunks", [])))
        chunks = []
        for item in items[:10]:
            text = item.get("page_content", item.get("content", ""))
            if not text and item.get("link"):
                link = item["link"]
                if api_url.startswith("https://") and link.startswith("http://"):
                    link = "https://" + link[7:]
                try:
                    r = httpx.get(link, headers=headers, timeout=5.0)
                    if r.status_code == 200:
                        text = r.json().get("page_content", "")
                except Exception:
                    pass
            if text.startswith("[CONTEXT] "):
                text = text[10:]
            elif text.startswith("[CONTEXT]"):
                text = text[9:]
            meta = item.get("metadata", {})
            fname = meta.get("original_filename", meta.get("filename", meta.get("file_id", "")))
            source = meta.get("source", "")
            partition_name = meta.get("partition", partition)
            static_path = source.replace("/app/data/", "/static/", 1) if source else ""
            page = meta.get("page", "")
            score = item.get("score", item.get("distance", None))
            rendered = md.markdown(text, extensions=["tables", "fenced_code"])
            chunks.append({
                "filename": fname,
                "partition": partition_name,
                "static_path": static_path,
                "page": str(page) if page else "",
                "score": score,
                "html": rendered,
            })
        return jsonify(chunks)
    except Exception:
        return f'<div style="color:var(--danger);">{t("chat.error.generic")}</div>'



def _sse_event(event, data):
    """Format an SSE event, handling multi-line data."""
    lines = data.replace("\n", "")  # SSE data must be single-line for simple cases
    return f"event: {event}\ndata: {lines}\n\n"


@chat_bp.route("/stream")
def chat_stream():
    """SSE endpoint — streams chat tokens then sources."""
    message = request.args.get("message", "").strip()
    if not message:
        return "", 400

    token, api_url = _get_credentials()
    if not token:
        return "", 401

    partition = session.get("active_partition", "openrag-all")

    # Build conversation history for this partition
    history_key = f"chat_history_{partition}"
    history = session.get(history_key, [])
    history.append({"role": "user", "content": message})

    def generate():
        import markdown as md

        sources = []
        full_text = []
        url = f"{api_url}/v1/chat/completions"
        try:
            with httpx.stream(
                "POST",
                url,
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "model": partition,
                    "messages": history,
                    "stream": True,
                },
                timeout=httpx.Timeout(connect=10.0, read=120.0, write=10.0, pool=10.0),
            ) as response:
                if response.status_code != 200:
                    body = response.read().decode()
                    msg = _friendly_error(response.status_code, body)
                    yield _sse_event("token", f"<span style='color:var(--danger)'>{msg}</span>")
                    yield "event: done\ndata: \n\n"
                    return
                for line in response.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choices = chunk.get("choices", [])
                    if not choices:
                        continue
                    delta = choices[0].get("delta", {})
                    token_text = delta.get("content", "")
                    # Capture sources from extra (may be a JSON string or dict)
                    if not sources:
                        extra = chunk.get("extra")
                        if isinstance(extra, str):
                            try:
                                extra = json.loads(extra)
                            except (json.JSONDecodeError, ValueError):
                                extra = None
                        if isinstance(extra, dict) and isinstance(extra.get("sources"), list):
                            sources = extra["sources"]
                    if token_text:
                        full_text.append(token_text)
                        html = f"<span>{token_text}</span>"
                        yield _sse_event("token", html)
        except httpx.ConnectError:
            yield _sse_event("token", f"<div class='mt-2' style='color:var(--danger)'>{t('chat.error.unavailable')}</div>")
        except httpx.TimeoutException:
            yield _sse_event("token", f"<div class='mt-2' style='color:var(--danger)'>{t('chat.error.timeout')}</div>")
        except Exception as e:
            current_app.logger.error("Stream error: %s", e)
            yield _sse_event("token", f"<div class='mt-2' style='color:var(--danger)'>{t('chat.error.generic')}</div>")

        # Save assistant response to conversation history
        if full_text:
            assistant_text = "".join(full_text)
            history.append({"role": "assistant", "content": assistant_text})
            # Keep last 20 messages to avoid session bloat
            session[history_key] = history[-20:]

            rendered = md.markdown(assistant_text, extensions=["tables", "fenced_code"])
            yield _sse_event("rendered", rendered)

        # Send sources after stream ends
        if sources:
            sources_html = render_template("app/sources.html", sources=sources)
            yield _sse_event("sources", sources_html)
        yield "event: done\ndata: \n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    )

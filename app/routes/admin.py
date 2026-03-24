# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Admin routes — CRUD for groups, users, prompts. Saves config.yaml on every mutation."""

import random

import httpx
from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app, jsonify,
)

from app.crypto import encrypt_token, decrypt_token
from app.yaml_store import load_config, save_config

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

DEFAULT_API_URL = "https://demo.open-rag.ai/"

RANDOM_FIRST_NAMES_F = ["Alice", "Marie", "Sophie", "Claire", "Emma", "Léa", "Chloé", "Camille", "Julie", "Sarah"]
RANDOM_FIRST_NAMES_M = ["Bob", "Pierre", "Thomas", "Nicolas", "Lucas", "Hugo", "Louis", "Antoine", "Julien", "Marc"]
RANDOM_LAST_NAMES = ["Martin", "Dubois", "Laurent", "Moreau", "Bernard", "Petit", "Roux", "Leroy", "Garcia", "Faure"]
RANDOM_TITLES_F = [
    "Legal Counsel", "HR Director", "Data Analyst", "Project Manager",
    "Chief of Staff", "Compliance Officer", "Communications Lead",
    "Research Director", "Finance Controller", "Policy Advisor",
]
RANDOM_TITLES_M = [
    "Legal Counsel", "HR Manager", "Data Engineer", "Project Lead",
    "Operations Director", "Security Officer", "Sales Manager",
    "Research Lead", "Finance Director", "Technical Advisor",
]
RANDOM_COLORS = [
    "#E85D9A", "#4F6EF7", "#F59E0B", "#22D3A4", "#8B5CF6",
    "#06B6D4", "#EF4444", "#10B981", "#F97316", "#6366F1",
]


def _is_htmx():
    return request.headers.get("HX-Request") == "true"


def _sorted_groups(config):
    return sorted(config.get("groups", []), key=lambda g: g.get("label", "").lower())


@admin_bp.route("")
def admin_index():
    tab = request.args.get("tab", "groups")
    config = load_config()
    return render_template("admin/index.html",
                           tab=tab,
                           groups=_sorted_groups(config),
                           users=config.get("demo_users", []),
                           prompts=config.get("demo_prompts", []))


@admin_bp.route("/tab/<tab>")
def admin_tab(tab):
    config = load_config()
    if tab == "groups":
        return render_template("admin/_groups.html", groups=_sorted_groups(config))
    elif tab == "users":
        return render_template("admin/_users.html",
                               users=config.get("demo_users", []),
                               groups=_sorted_groups(config))
    elif tab == "prompts":
        return render_template("admin/_prompts.html",
                               prompts=config.get("demo_prompts", []),
                               groups=_sorted_groups(config),
                               users=config.get("demo_users", []))
    return "", 404


# --- Groups ---

@admin_bp.route("/users/lookup", methods=["POST"])
def lookup_user():
    """Fetch user info from API token via GET /users/info."""
    api_url = request.form.get("api_url", DEFAULT_API_URL).strip().rstrip("/")
    token = request.form.get("token", "").strip()
    if not api_url or not token:
        return jsonify({"error": "API URL and token required"}), 400
    try:
        resp = httpx.get(
            f"{api_url}/users/info",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            return jsonify({
                "name": data.get("display_name", ""),
                "email": data.get("external_user_id", ""),
            })
        return jsonify({"error": f"HTTP {resp.status_code}"}), 400
    except httpx.ConnectError:
        return jsonify({"error": "Cannot connect"}), 400
    except httpx.TimeoutException:
        return jsonify({"error": "Timeout"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@admin_bp.route("/groups/add", methods=["POST"])
def add_group():
    config = load_config()
    groups = _sorted_groups(config)
    label = request.form.get("label", "").strip()
    color = request.form.get("color", "#4F6EF7")
    icon = request.form.get("icon", "folder").strip()
    if label:
        gid = label.lower().replace(" ", "-")
        existing_ids = {g["id"] for g in groups}
        base_id = gid
        counter = 2
        while gid in existing_ids:
            gid = f"{base_id}-{counter}"
            counter += 1
        groups.append({"id": gid, "label": label, "color": color, "icon": icon})
        config["groups"] = groups
        save_config(config)
    if _is_htmx():
        return render_template("admin/_groups.html", groups=_sorted_groups(config))
    return redirect(url_for("admin.admin_index"))


@admin_bp.route("/groups/edit/<int:idx>", methods=["GET", "POST"])
def edit_group(idx):
    config = load_config()
    groups = _sorted_groups(config)
    if idx < 0 or idx >= len(groups):
        return redirect(url_for("admin.admin_index"))
    if request.method == "POST":
        groups[idx]["label"] = request.form.get("label", groups[idx]["label"]).strip()
        groups[idx]["color"] = request.form.get("color", groups[idx]["color"])
        groups[idx]["icon"] = request.form.get("icon", groups[idx]["icon"]).strip()
        config["groups"] = groups
        save_config(config)
        if _is_htmx():
            return render_template("admin/_groups.html", groups=_sorted_groups(config))
        return redirect(url_for("admin.admin_index"))
    # GET → return edit form
    if _is_htmx():
        return render_template("admin/_group_edit.html", group=groups[idx], idx=idx)
    return redirect(url_for("admin.admin_index"))


@admin_bp.route("/groups/remove/<int:idx>", methods=["DELETE"])
def remove_group(idx):
    config = load_config()
    groups = _sorted_groups(config)
    if 0 <= idx < len(groups):
        groups.pop(idx)
        config["groups"] = groups
        save_config(config)
    if _is_htmx():
        return render_template("admin/_groups.html", groups=_sorted_groups(config))
    return redirect(url_for("admin.admin_index"))


# --- Token validation ---

@admin_bp.route("/users/validate-token", methods=["POST"])
def validate_token():
    """Test an API token by calling GET /v1/models on the target server."""
    api_url = request.form.get("api_url", "").strip().rstrip("/")
    token = request.form.get("token", "").strip()
    if not api_url or not token:
        return jsonify({"valid": False, "error": "API URL and token are required"}), 400
    try:
        resp = httpx.get(
            f"{api_url}/v1/models",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            return jsonify({"valid": True})
        return jsonify({"valid": False, "error": f"HTTP {resp.status_code}"}), 400
    except httpx.ConnectError:
        return jsonify({"valid": False, "error": "Cannot connect to server"}), 400
    except httpx.TimeoutException:
        return jsonify({"valid": False, "error": "Connection timed out"}), 400
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 400


# --- Users ---

@admin_bp.route("/users/add", methods=["POST"])
def add_user():
    config = load_config()
    users = config.get("demo_users", [])
    password = current_app.config.get("ADMIN_PASSWORD")

    name = request.form.get("name", "").strip()
    title = request.form.get("title", "").strip()
    email = request.form.get("email", "").strip()
    group = request.form.get("group", "")
    genre = request.form.get("genre", "neutral")
    avatar_color = request.form.get("avatar_color", "#4F6EF7")
    api_url = request.form.get("api_url", DEFAULT_API_URL).strip().rstrip("/")
    token = request.form.get("token", "").strip()

    # Collect form values to re-fill on error
    form_values = {
        "name": name, "title": title, "email": email, "group": group,
        "genre": genre, "avatar_color": avatar_color,
        "api_url": api_url, "token": token,
    }

    error = None
    if not token:
        error = "Token is required"
    elif not group:
        error = "Group is required"
    elif not password:
        error = "Session expired — please unlock again"

    # Check duplicate token
    if not error and password:
        from app.crypto import decrypt_token
        for u in users:
            try:
                existing = decrypt_token(u["token"], password, u["id"])
                if existing == token:
                    error = f"This token is already used by {u['name']}"
                    break
            except Exception:
                pass

    # Validate token against API
    if not error:
        try:
            resp = httpx.get(
                f"{api_url}/v1/models",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0,
            )
            if resp.status_code != 200:
                error = f"Token rejected by server (HTTP {resp.status_code})"
        except httpx.ConnectError:
            error = f"Cannot connect to {api_url}"
        except httpx.TimeoutException:
            error = f"Connection to {api_url} timed out"
        except Exception as e:
            error = str(e)

    if not error:
        uid = name.lower().replace(" ", "-")
        existing_ids = {u["id"] for u in users}
        base_id = uid
        counter = 2
        while uid in existing_ids:
            uid = f"{base_id}-{counter}"
            counter += 1
        users.append({
            "id": uid,
            "name": name,
            "title": title,
            "email": email,
            "group": group,
            "genre": genre,
            "avatar_color": avatar_color,
            "api_url": api_url,
            "token": encrypt_token(token, password, uid),
        })
        config["demo_users"] = users
        save_config(config)

    if _is_htmx():
        return render_template("admin/_users.html",
                               users=config.get("demo_users", []),
                               groups=_sorted_groups(config),
                               error=error,
                               form=form_values if error else {})
    return redirect(url_for("admin.admin_index"))


@admin_bp.route("/users/edit/<int:idx>", methods=["GET", "POST"])
def edit_user(idx):
    config = load_config()
    users = config.get("demo_users", [])
    password = current_app.config.get("ADMIN_PASSWORD")
    if idx < 0 or idx >= len(users):
        return redirect(url_for("admin.admin_index"))
    if request.method == "POST":
        u = users[idx]
        u["name"] = request.form.get("name", u["name"]).strip()
        u["title"] = request.form.get("title", u.get("title", "")).strip()
        u["group"] = request.form.get("group", u.get("group", ""))
        u["genre"] = request.form.get("genre", u.get("genre", "neutral"))
        u["email"] = request.form.get("email", u.get("email", "")).strip()
        u["avatar_color"] = request.form.get("avatar_color", u.get("avatar_color", "#4F6EF7"))
        u["api_url"] = request.form.get("api_url", u.get("api_url", "")).strip()
        new_token = request.form.get("token", "").strip()
        if new_token and password:
            u["token"] = encrypt_token(new_token, password, u["id"])
        config["demo_users"] = users
        save_config(config)
        if _is_htmx():
            return render_template("admin/_users.html",
                                   users=config.get("demo_users", []),
                                   groups=_sorted_groups(config))
        return redirect(url_for("admin.admin_index"))
    if _is_htmx():
        return render_template("admin/_user_edit.html",
                               user=users[idx], idx=idx,
                               groups=_sorted_groups(config))
    return redirect(url_for("admin.admin_index"))


@admin_bp.route("/users/remove/<int:idx>", methods=["DELETE"])
def remove_user(idx):
    config = load_config()
    users = config.get("demo_users", [])
    if 0 <= idx < len(users):
        users.pop(idx)
        config["demo_users"] = users
        save_config(config)
    if _is_htmx():
        return render_template("admin/_users.html",
                               users=config.get("demo_users", []),
                               groups=_sorted_groups(config))
    return redirect(url_for("admin.admin_index"))


@admin_bp.route("/users/random", methods=["GET"])
def random_user():
    """Return JSON with random user data for the form."""
    genre = random.choice(["male", "female"])
    if genre == "female":
        first = random.choice(RANDOM_FIRST_NAMES_F)
        title = random.choice(RANDOM_TITLES_F)
    else:
        first = random.choice(RANDOM_FIRST_NAMES_M)
        title = random.choice(RANDOM_TITLES_M)
    last = random.choice(RANDOM_LAST_NAMES)
    color = random.choice(RANDOM_COLORS)
    return jsonify({
        "name": f"{first} {last}",
        "title": title,
        "email": f"{first.lower()}.{last.lower()}@example.com",
        "genre": genre,
        "avatar_color": color,
    })


# --- Prompts ---

@admin_bp.route("/prompts/add", methods=["POST"])
def add_prompt():
    config = load_config()
    prompts = config.get("demo_prompts", [])
    scope = request.form.get("scope", "global")
    prompt_text = request.form.get("prompt", "").strip()
    if prompt_text:
        prompts.append({
            "scope": scope,
            "prompt": prompt_text,
        })
        config["demo_prompts"] = prompts
        save_config(config)
    if _is_htmx():
        return render_template("admin/_prompts.html",
                               prompts=config.get("demo_prompts", []),
                               groups=_sorted_groups(config),
                               users=config.get("demo_users", []))
    return redirect(url_for("admin.admin_index"))


@admin_bp.route("/prompts/edit/<int:idx>", methods=["GET", "POST"])
def edit_prompt(idx):
    config = load_config()
    prompts = config.get("demo_prompts", [])
    if idx < 0 or idx >= len(prompts):
        return redirect(url_for("admin.admin_index"))
    if request.method == "POST":
        prompts[idx]["scope"] = request.form.get("scope", prompts[idx].get("scope", "global"))
        prompts[idx]["prompt"] = request.form.get("prompt", prompts[idx]["prompt"]).strip()
        config["demo_prompts"] = prompts
        save_config(config)
        if _is_htmx():
            return render_template("admin/_prompts.html",
                                   prompts=config.get("demo_prompts", []),
                                   groups=_sorted_groups(config),
                                   users=config.get("demo_users", []))
        return redirect(url_for("admin.admin_index"))
    if _is_htmx():
        return render_template("admin/_prompt_edit.html",
                               prompt=prompts[idx], idx=idx,
                               groups=_sorted_groups(config),
                               users=config.get("demo_users", []))
    return redirect(url_for("admin.admin_index"))


@admin_bp.route("/prompts/remove/<int:idx>", methods=["DELETE"])
def remove_prompt(idx):
    config = load_config()
    prompts = config.get("demo_prompts", [])
    if 0 <= idx < len(prompts):
        prompts.pop(idx)
        config["demo_prompts"] = prompts
        save_config(config)
    if _is_htmx():
        return render_template("admin/_prompts.html",
                               prompts=config.get("demo_prompts", []),
                               groups=_sorted_groups(config),
                               users=config.get("demo_users", []))
    return redirect(url_for("admin.admin_index"))



@admin_bp.route("/import-config", methods=["POST"])
def import_config():
    """Import a config.yaml file, encrypting any plaintext tokens."""
    import yaml

    password = current_app.config.get("ADMIN_PASSWORD")
    if not password:
        return redirect(url_for("admin.admin_index"))

    file = request.files.get("file")
    if not file or not file.filename:
        return redirect(url_for("admin.admin_index"))

    try:
        data = yaml.safe_load(file.stream)
    except Exception:
        return redirect(url_for("admin.admin_index"))

    if not isinstance(data, dict):
        return redirect(url_for("admin.admin_index"))

    # Encrypt any plaintext tokens
    for u in data.get("demo_users", []):
        tok = u.get("token", "")
        if tok and not tok.startswith("enc:"):
            u["token"] = encrypt_token(tok, password, u["id"])

    # Keep existing password_hash
    existing = load_config()
    if existing and "password_hash" in existing:
        data["password_hash"] = existing["password_hash"]

    save_config(data)
    return redirect(url_for("admin.admin_index"))

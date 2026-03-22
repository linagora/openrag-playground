# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Session middleware — master password gate.

Not a single page, template fragment, or API response is accessible without a valid session.
Only /unlock, /setup (first-run), /health, and static files are exempt.
"""

from flask import Flask, session, redirect, url_for, request, render_template


from app.yaml_store import load_config


EXEMPT_ENDPOINTS = {
    "auth.unlock", "setup.setup_index", "health", "static", "set_language",
    "pages.about", "pages.gdpr", "pages.ai_act", "pages.sovereignty", "pages.legal",
}


def init_auth(app: Flask):
    @app.before_request
    def require_auth():
        # Always allow static files and health check
        if request.endpoint and request.endpoint in EXEMPT_ENDPOINTS:
            return None

        # Allow /static/ paths (fallback for unnamed static routes)
        if request.path.startswith("/static/"):
            return None

        is_htmx = request.headers.get("HX-Request") == "true"
        config = load_config()

        # No config → invalidate any stale session → setup wizard
        if config is None:
            session.clear()
            if request.endpoint and request.endpoint.startswith("setup."):
                return None
            if is_htmx:
                return "", 204
            return redirect(url_for("setup.setup_index"))

        # Config exists but no session → render unlock inline
        if not session.get("authenticated"):
            if request.endpoint == "auth.unlock":
                return None
            if is_htmx:
                return "", 204
            return render_template("unlock.html", next_url=request.url), 401

        # Session valid but password lost (server restart) → render unlock inline
        from flask import current_app
        if not current_app.config.get("ADMIN_PASSWORD"):
            session.clear()
            if request.endpoint == "auth.unlock":
                return None
            if is_htmx:
                return "", 204
            return render_template("unlock.html", next_url=request.url), 401

        return None

# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Route registration."""

from flask import Flask, jsonify, render_template, request, session

from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.chat import chat_bp
from app.routes.demo import demo_bp
from app.routes.pages import pages_bp
from app.routes.setup import setup_bp


def register_routes(app: Flask):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(demo_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(setup_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/")
    def index():
        from app.yaml_store import load_config
        config = load_config()
        if not config:
            return render_template("base.html")
        groups = config.get("groups", [])
        users = config.get("demo_users", [])
        group_map = {g["id"]: g for g in groups}

        # Sort by group label then name
        def sort_key(u):
            g = group_map.get(u.get("group", ""), {})
            return (g.get("label", "zzz").lower(), u.get("name", "").lower())
        hidden = set(session.get("hidden_users", []))
        users = [u for u in users if u.get("id") not in hidden]
        users_sorted = sorted(users, key=sort_key)

        # Group users by group id (ordered)
        grouped_users = []
        current_group = None
        for u in users_sorted:
            gid = u.get("group", "")
            if gid != current_group:
                current_group = gid
                grouped_users.append({
                    "group": group_map.get(gid),
                    "users": [],
                })
            grouped_users[-1]["users"].append(u)

        return render_template("login.html",
                               grouped_users=grouped_users,
                               groups=groups)

    @app.route("/hide-user", methods=["POST"])
    def hide_user():
        user_id = request.form.get("user_id", "")
        if user_id:
            hidden = session.get("hidden_users", [])
            if user_id not in hidden:
                hidden.append(user_id)
                session["hidden_users"] = hidden
        return "", 204

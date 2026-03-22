# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Demo routes — persona login, /app shell."""

from flask import (
    Blueprint, render_template, request, session, redirect, url_for, current_app,
)

from app.crypto import decrypt_token
from app.yaml_store import load_config

demo_bp = Blueprint("demo", __name__)


@demo_bp.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id", "")
    config = load_config()
    password = current_app.config.get("ADMIN_PASSWORD")

    if not config or not password:
        return redirect(url_for("index"))

    # Find user
    user = None
    for u in config.get("demo_users", []):
        if u["id"] == user_id:
            user = u
            break

    if not user:
        return redirect(url_for("index"))

    # Decrypt token
    try:
        token = decrypt_token(user["token"], password, user["id"])
    except Exception:
        return redirect(url_for("index"))

    # Find group info
    group_info = None
    for g in config.get("groups", []):
        if g["id"] == user.get("group"):
            group_info = g
            break

    # Store in session
    session["demo_user"] = {
        "id": user["id"],
        "name": user["name"],
        "title": user["title"],
        "group": user.get("group", ""),
        "group_label": group_info["label"] if group_info else "",
        "group_color": group_info["color"] if group_info else "",
        "group_icon": group_info["icon"] if group_info else "",
        "genre": user.get("genre", "neutral"),
        "avatar_color": user.get("avatar_color", "#4F6EF7"),
    }
    session["user_token"] = token
    session["user_api_url"] = user.get("api_url", "")

    return redirect(url_for("demo.app_shell"))


@demo_bp.route("/logout-demo", methods=["POST"])
def logout_demo():
    session.pop("demo_user", None)
    session.pop("user_token", None)
    session.pop("user_api_url", None)
    session.pop("active_partition", None)
    return redirect(url_for("index"))


@demo_bp.route("/app")
def app_shell():
    if "demo_user" not in session:
        return redirect(url_for("index"))
    return render_template("app/shell.html", user=session["demo_user"])

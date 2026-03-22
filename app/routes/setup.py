# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Setup routes — first-run: set master password, create config.yaml."""

from flask import (
    Blueprint, render_template, request, session,
    redirect, url_for, current_app,
)

from app.crypto import hash_password
from app.yaml_store import save_config, load_config

setup_bp = Blueprint("setup", __name__, url_prefix="/setup")


@setup_bp.route("")
def setup_index():
    if load_config() is not None:
        return redirect(url_for("index"))
    return render_template("setup/index.html")


@setup_bp.route("/save-password", methods=["POST"])
def save_password():
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")

    if len(password) < 8:
        return render_template("setup/index.html",
                               error="Password must be at least 8 characters")
    if password != confirm:
        return render_template("setup/index.html",
                               error="Passwords do not match")

    # Create config.yaml immediately
    config = {
        "password_hash": hash_password(password),
        "groups": [],
        "demo_users": [],
        "demo_prompts": [],
    }
    save_config(config)

    # Authenticate and cache password
    session["authenticated"] = True
    session.permanent = True
    current_app.config["ADMIN_PASSWORD"] = password

    return redirect(url_for("admin.admin_index"))

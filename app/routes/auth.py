# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Auth routes — /unlock (master password gate)."""

from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from app.yaml_store import load_config
from app.crypto import verify_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/unlock", methods=["GET", "POST"])
def unlock():
    config = load_config()
    if config is None:
        return redirect(url_for("setup.setup_index"))

    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if verify_password(password, config["password_hash"]):
            session["authenticated"] = True
            session.permanent = True
            # Cache password in app config for token decryption
            current_app.config["ADMIN_PASSWORD"] = password
            next_url = request.form.get("next", "")
            return redirect(next_url or url_for("index"))
        error = "Invalid password"

    return render_template("unlock.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.unlock"))

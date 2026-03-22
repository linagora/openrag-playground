# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""OpenRAG Playground — Flask app factory."""

import os
from datetime import datetime, timedelta

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-key")
    app.permanent_session_lifetime = timedelta(hours=24)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now().year}

    from app.auth import init_auth
    from app.i18n import init_i18n
    from app.routes import register_routes

    register_routes(app)
    init_auth(app)
    init_i18n(app)

    return app

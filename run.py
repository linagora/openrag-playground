# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Entry point for Flask dev server and gunicorn."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

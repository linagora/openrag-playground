# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Footer modal pages — About, GDPR, AI Act, Data Sovereignty, Legal Notice."""

from flask import Blueprint, render_template
from app.i18n import t

pages_bp = Blueprint("pages", __name__)


def _modal(title, content):
    return render_template("partials/modal.html", title=title, content=content)


@pages_bp.route("/about")
def about():
    return _modal(t("modal.about.title"), t("modal.about.body"))


@pages_bp.route("/gdpr")
def gdpr():
    return _modal(t("modal.gdpr.title"), t("modal.gdpr.body"))


@pages_bp.route("/ai-act")
def ai_act():
    return _modal(t("modal.ai_act.title"), t("modal.ai_act.body"))


@pages_bp.route("/sovereignty")
def sovereignty():
    return _modal(t("modal.sovereignty.title"), t("modal.sovereignty.body"))


@pages_bp.route("/legal")
def legal():
    return _modal(t("modal.legal.title"), t("modal.legal.body"))

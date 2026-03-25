# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Footer modal pages — rendered from markdown files in docs/."""

import os

import markdown
from flask import Blueprint, render_template

from app.i18n import get_locale, t

pages_bp = Blueprint("pages", __name__)

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs")


def _load_doc(name):
    """Load a markdown file from docs/{lang}/{name}.md and render to HTML."""
    lang = get_locale()
    path = os.path.join(DOCS_DIR, lang, f"{name}.md")
    if not os.path.exists(path):
        path = os.path.join(DOCS_DIR, "en", f"{name}.md")
    if not os.path.exists(path):
        return name.replace("-", " ").title(), "<p>Document not found.</p>"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Extract title from first # heading but keep it in content
    title = name.replace("-", " ").title()
    lines = text.split("\n", 1)
    if lines[0].startswith("# "):
        title = lines[0][2:].strip()
    html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return title, html


def _modal(title, content, hide_title=False):
    return render_template("partials/modal.html", title=title if not hide_title else "", content=content)


@pages_bp.route("/about")
def about():
    title, body = _load_doc("about")
    return _modal(title, body, hide_title=True)


@pages_bp.route("/gdpr")
def gdpr():
    title, body = _load_doc("gdpr")
    return _modal(title, body, hide_title=True)


@pages_bp.route("/ai-act")
def ai_act():
    title, body = _load_doc("ai-act")
    return _modal(title, body, hide_title=True)


@pages_bp.route("/sovereignty")
def sovereignty():
    title, body = _load_doc("sovereignty")
    return _modal(title, body, hide_title=True)


@pages_bp.route("/legal")
def legal():
    title, body = _load_doc("legal")
    return _modal(title, body, hide_title=True)


@pages_bp.route("/manual")
def manual():
    title, body = _load_doc("manual")
    return _modal(title, body, hide_title=True)

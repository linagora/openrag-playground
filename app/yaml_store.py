# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Read/write config.yaml — the only persistent storage."""

import yaml

from app.config import CONFIG_PATH


def load_config() -> dict | None:
    """Load config.yaml. Returns None if file doesn't exist."""
    try:
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None


def save_config(data: dict) -> None:
    """Write config dict to config.yaml."""
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

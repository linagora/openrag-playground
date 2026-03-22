# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration constants and environment variable access."""

import os

CONFIG_PATH = os.environ.get("CONFIG_PATH", "config.yaml")

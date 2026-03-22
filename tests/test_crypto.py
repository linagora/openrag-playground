# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for app.crypto — the one place where a silent bug locks you out."""

import pytest

from app.crypto import encrypt_token, decrypt_token


PASSWORD = "S3cure-Demo-Pass!"
USER_ID = "alice-martin"
TOKEN = "sk-live-abc123xyz789"


def test_round_trip_correct_password():
    """Encrypt then decrypt with correct password returns original token."""
    encrypted = encrypt_token(TOKEN, PASSWORD, USER_ID)
    result = decrypt_token(encrypted, PASSWORD, USER_ID)
    assert result == TOKEN


def test_decrypt_wrong_password_raises():
    """Decrypt with wrong password raises an exception."""
    encrypted = encrypt_token(TOKEN, PASSWORD, USER_ID)
    with pytest.raises(Exception):
        decrypt_token(encrypted, "wrong-password", USER_ID)


def test_decrypt_wrong_user_id_raises():
    """Decrypt with wrong user id (wrong salt) raises an exception."""
    encrypted = encrypt_token(TOKEN, PASSWORD, USER_ID)
    with pytest.raises(Exception):
        decrypt_token(encrypted, PASSWORD, "bob-dubois")


def test_encrypted_value_has_prefix():
    """Encrypted value starts with enc:v1: prefix."""
    encrypted = encrypt_token(TOKEN, PASSWORD, USER_ID)
    assert encrypted.startswith("enc:v1:")

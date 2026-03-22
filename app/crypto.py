# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""AES-256-GCM token encryption with PBKDF2 key derivation.

Format: enc:v1:<base64(iv + ciphertext + tag)>

- Key: PBKDF2-SHA256, 310 000 iterations, 32 bytes
- Salt: deterministic from user id (never stored separately)
- Cipher: AES-256-GCM (12-byte IV, 16-byte auth tag)
"""

import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

PREFIX = "enc:v1:"
ITERATIONS = 310_000
KEY_LENGTH = 32  # 256 bits
IV_LENGTH = 12   # 96 bits, standard for GCM


def _derive_key(password: str, user_id: str) -> bytes:
    """Derive a 256-bit key from admin password + user id as salt."""
    salt = hashlib.sha256(user_id.encode()).digest()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode())


def encrypt_token(token: str, password: str, user_id: str) -> str:
    """Encrypt a plaintext token. Returns 'enc:v1:<base64>'."""
    key = _derive_key(password, user_id)
    iv = os.urandom(IV_LENGTH)
    aesgcm = AESGCM(key)
    # GCM appends the 16-byte auth tag to the ciphertext
    ciphertext_and_tag = aesgcm.encrypt(iv, token.encode(), None)
    payload = base64.b64encode(iv + ciphertext_and_tag).decode()
    return f"{PREFIX}{payload}"


def decrypt_token(encrypted: str, password: str, user_id: str) -> str:
    """Decrypt an 'enc:v1:...' token. Raises on wrong password or user id."""
    if not encrypted.startswith(PREFIX):
        raise ValueError(f"Invalid token format: missing '{PREFIX}' prefix")
    raw = base64.b64decode(encrypted[len(PREFIX):])
    iv = raw[:IV_LENGTH]
    ciphertext_and_tag = raw[IV_LENGTH:]
    key = _derive_key(password, user_id)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(iv, ciphertext_and_tag, None)
    return plaintext.decode()


def hash_password(password: str) -> str:
    """Hash a password with bcrypt."""
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash."""
    import bcrypt
    return bcrypt.checkpw(password.encode(), hashed.encode())

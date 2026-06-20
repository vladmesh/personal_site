"""Password hashing and login rate limiting for the admin panel.

Uses the standard library only (PBKDF2-HMAC-SHA256), so there is no extra
dependency to install or type-stub. Hashes are self-describing
(``pbkdf2_sha256$<iterations>$<salt_b64>$<dk_b64>``) so the iteration count can
be raised later without invalidating existing hashes.
"""

from __future__ import annotations

import hmac
import secrets
import time
from base64 import b64decode, b64encode
from dataclasses import dataclass
from hashlib import pbkdf2_hmac

_ALGORITHM = "pbkdf2_sha256"
_HASH_NAME = "sha256"
# OWASP-recommended floor for PBKDF2-HMAC-SHA256.
_ITERATIONS = 600_000
_DKLEN = 32
_SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Return a self-describing PBKDF2 hash of ``password``."""
    salt = secrets.token_bytes(_SALT_BYTES)
    derived = pbkdf2_hmac(_HASH_NAME, password.encode("utf-8"), salt, _ITERATIONS, _DKLEN)
    return f"{_ALGORITHM}${_ITERATIONS}${b64encode(salt).decode()}${b64encode(derived).decode()}"


def verify_password(password: str, stored: str) -> bool:
    """Constant-time check of ``password`` against a stored PBKDF2 hash.

    Returns ``False`` (never raises) for malformed or unsupported hashes.
    """
    try:
        algorithm, iterations_s, salt_b64, derived_b64 = stored.split("$")
        if algorithm != _ALGORITHM:
            return False
        iterations = int(iterations_s)
        salt = b64decode(salt_b64)
        expected = b64decode(derived_b64)
    except (ValueError, TypeError):
        return False
    candidate = pbkdf2_hmac(_HASH_NAME, password.encode("utf-8"), salt, iterations, len(expected))
    return hmac.compare_digest(candidate, expected)


@dataclass
class _Attempts:
    count: int = 0
    locked_until: float = 0.0


class LoginRateLimiter:
    """In-memory per-key failed-login lockout.

    After ``max_attempts`` consecutive failures a key is locked for
    ``lockout_seconds``. State is process-local: it resets on restart and is
    per-worker, which is adequate for a single-admin panel. Back it with a
    shared store (e.g. Redis) if the admin runs behind multiple workers.
    """

    def __init__(self, max_attempts: int = 5, lockout_seconds: float = 900.0) -> None:
        self._max_attempts = max_attempts
        self._lockout_seconds = lockout_seconds
        self._attempts: dict[str, _Attempts] = {}

    def is_locked(self, key: str) -> bool:
        record = self._attempts.get(key)
        if record is None or not record.locked_until:
            return False
        if record.locked_until > time.monotonic():
            return True
        # Lock expired: clear it so the caller starts fresh.
        self._attempts.pop(key, None)
        return False

    def record_failure(self, key: str) -> None:
        record = self._attempts.setdefault(key, _Attempts())
        record.count += 1
        if record.count >= self._max_attempts:
            record.locked_until = time.monotonic() + self._lockout_seconds

    def reset(self, key: str) -> None:
        self._attempts.pop(key, None)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: python -m app.security <password>", file=sys.stderr)
        raise SystemExit(2)
    print(hash_password(sys.argv[1]))

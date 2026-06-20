"""Tests for admin authentication: password hashing, lockout, login flow."""

import pytest

from app.admin import auth as admin_auth
from app.admin.auth import AdminAuth
from app.security import LoginRateLimiter, hash_password, verify_password


class TestPasswordHashing:
    def test_roundtrip(self):
        stored = hash_password("correct horse")
        assert verify_password("correct horse", stored) is True

    def test_rejects_wrong_password(self):
        stored = hash_password("correct horse")
        assert verify_password("battery staple", stored) is False

    def test_hash_is_salted(self):
        # Same password hashes differently (random salt) but both verify.
        a = hash_password("same")
        b = hash_password("same")
        assert a != b
        assert verify_password("same", a)
        assert verify_password("same", b)

    def test_hash_is_not_plaintext(self):
        stored = hash_password("secret")
        assert "secret" not in stored
        assert stored.startswith("pbkdf2_sha256$")

    @pytest.mark.parametrize("bad", ["", "not-a-hash", "pbkdf2_sha256$only$two", "md5$1$a$b"])
    def test_malformed_hash_returns_false(self, bad):
        assert verify_password("whatever", bad) is False


class TestLoginRateLimiter:
    def test_not_locked_initially(self):
        limiter = LoginRateLimiter(max_attempts=3, lockout_seconds=60)
        assert limiter.is_locked("ip") is False

    def test_locks_after_max_attempts(self):
        limiter = LoginRateLimiter(max_attempts=3, lockout_seconds=60)
        for _ in range(3):
            limiter.record_failure("ip")
        assert limiter.is_locked("ip") is True

    def test_below_threshold_not_locked(self):
        limiter = LoginRateLimiter(max_attempts=3, lockout_seconds=60)
        limiter.record_failure("ip")
        limiter.record_failure("ip")
        assert limiter.is_locked("ip") is False

    def test_reset_clears_failures(self):
        limiter = LoginRateLimiter(max_attempts=3, lockout_seconds=60)
        for _ in range(3):
            limiter.record_failure("ip")
        limiter.reset("ip")
        assert limiter.is_locked("ip") is False

    def test_lock_expires(self):
        # Zero lockout window → the lock is already expired on next check.
        limiter = LoginRateLimiter(max_attempts=1, lockout_seconds=0)
        limiter.record_failure("ip")
        assert limiter.is_locked("ip") is False

    def test_keys_are_independent(self):
        limiter = LoginRateLimiter(max_attempts=1, lockout_seconds=60)
        limiter.record_failure("ip-a")
        assert limiter.is_locked("ip-a") is True
        assert limiter.is_locked("ip-b") is False


class _FakeClient:
    def __init__(self, host: str) -> None:
        self.host = host


class _FakeRequest:
    """Minimal stand-in for starlette.Request used by AdminAuth.login."""

    def __init__(self, form: dict[str, str], host: str = "10.0.0.1") -> None:
        self._form = form
        self.session: dict[str, object] = {}
        self.client = _FakeClient(host)

    async def form(self) -> dict[str, str]:
        return self._form


class TestAdminLogin:
    @pytest.fixture(autouse=True)
    def _clear_limiter(self):
        # The backend keeps a module-level limiter; isolate each test.
        admin_auth._rate_limiter._attempts.clear()
        yield
        admin_auth._rate_limiter._attempts.clear()

    @pytest.fixture
    def backend(self) -> AdminAuth:
        return AdminAuth(secret_key="test-secret")

    async def test_valid_credentials_authenticate(self, backend):
        request = _FakeRequest({"username": "admin", "password": "test"})
        assert await backend.login(request) is True
        assert request.session.get("authenticated") is True

    async def test_wrong_password_rejected(self, backend):
        request = _FakeRequest({"username": "admin", "password": "wrong"})
        assert await backend.login(request) is False
        assert request.session.get("authenticated") is None

    async def test_wrong_username_rejected(self, backend):
        request = _FakeRequest({"username": "root", "password": "test"})
        assert await backend.login(request) is False

    async def test_missing_fields_rejected(self, backend):
        assert await backend.login(_FakeRequest({})) is False

    async def test_lockout_blocks_even_correct_password(self, backend):
        host = "10.0.0.99"
        for _ in range(5):
            await backend.login(_FakeRequest({"username": "admin", "password": "x"}, host=host))
        # Correct credentials from the locked IP are still refused.
        good = _FakeRequest({"username": "admin", "password": "test"}, host=host)
        assert await backend.login(good) is False
        assert good.session.get("authenticated") is None

"""Authentication backend for SQLAdmin."""

import hmac
import logging

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.security import LoginRateLimiter, verify_password

logger = logging.getLogger(__name__)

# Process-local lockout: 5 failed attempts per client IP → 15 minute lock.
_rate_limiter = LoginRateLimiter(max_attempts=5, lockout_seconds=900.0)


def _client_key(request: Request) -> str:
    """Identify the caller for rate limiting (client IP, or a fallback)."""
    return request.client.host if request.client else "unknown"


class AdminAuth(AuthenticationBackend):
    """Username/password authentication for the admin panel."""

    async def login(self, request: Request) -> bool:
        """Validate login credentials, with hashing and a failed-attempt lock."""
        key = _client_key(request)
        if _rate_limiter.is_locked(key):
            logger.warning("Admin login blocked: too many attempts (client=%s)", key)
            return False

        form = await request.form()
        username = str(form.get("username") or "")
        password = str(form.get("password") or "")

        # compare_digest on the username avoids leaking it via timing; the
        # password is checked against a stored hash (also constant-time).
        username_ok = hmac.compare_digest(username, settings.ADMIN_USERNAME)
        password_ok = verify_password(password, settings.ADMIN_PASSWORD_HASH)
        if username_ok and password_ok:
            _rate_limiter.reset(key)
            request.session.update({"authenticated": True})
            return True

        _rate_limiter.record_failure(key)
        logger.warning("Admin login failed (client=%s)", key)
        return False

    async def logout(self, request: Request) -> bool:
        """Clear session on logout."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        """Check if user is authenticated."""
        if not request.session.get("authenticated"):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True

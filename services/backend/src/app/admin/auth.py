"""Authentication backend for SQLAdmin."""

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings


class AdminAuth(AuthenticationBackend):
    """Simple username/password authentication for admin panel."""

    async def login(self, request: Request) -> bool:
        """Validate login credentials."""
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"authenticated": True})
            return True

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

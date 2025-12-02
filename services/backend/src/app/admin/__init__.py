"""Admin panel configuration using SQLAdmin."""

from sqladmin import Admin

from app.admin.auth import AdminAuth
from app.admin.views import (
    ContactAdmin,
    ContactTranslationAdmin,
    ProjectAdmin,
    ProjectTranslationAdmin,
    ResumeAdmin,
    StackAdmin,
    TestimonialAdmin,
    TestimonialTranslationAdmin,
    WorkExperienceAdmin,
    WorkExperienceTranslationAdmin,
)
from app.config import settings


def setup_admin(app, engine) -> Admin:  # type: ignore[no-untyped-def]
    """Configure and return SQLAdmin instance."""
    authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)

    admin = Admin(
        app,
        engine,
        authentication_backend=authentication_backend,
        title="Personal Site Admin",
    )

    admin.add_view(ProjectAdmin)
    admin.add_view(ProjectTranslationAdmin)
    admin.add_view(WorkExperienceAdmin)
    admin.add_view(WorkExperienceTranslationAdmin)
    admin.add_view(TestimonialAdmin)
    admin.add_view(TestimonialTranslationAdmin)
    admin.add_view(ContactAdmin)
    admin.add_view(ContactTranslationAdmin)
    admin.add_view(StackAdmin)
    admin.add_view(ResumeAdmin)

    return admin


__all__ = ["setup_admin"]

import uuid

from sqlalchemy import String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import TimestampMixin


class SiteContent(Base, TimestampMixin):
    """
    Homepage hero and about copy.

    A singleton-per-language table: one row per ``language_code``. Kept flat
    (no parent/translation split) because there is exactly one site, unlike the
    collection models (projects, testimonials, ...). ``about_body`` holds
    paragraphs separated by newlines; the frontend splits them.
    """

    __tablename__ = "site_content"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    hero_eyebrow: Mapped[str] = mapped_column(String, nullable=False, default="")
    hero_greeting: Mapped[str] = mapped_column(String, nullable=False, default="")
    hero_subtitle: Mapped[str] = mapped_column(String, nullable=False, default="")
    about_title: Mapped[str] = mapped_column(String, nullable=False, default="")
    about_body: Mapped[str] = mapped_column(Text, nullable=False, default="")

    def __repr__(self) -> str:
        return f"<SiteContent {self.language_code}>"

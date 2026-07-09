import uuid

from sqlalchemy import Boolean, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import TimestampMixin


class Offer(Base, TimestampMixin):
    """
    Homepage offer block (e.g. a productized service).

    Singleton-per-language like :class:`SiteContent`: one row per
    ``language_code``. Hidden by default (``is_visible=False``) so the block can
    be drafted in /admin and switched on or off without a deploy. ``body`` holds
    paragraphs and ``bullets`` holds list items, both newline-separated; the
    frontend splits them. ``cta_note`` is a short line rendered right above the
    CTA button.
    """

    __tablename__ = "offer"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    eyebrow: Mapped[str] = mapped_column(String, nullable=False, default="")
    title: Mapped[str] = mapped_column(String, nullable=False, default="")
    subtitle: Mapped[str] = mapped_column(String, nullable=False, default="")
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    bullets: Mapped[str] = mapped_column(Text, nullable=False, default="")
    price: Mapped[str] = mapped_column(String, nullable=False, default="")
    timeline: Mapped[str] = mapped_column(String, nullable=False, default="")
    cta_note: Mapped[str] = mapped_column(String, nullable=False, default="")
    cta_label: Mapped[str] = mapped_column(String, nullable=False, default="")
    cta_href: Mapped[str] = mapped_column(String, nullable=False, default="")

    def __repr__(self) -> str:
        return f"<Offer {self.language_code} visible={self.is_visible}>"

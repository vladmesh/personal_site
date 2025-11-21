import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy import String, Date, ForeignKey, Text, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin


class Testimonial(Base, TimestampMixin):
    """
    Testimonial (Review) model.
    Stores language-neutral data.
    """

    __tablename__ = "testimonials"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    author_name: Mapped[str] = mapped_column(String, nullable=False)
    author_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    author_avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    # Relationships
    translations: Mapped[List["TestimonialTranslation"]] = relationship(
        back_populates="testimonial", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Testimonial from {self.author_name}>"


class TestimonialTranslation(Base):
    """
    Testimonial Translation model.
    Stores language-specific data.
    """

    __tablename__ = "testimonial_translations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    testimonial_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("testimonials.id"), nullable=False
    )
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    author_position: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    testimonial: Mapped[Testimonial] = relationship(back_populates="translations")

    # Constraints
    __table_args__ = (
        UniqueConstraint("testimonial_id", "language_code", name="uq_testimonial_translation_lang"),
    )

    def __repr__(self) -> str:
        return f"<TestimonialTranslation {self.language_code} for {self.testimonial_id}>"

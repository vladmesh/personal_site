import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin


class Contact(Base, TimestampMixin):
    """
    Contact model.
    Stores contact information.
    """

    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String, nullable=False)  # e.g., email, linkedin
    value: Mapped[str] = mapped_column(String, nullable=False)
    icon: Mapped[str | None] = mapped_column(String, nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    translations: Mapped[list["ContactTranslation"]] = relationship(
        back_populates="contact", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Contact {self.type}: {self.value}>"


class ContactTranslation(Base):
    """
    Contact Translation model.
    Stores language-specific labels for contacts.
    """

    __tablename__ = "contact_translations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("contacts.id"), nullable=False
    )
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    label: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationships
    contact: Mapped[Contact] = relationship(back_populates="translations")

    # Constraints
    __table_args__ = (
        UniqueConstraint("contact_id", "language_code", name="uq_contact_translation_lang"),
    )

    def __repr__(self) -> str:
        return f"<ContactTranslation {self.language_code} for {self.contact_id}>"

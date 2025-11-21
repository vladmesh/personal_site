import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy import String, Boolean, Date, ForeignKey, Text, Uuid, UniqueConstraint, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin
from app.models.stack import Stack

# Association table for WorkExperience <-> Stack
work_experience_stacks = Table(
    "work_experience_stacks",
    Base.metadata,
    Column("work_experience_id", Uuid(as_uuid=True), ForeignKey("work_experiences.id"), primary_key=True),
    Column("stack_id", Uuid(as_uuid=True), ForeignKey("stacks.id"), primary_key=True),
)


class WorkExperience(Base, TimestampMixin):
    """
    Work Experience model.
    Stores language-neutral data.
    """

    __tablename__ = "work_experiences"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    company_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    translations: Mapped[List["WorkExperienceTranslation"]] = relationship(
        back_populates="work_experience", cascade="all, delete-orphan", lazy="selectin"
    )
    stacks: Mapped[List[Stack]] = relationship(
        secondary=work_experience_stacks, lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<WorkExperience {self.company_name}>"


class WorkExperienceTranslation(Base):
    """
    Work Experience Translation model.
    Stores language-specific data.
    """

    __tablename__ = "work_experience_translations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    work_experience_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("work_experiences.id"), nullable=False
    )
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    work_experience: Mapped[WorkExperience] = relationship(back_populates="translations")

    # Constraints
    __table_args__ = (
        UniqueConstraint("work_experience_id", "language_code", name="uq_work_exp_translation_lang"),
    )

    def __repr__(self) -> str:
        return f"<WorkExperienceTranslation {self.language_code} for {self.work_experience_id}>"

import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy import String, Boolean, Date, ForeignKey, Text, Uuid, UniqueConstraint, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin
from app.models.stack import Stack

# Association table for Project <-> Stack
project_stacks = Table(
    "project_stacks",
    Base.metadata,
    Column("project_id", Uuid(as_uuid=True), ForeignKey("projects.id"), primary_key=True),
    Column("stack_id", Uuid(as_uuid=True), ForeignKey("stacks.id"), primary_key=True),
)


class Project(Base, TimestampMixin):
    """
    Project model.
    Stores language-neutral data.
    """

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    link: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    repo_link: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    translations: Mapped[List["ProjectTranslation"]] = relationship(
        back_populates="project", cascade="all, delete-orphan", lazy="selectin"
    )
    stacks: Mapped[List[Stack]] = relationship(
        secondary=project_stacks, lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Project {self.slug}>"


class ProjectTranslation(Base):
    """
    Project Translation model.
    Stores language-specific data.
    """

    __tablename__ = "project_translations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id"), nullable=False
    )
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    project: Mapped[Project] = relationship(back_populates="translations")

    # Constraints
    __table_args__ = (
        UniqueConstraint("project_id", "language_code", name="uq_project_translation_lang"),
    )

    def __repr__(self) -> str:
        return f"<ProjectTranslation {self.language_code} for {self.project_id}>"

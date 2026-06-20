# ruff: noqa: E501

"""squashed schema baseline

Revision ID: 0001_squash_schema
Revises:
Create Date: 2026-06-20 12:30:00.000000

Single schema-only baseline that collapses the original initial_schema,
the testimonials.kind column, and the site_content table. No data: content is
seeded by the example-seed migration and edited via /admin.

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_squash_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "contacts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("icon", sa.String(), nullable=True),
        sa.Column("is_visible", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("link", sa.String(), nullable=True),
        sa.Column("repo_link", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_projects_slug"), "projects", ["slug"], unique=True)
    op.create_table(
        "resumes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stacks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("icon_url", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("proficiency", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stacks_name"), "stacks", ["name"], unique=True)
    op.create_table(
        "testimonials",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("author_name", sa.String(), nullable=False),
        sa.Column("author_url", sa.String(), nullable=True),
        sa.Column("author_avatar_url", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("kind", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "work_experiences",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("company_name", sa.String(), nullable=False),
        sa.Column("company_url", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contact_translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("contact_id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("label", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["contact_id"], ["contacts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("contact_id", "language_code", name="uq_contact_translation_lang"),
    )
    op.create_table(
        "project_stacks",
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("stack_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["stack_id"], ["stacks.id"]),
        sa.PrimaryKeyConstraint("project_id", "stack_id"),
    )
    op.create_table(
        "project_translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("role", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "language_code", name="uq_project_translation_lang"),
    )
    op.create_table(
        "testimonial_translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("testimonial_id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("author_position", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["testimonial_id"], ["testimonials.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("testimonial_id", "language_code", name="uq_testimonial_translation_lang"),
    )
    op.create_table(
        "work_experience_stacks",
        sa.Column("work_experience_id", sa.Uuid(), nullable=False),
        sa.Column("stack_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["stack_id"], ["stacks.id"]),
        sa.ForeignKeyConstraint(["work_experience_id"], ["work_experiences.id"]),
        sa.PrimaryKeyConstraint("work_experience_id", "stack_id"),
    )
    op.create_table(
        "work_experience_translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("work_experience_id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("position", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("location", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["work_experience_id"], ["work_experiences.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("work_experience_id", "language_code", name="uq_work_exp_translation_lang"),
    )
    op.create_table(
        "site_content",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("hero_eyebrow", sa.String(), server_default="", nullable=False),
        sa.Column("hero_greeting", sa.String(), server_default="", nullable=False),
        sa.Column("hero_subtitle", sa.String(), server_default="", nullable=False),
        sa.Column("about_title", sa.String(), server_default="", nullable=False),
        sa.Column("about_body", sa.Text(), server_default="", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("language_code", name="uq_site_content_language_code"),
    )


def downgrade() -> None:
    op.drop_table("site_content")
    op.drop_table("work_experience_translations")
    op.drop_table("work_experience_stacks")
    op.drop_table("testimonial_translations")
    op.drop_table("project_translations")
    op.drop_table("project_stacks")
    op.drop_table("contact_translations")
    op.drop_table("work_experiences")
    op.drop_table("testimonials")
    op.drop_index(op.f("ix_stacks_name"), table_name="stacks")
    op.drop_table("stacks")
    op.drop_table("resumes")
    op.drop_index(op.f("ix_projects_slug"), table_name="projects")
    op.drop_table("projects")
    op.drop_table("contacts")

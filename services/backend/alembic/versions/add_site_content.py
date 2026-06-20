"""add site_content table for homepage hero/about copy

Revision ID: site_content_003
Revises: seed_profile_content_002
Create Date: 2026-06-20 01:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "site_content_003"
down_revision: str | None = "seed_profile_content_002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "site_content",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("hero_eyebrow", sa.String(), server_default="", nullable=False),
        sa.Column("hero_greeting", sa.String(), server_default="", nullable=False),
        sa.Column("hero_subtitle", sa.String(), server_default="", nullable=False),
        sa.Column("about_title", sa.String(), server_default="", nullable=False),
        sa.Column("about_body", sa.Text(), server_default="", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("language_code", name="uq_site_content_language_code"),
    )


def downgrade() -> None:
    op.drop_table("site_content")

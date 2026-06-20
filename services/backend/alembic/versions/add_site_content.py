# ruff: noqa: E501

"""add site_content table for homepage hero/about copy

Revision ID: site_content_003
Revises: seed_profile_content_002
Create Date: 2026-06-20 01:30:00.000000

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.sql import column, table

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

    # Placeholder hero/about copy so a fresh template DB renders something.
    # Edit in /admin (Site Content); prod is already migrated so this won't run there.
    site_content = table(
        "site_content",
        column("id", sa.Uuid),
        column("language_code", sa.String),
        column("hero_eyebrow", sa.String),
        column("hero_greeting", sa.String),
        column("hero_subtitle", sa.String),
        column("about_title", sa.String),
        column("about_body", sa.Text),
    )
    op.bulk_insert(
        site_content,
        [
            {
                "id": uuid.uuid4(),
                "language_code": "en",
                "hero_eyebrow": "Backend / AI",
                "hero_greeting": "Hi, I'm Your Name",
                "hero_subtitle": "Backend developer and mentor. Edit this copy in /admin.",
                "about_title": "About",
                "about_body": "Placeholder about text. Edit it in the admin panel under Site Content.",
            },
            {
                "id": uuid.uuid4(),
                "language_code": "ru",
                "hero_eyebrow": "Backend / AI",
                "hero_greeting": "Привет, я Ваше Имя",
                "hero_subtitle": "Backend-разработчик и ментор. Отредактируйте текст в /admin.",
                "about_title": "Обо мне",
                "about_body": "Заглушка для блока «обо мне». Отредактируйте её в админке, раздел Site Content.",
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("site_content")

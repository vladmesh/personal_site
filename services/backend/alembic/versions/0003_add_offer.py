# ruff: noqa: E501

"""add offer block

Revision ID: 0003_add_offer
Revises: 0002_example_seed
Create Date: 2026-06-20 16:00:00.000000

Homepage offer block: a singleton-per-language table that mirrors site_content.
Hidden by default (is_visible=false) so the block can be drafted in /admin and
switched on without a deploy. Seeds placeholder rows for en/ru.

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003_add_offer"
down_revision: str | None = "0002_example_seed"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "offer",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column("is_visible", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("eyebrow", sa.String(), server_default="", nullable=False),
        sa.Column("title", sa.String(), server_default="", nullable=False),
        sa.Column("subtitle", sa.String(), server_default="", nullable=False),
        sa.Column("body", sa.Text(), server_default="", nullable=False),
        sa.Column("bullets", sa.Text(), server_default="", nullable=False),
        sa.Column("price", sa.String(), server_default="", nullable=False),
        sa.Column("timeline", sa.String(), server_default="", nullable=False),
        sa.Column("cta_label", sa.String(), server_default="", nullable=False),
        sa.Column("cta_href", sa.String(), server_default="", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("language_code", name="uq_offer_language_code"),
    )

    offer = table(
        "offer",
        column("id", sa.Uuid),
        column("language_code", sa.String),
        column("is_visible", sa.Boolean),
        column("eyebrow", sa.String),
        column("title", sa.String),
        column("subtitle", sa.String),
        column("body", sa.Text),
        column("bullets", sa.Text),
        column("price", sa.String),
        column("timeline", sa.String),
        column("cta_label", sa.String),
        column("cta_href", sa.String),
    )
    op.bulk_insert(
        offer,
        [
            {
                "id": uuid.uuid4(),
                "language_code": "en",
                "is_visible": False,
                "eyebrow": "Offer",
                "title": "What I can do for you",
                "subtitle": "A one-line pitch for your productized service. Edit it in /admin, then flip visibility on.",
                "body": "Describe the offer in a sentence or two.\nHidden by default — set is_visible to show this block.",
                "bullets": "What's included, item one\nWhat's included, item two\nWhat's included, item three",
                "price": "Fixed price",
                "timeline": "1–2 weeks",
                "cta_label": "Get in touch",
                "cta_href": "",
            },
            {
                "id": uuid.uuid4(),
                "language_code": "ru",
                "is_visible": False,
                "eyebrow": "Предложение",
                "title": "Чем могу помочь",
                "subtitle": "Одна строка про ваш продукт-услугу. Отредактируйте в /admin и включите видимость.",
                "body": "Опишите предложение в паре предложений.\nПо умолчанию скрыто — поставьте is_visible, чтобы показать блок.",
                "bullets": "Что входит, пункт один\nЧто входит, пункт два\nЧто входит, пункт три",
                "price": "Фикс-цена",
                "timeline": "1–2 недели",
                "cta_label": "Связаться",
                "cta_href": "",
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("offer")

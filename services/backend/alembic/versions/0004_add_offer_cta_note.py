# ruff: noqa: E501

"""add offer cta_note

Revision ID: 0004_add_offer_cta_note
Revises: 0003_add_offer
Create Date: 2026-07-09 14:30:00.000000

Short line rendered right above the offer CTA button, e.g. an invitation to
reach out with questions before committing.

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0004_add_offer_cta_note"
down_revision: str | None = "0003_add_offer"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("offer", sa.Column("cta_note", sa.String(), server_default="", nullable=False))


def downgrade() -> None:
    op.drop_column("offer", "cta_note")

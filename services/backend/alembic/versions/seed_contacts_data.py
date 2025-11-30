"""seed contacts data

Revision ID: seed_contacts_001
Revises: 678705771ddf
Create Date: 2025-11-22 03:36:00.000000

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "seed_contacts_001"
down_revision: str | None = "678705771ddf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add contact seed data from frontend links.ts"""

    # Define tables for bulk insert
    contacts = table(
        "contacts",
        column("id", sa.Uuid),
        column("type", sa.String),
        column("value", sa.String),
        column("icon", sa.String),
        column("is_visible", sa.Boolean),
        column("sort_order", sa.Integer),
    )

    contact_translations = table(
        "contact_translations",
        column("id", sa.Uuid),
        column("contact_id", sa.Uuid),
        column("language_code", sa.String),
        column("label", sa.String),
    )

    # Generate UUIDs for contacts
    email_id = uuid.uuid4()
    telegram_id = uuid.uuid4()
    github_id = uuid.uuid4()
    github_repo_id = uuid.uuid4()
    linkedin_id = uuid.uuid4()
    phone_id = uuid.uuid4()
    whatsapp_id = uuid.uuid4()

    # Insert contacts
    op.bulk_insert(
        contacts,
        [
            {
                "id": email_id,
                "type": "email",
                "value": "vladmesh.dev@gmail.com",
                "icon": "email",
                "is_visible": True,
                "sort_order": 1,
            },
            {
                "id": telegram_id,
                "type": "telegram",
                "value": "https://t.me/vladislav_meshk",
                "icon": "telegram",
                "is_visible": True,
                "sort_order": 2,
            },
            {
                "id": github_id,
                "type": "github",
                "value": "https://github.com/vladmesh",
                "icon": "github",
                "is_visible": True,
                "sort_order": 3,
            },
            {
                "id": github_repo_id,
                "type": "github_repo",
                "value": "https://github.com/vladmesh/personal-site",
                "icon": "github",
                "is_visible": True,
                "sort_order": 4,
            },
            {
                "id": linkedin_id,
                "type": "linkedin",
                "value": "https://www.linkedin.com/in/vladmesh",
                "icon": "linkedin",
                "is_visible": True,
                "sort_order": 5,
            },
            {
                "id": phone_id,
                "type": "phone",
                "value": "+79000000000",
                "icon": "phone",
                "is_visible": False,  # Might want to keep phone private
                "sort_order": 6,
            },
            {
                "id": whatsapp_id,
                "type": "whatsapp",
                "value": "https://wa.me/79000000000",
                "icon": "whatsapp",
                "is_visible": False,
                "sort_order": 7,
            },
        ],
    )

    # Insert translations
    op.bulk_insert(
        contact_translations,
        [
            # Email
            {"id": uuid.uuid4(), "contact_id": email_id, "language_code": "en", "label": "Email"},
            {"id": uuid.uuid4(), "contact_id": email_id, "language_code": "ru", "label": "Email"},
            # Telegram
            {
                "id": uuid.uuid4(),
                "contact_id": telegram_id,
                "language_code": "en",
                "label": "Telegram",
            },
            {
                "id": uuid.uuid4(),
                "contact_id": telegram_id,
                "language_code": "ru",
                "label": "Telegram",
            },
            # GitHub
            {"id": uuid.uuid4(), "contact_id": github_id, "language_code": "en", "label": "GitHub"},
            {"id": uuid.uuid4(), "contact_id": github_id, "language_code": "ru", "label": "GitHub"},
            # GitHub Repo
            {
                "id": uuid.uuid4(),
                "contact_id": github_repo_id,
                "language_code": "en",
                "label": "Source Code",
            },
            {
                "id": uuid.uuid4(),
                "contact_id": github_repo_id,
                "language_code": "ru",
                "label": "Исходный код",
            },
            # LinkedIn
            {
                "id": uuid.uuid4(),
                "contact_id": linkedin_id,
                "language_code": "en",
                "label": "LinkedIn",
            },
            {
                "id": uuid.uuid4(),
                "contact_id": linkedin_id,
                "language_code": "ru",
                "label": "LinkedIn",
            },
            # Phone
            {"id": uuid.uuid4(), "contact_id": phone_id, "language_code": "en", "label": "Phone"},
            {"id": uuid.uuid4(), "contact_id": phone_id, "language_code": "ru", "label": "Телефон"},
            # WhatsApp
            {
                "id": uuid.uuid4(),
                "contact_id": whatsapp_id,
                "language_code": "en",
                "label": "WhatsApp",
            },
            {
                "id": uuid.uuid4(),
                "contact_id": whatsapp_id,
                "language_code": "ru",
                "label": "WhatsApp",
            },
        ],
    )


def downgrade() -> None:
    """Remove contact seed data"""
    op.execute("DELETE FROM contact_translations")
    op.execute("DELETE FROM contacts")

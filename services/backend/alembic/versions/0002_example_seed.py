# ruff: noqa: E501

"""example seed data (placeholders)

Revision ID: 0002_example_seed
Revises: 0001_squash_schema
Create Date: 2026-06-20 12:31:00.000000

Placeholder demo content so a fresh template database renders a populated site.
All of it is editable in /admin; replace it with your own data.

"""

import uuid
from collections.abc import Sequence
from datetime import UTC, date, datetime

import sqlalchemy as sa
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002_example_seed"
down_revision: str | None = "0001_squash_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
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
    stacks = table(
        "stacks",
        column("id", sa.Uuid),
        column("name", sa.String),
        column("icon_url", sa.String),
        column("category", sa.String),
        column("proficiency", sa.Integer),
    )
    work_experiences = table(
        "work_experiences",
        column("id", sa.Uuid),
        column("company_name", sa.String),
        column("company_url", sa.String),
        column("start_date", sa.Date),
        column("end_date", sa.Date),
        column("is_current", sa.Boolean),
    )
    work_experience_translations = table(
        "work_experience_translations",
        column("id", sa.Uuid),
        column("work_experience_id", sa.Uuid),
        column("language_code", sa.String),
        column("position", sa.String),
        column("description", sa.Text),
        column("location", sa.String),
    )
    work_experience_stacks = table(
        "work_experience_stacks",
        column("work_experience_id", sa.Uuid),
        column("stack_id", sa.Uuid),
    )
    projects = table(
        "projects",
        column("id", sa.Uuid),
        column("slug", sa.String),
        column("link", sa.String),
        column("repo_link", sa.String),
        column("start_date", sa.Date),
        column("end_date", sa.Date),
        column("is_featured", sa.Boolean),
    )
    project_translations = table(
        "project_translations",
        column("id", sa.Uuid),
        column("project_id", sa.Uuid),
        column("language_code", sa.String),
        column("title", sa.String),
        column("description", sa.Text),
        column("role", sa.String),
    )
    project_stacks = table(
        "project_stacks",
        column("project_id", sa.Uuid),
        column("stack_id", sa.Uuid),
    )
    testimonials = table(
        "testimonials",
        column("id", sa.Uuid),
        column("author_name", sa.String),
        column("author_url", sa.String),
        column("author_avatar_url", sa.String),
        column("kind", sa.String),
        column("date", sa.Date),
    )
    testimonial_translations = table(
        "testimonial_translations",
        column("id", sa.Uuid),
        column("testimonial_id", sa.Uuid),
        column("language_code", sa.String),
        column("author_position", sa.String),
        column("content", sa.Text),
    )
    resumes = table(
        "resumes",
        column("id", sa.Uuid),
        column("language_code", sa.String),
        column("file_path", sa.String),
        column("generated_at", sa.DateTime(timezone=True)),
        column("is_active", sa.Boolean),
    )
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

    # --- Contacts ---
    contact_rows = [
        ("email", "you@example.com", "email", True, 1, "Email", "Email"),
        ("telegram", "https://t.me/yourhandle", "telegram", True, 2, "Telegram", "Telegram"),
        ("github", "https://github.com/your-org", "github", True, 3, "GitHub", "GitHub"),
        ("github_repo", "https://github.com/your-org/personal-site", "github", True, 4, "Source Code", "Исходный код"),
        ("linkedin", "https://www.linkedin.com/in/your-handle", "linkedin", True, 5, "LinkedIn", "LinkedIn"),
        ("phone", "+10000000000", "phone", False, 6, "Phone", "Телефон"),
        ("whatsapp", "https://wa.me/10000000000", "whatsapp", False, 7, "WhatsApp", "WhatsApp"),
    ]
    contact_records = []
    contact_translation_records = []
    for type_, value, icon, visible, order, label_en, label_ru in contact_rows:
        cid = uuid.uuid4()
        contact_records.append(
            {"id": cid, "type": type_, "value": value, "icon": icon, "is_visible": visible, "sort_order": order}
        )
        contact_translation_records.append({"id": uuid.uuid4(), "contact_id": cid, "language_code": "en", "label": label_en})
        contact_translation_records.append({"id": uuid.uuid4(), "contact_id": cid, "language_code": "ru", "label": label_ru})
    op.bulk_insert(contacts, contact_records)
    op.bulk_insert(contact_translations, contact_translation_records)

    # --- Stacks (generic tech list) ---
    stack_entries = [
        ("Python", "Backend"),
        ("FastAPI", "Backend"),
        ("Django", "Backend"),
        ("Node.js", "Backend"),
        ("REST", "Backend"),
        ("SQLAlchemy", "Backend"),
        ("RabbitMQ", "Backend"),
        ("LangChain", "Data & AI"),
        ("OpenAI API", "Data & AI"),
        ("PostgreSQL", "Data & AI"),
        ("Redis", "Data & AI"),
        ("Airflow", "Data & AI"),
        ("Docker", "DevOps"),
        ("Kubernetes", "DevOps"),
        ("Terraform", "DevOps"),
        ("GitHub Actions", "DevOps"),
        ("Grafana", "DevOps"),
        ("Team Leadership", "Communication"),
        ("Roadmapping", "Communication"),
        ("Tech Writing", "Communication"),
    ]
    stack_records = [
        {"id": uuid.uuid4(), "name": name, "icon_url": None, "category": category, "proficiency": None}
        for name, category in stack_entries
    ]
    op.bulk_insert(stacks, stack_records)
    stack_ids = {r["name"]: r["id"] for r in stack_records}

    # --- Work experience ---
    experience_entries = [
        {
            "id": uuid.uuid4(),
            "company_name": "Acme Corp",
            "company_url": "https://example.com",
            "start_date": date(2022, 1, 1),
            "end_date": date(2024, 12, 31),
            "is_current": False,
            "translations": [
                {"language_code": "en", "position": "Senior Backend Engineer", "description": "Led backend development for a SaaS platform.\nDesigned microservices with FastAPI, SQLAlchemy, and PostgreSQL.\nSet up CI/CD and observability. (Placeholder, edit in /admin.)", "location": "Remote"},
                {"language_code": "ru", "position": "Старший backend-инженер", "description": "Вёл разработку бэкенда SaaS-платформы.\nПроектировал микросервисы на FastAPI, SQLAlchemy и PostgreSQL.\nНастроил CI/CD и мониторинг. (Заглушка, отредактируйте в /admin.)", "location": "Удалённо"},
            ],
            "stacks": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Docker"],
        },
        {
            "id": uuid.uuid4(),
            "company_name": "Globex",
            "company_url": "https://example.com",
            "start_date": date(2019, 1, 1),
            "end_date": date(2021, 12, 31),
            "is_current": False,
            "translations": [
                {"language_code": "en", "position": "Backend Developer", "description": "Built and maintained REST APIs for a high-traffic service.\nOptimized database queries and caching.", "location": "Remote"},
                {"language_code": "ru", "position": "Backend-разработчик", "description": "Разрабатывал и поддерживал REST API для нагруженного сервиса.\nОптимизировал запросы к БД и кеширование.", "location": "Удалённо"},
            ],
            "stacks": ["Django", "Redis", "PostgreSQL"],
        },
    ]
    op.bulk_insert(
        work_experiences,
        [{k: e[k] for k in ("id", "company_name", "company_url", "start_date", "end_date", "is_current")} for e in experience_entries],
    )
    exp_translations = []
    exp_stack_links = []
    for e in experience_entries:
        for tr in e["translations"]:
            exp_translations.append({"id": uuid.uuid4(), "work_experience_id": e["id"], **tr})
        for sname in e["stacks"]:
            if stack_ids.get(sname):
                exp_stack_links.append({"work_experience_id": e["id"], "stack_id": stack_ids[sname]})
    op.bulk_insert(work_experience_translations, exp_translations)
    if exp_stack_links:
        op.bulk_insert(work_experience_stacks, exp_stack_links)

    # --- Projects ---
    project_entries = [
        {
            "id": uuid.uuid4(),
            "slug": "example-api",
            "link": None,
            "repo_link": "https://github.com/your-org/example-api",
            "start_date": date(2024, 1, 1),
            "end_date": None,
            "is_featured": True,
            "translations": [
                {"language_code": "en", "title": "Example REST API", "description": "A sample backend service with auth, background jobs, and a clean OpenAPI schema.\nReplace this with one of your own case studies in /admin.", "role": "Author"},
                {"language_code": "ru", "title": "Пример REST API", "description": "Демо backend-сервис с аутентификацией, фоновыми задачами и аккуратной OpenAPI-схемой.\nЗамените на свой кейс в /admin.", "role": "Автор"},
            ],
            "stacks": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        },
        {
            "id": uuid.uuid4(),
            "slug": "example-bot",
            "link": None,
            "repo_link": "https://github.com/your-org/example-bot",
            "start_date": date(2024, 3, 1),
            "end_date": None,
            "is_featured": False,
            "translations": [
                {"language_code": "en", "title": "Example Chat Bot", "description": "A messenger bot template with commands, inline keyboards, and a small API.\nSwap in your own project in /admin.", "role": "Author"},
                {"language_code": "ru", "title": "Пример чат-бота", "description": "Шаблон бота для мессенджера с командами, клавиатурами и небольшим API.\nЗамените на свой проект в /admin.", "role": "Автор"},
            ],
            "stacks": ["Python", "FastAPI", "Redis"],
        },
    ]
    op.bulk_insert(
        projects,
        [{k: e[k] for k in ("id", "slug", "link", "repo_link", "start_date", "end_date", "is_featured")} for e in project_entries],
    )
    proj_translations = []
    proj_stack_links = []
    for e in project_entries:
        for tr in e["translations"]:
            proj_translations.append({"id": uuid.uuid4(), "project_id": e["id"], **tr})
        for sname in e["stacks"]:
            if stack_ids.get(sname):
                proj_stack_links.append({"project_id": e["id"], "stack_id": stack_ids[sname]})
    op.bulk_insert(project_translations, proj_translations)
    if proj_stack_links:
        op.bulk_insert(project_stacks, proj_stack_links)

    # --- Testimonials ---
    testimonial_entries = [
        {
            "id": uuid.uuid4(),
            "author_name": "Jane Doe",
            "author_url": None,
            "author_avatar_url": None,
            "kind": "dev",
            "date": date(2024, 5, 1),
            "translations": [
                {"language_code": "en", "author_position": None, "content": "Sample testimonial. The project was delivered on time with clear communication. Replace this with a real quote in /admin."},
                {"language_code": "ru", "author_position": None, "content": "Пример отзыва. Проект сдан в срок, коммуникация была чёткой. Замените на настоящий отзыв в /admin."},
            ],
        },
        {
            "id": uuid.uuid4(),
            "author_name": "John Smith",
            "author_url": None,
            "author_avatar_url": None,
            "kind": "teacher",
            "date": date(2023, 6, 15),
            "translations": [
                {"language_code": "en", "author_position": None, "content": "Sample testimonial. A patient mentor with clear explanations. Replace this with a real quote in /admin."},
                {"language_code": "ru", "author_position": None, "content": "Пример отзыва. Терпеливый ментор, объясняет понятно. Замените на настоящий отзыв в /admin."},
            ],
        },
    ]
    op.bulk_insert(
        testimonials,
        [{k: e[k] for k in ("id", "author_name", "author_url", "author_avatar_url", "kind", "date")} for e in testimonial_entries],
    )
    testimonial_translation_rows = []
    for e in testimonial_entries:
        for tr in e["translations"]:
            testimonial_translation_rows.append({"id": uuid.uuid4(), "testimonial_id": e["id"], **tr})
    op.bulk_insert(testimonial_translations, testimonial_translation_rows)

    # --- Resumes ---
    now_ts = datetime.now(UTC)
    op.bulk_insert(
        resumes,
        [
            {"id": uuid.uuid4(), "language_code": "en", "file_path": "/cv/cv_en.pdf", "generated_at": now_ts, "is_active": True},
            {"id": uuid.uuid4(), "language_code": "ru", "file_path": "/cv/cv_ru.pdf", "generated_at": now_ts, "is_active": True},
        ],
    )

    # --- Site content (hero/about) ---
    op.bulk_insert(
        site_content,
        [
            {"id": uuid.uuid4(), "language_code": "en", "hero_eyebrow": "Backend / AI", "hero_greeting": "Hi, I'm Your Name", "hero_subtitle": "Backend developer and mentor. Edit this copy in /admin.", "about_title": "About", "about_body": "Placeholder about text. Edit it in the admin panel under Site Content."},
            {"id": uuid.uuid4(), "language_code": "ru", "hero_eyebrow": "Backend / AI", "hero_greeting": "Привет, я Ваше Имя", "hero_subtitle": "Backend-разработчик и ментор. Отредактируйте текст в /admin.", "about_title": "Обо мне", "about_body": "Заглушка для блока «обо мне». Отредактируйте её в админке, раздел Site Content."},
        ],
    )


def downgrade() -> None:
    # 0002 is the only seeder, so a blanket delete in FK-safe order is correct.
    for stmt in [
        "DELETE FROM contact_translations",
        "DELETE FROM contacts",
        "DELETE FROM work_experience_stacks",
        "DELETE FROM work_experience_translations",
        "DELETE FROM project_stacks",
        "DELETE FROM project_translations",
        "DELETE FROM testimonial_translations",
        "DELETE FROM work_experiences",
        "DELETE FROM projects",
        "DELETE FROM testimonials",
        "DELETE FROM resumes",
        "DELETE FROM stacks",
        "DELETE FROM site_content",
    ]:
        op.execute(stmt)

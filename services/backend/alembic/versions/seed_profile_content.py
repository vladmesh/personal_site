# ruff: noqa: E501

"""add testimonial kind and seed example profile content

Revision ID: seed_profile_content_002
Revises: seed_contacts_001
Create Date: 2025-11-22 05:30:00.000000

Seeds placeholder profile content (experience, projects, testimonials, skills,
resumes) so a fresh template database renders a populated demo. Replace it all
via /admin. The stack list is generic tech, kept as-is.

"""

import uuid
from collections.abc import Sequence
from datetime import UTC, date, datetime

import sqlalchemy as sa
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "seed_profile_content_002"
down_revision: str | None = "seed_contacts_001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _seed_uuid(key: str) -> uuid.UUID:
    """Deterministic UUID for seed data based on key."""
    return uuid.uuid5(uuid.NAMESPACE_DNS, f"profile-seed-{key}")


def upgrade() -> None:
    """Add testimonial kind column and seed example profile content."""
    op.add_column("testimonials", sa.Column("kind", sa.String(), nullable=True))

    # Table shortcuts
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

    # --- Seed stacks (generic tech list) ---
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
        {
            "id": _seed_uuid(f"stack-{name}"),
            "name": name,
            "icon_url": None,
            "category": category,
            "proficiency": None,
        }
        for name, category in stack_entries
    ]
    op.bulk_insert(stacks, stack_records)
    stack_ids = {record["name"]: record["id"] for record in stack_records}

    # --- Seed work experience (placeholder) ---
    experience_entries = [
        {
            "id": _seed_uuid("work-exp-1"),
            "company_name": "Acme Corp",
            "company_url": "https://example.com",
            "start_date": date(2022, 1, 1),
            "end_date": date(2024, 12, 31),
            "is_current": False,
            "translations": [
                {
                    "language_code": "en",
                    "position": "Senior Backend Engineer",
                    "description": "\n".join(
                        [
                            "Led backend development for a SaaS platform.",
                            "Designed microservices with FastAPI, SQLAlchemy, and PostgreSQL.",
                            "Set up CI/CD and observability. (Placeholder, edit in /admin.)",
                        ]
                    ),
                    "location": "Remote",
                },
                {
                    "language_code": "ru",
                    "position": "Старший backend-инженер",
                    "description": "\n".join(
                        [
                            "Вёл разработку бэкенда SaaS-платформы.",
                            "Проектировал микросервисы на FastAPI, SQLAlchemy и PostgreSQL.",
                            "Настроил CI/CD и мониторинг. (Заглушка, отредактируйте в /admin.)",
                        ]
                    ),
                    "location": "Удалённо",
                },
            ],
            "stacks": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Docker"],
        },
        {
            "id": _seed_uuid("work-exp-2"),
            "company_name": "Globex",
            "company_url": "https://example.com",
            "start_date": date(2019, 1, 1),
            "end_date": date(2021, 12, 31),
            "is_current": False,
            "translations": [
                {
                    "language_code": "en",
                    "position": "Backend Developer",
                    "description": "\n".join(
                        [
                            "Built and maintained REST APIs for a high-traffic service.",
                            "Optimized database queries and caching.",
                        ]
                    ),
                    "location": "Remote",
                },
                {
                    "language_code": "ru",
                    "position": "Backend-разработчик",
                    "description": "\n".join(
                        [
                            "Разрабатывал и поддерживал REST API для нагруженного сервиса.",
                            "Оптимизировал запросы к БД и кеширование.",
                        ]
                    ),
                    "location": "Удалённо",
                },
            ],
            "stacks": ["Django", "Redis", "PostgreSQL"],
        },
    ]

    op.bulk_insert(
        work_experiences,
        [
            {
                "id": entry["id"],
                "company_name": entry["company_name"],
                "company_url": entry["company_url"],
                "start_date": entry["start_date"],
                "end_date": entry["end_date"],
                "is_current": entry["is_current"],
            }
            for entry in experience_entries
        ],
    )

    experience_translations = []
    experience_stack_links = []
    for entry in experience_entries:
        for translation in entry["translations"]:
            experience_translations.append(
                {
                    "id": uuid.uuid4(),
                    "work_experience_id": entry["id"],
                    "language_code": translation["language_code"],
                    "position": translation["position"],
                    "description": translation["description"],
                    "location": translation["location"],
                }
            )
        for stack_name in entry["stacks"]:
            stack_id = stack_ids.get(stack_name)
            if stack_id:
                experience_stack_links.append(
                    {"work_experience_id": entry["id"], "stack_id": stack_id}
                )

    op.bulk_insert(work_experience_translations, experience_translations)
    if experience_stack_links:
        op.bulk_insert(work_experience_stacks, experience_stack_links)

    # --- Seed projects (placeholder) ---
    project_entries = [
        {
            "id": _seed_uuid("project-1"),
            "slug": "example-api",
            "link": None,
            "repo_link": "https://github.com/your-org/example-api",
            "start_date": date(2024, 1, 1),
            "end_date": None,
            "is_featured": True,
            "translations": [
                {
                    "language_code": "en",
                    "title": "Example REST API",
                    "description": "\n".join(
                        [
                            "A sample backend service with auth, background jobs, and a clean OpenAPI schema.",
                            "Replace this with one of your own case studies in /admin.",
                        ]
                    ),
                    "role": "Author",
                },
                {
                    "language_code": "ru",
                    "title": "Пример REST API",
                    "description": "\n".join(
                        [
                            "Демо backend-сервис с аутентификацией, фоновыми задачами и аккуратной OpenAPI-схемой.",
                            "Замените на свой кейс в /admin.",
                        ]
                    ),
                    "role": "Автор",
                },
            ],
            "stacks": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        },
        {
            "id": _seed_uuid("project-2"),
            "slug": "example-bot",
            "link": None,
            "repo_link": "https://github.com/your-org/example-bot",
            "start_date": date(2024, 3, 1),
            "end_date": None,
            "is_featured": False,
            "translations": [
                {
                    "language_code": "en",
                    "title": "Example Chat Bot",
                    "description": "\n".join(
                        [
                            "A messenger bot template with commands, inline keyboards, and a small API.",
                            "Swap in your own project in /admin.",
                        ]
                    ),
                    "role": "Author",
                },
                {
                    "language_code": "ru",
                    "title": "Пример чат-бота",
                    "description": "\n".join(
                        [
                            "Шаблон бота для мессенджера с командами, клавиатурами и небольшим API.",
                            "Замените на свой проект в /admin.",
                        ]
                    ),
                    "role": "Автор",
                },
            ],
            "stacks": ["Python", "FastAPI", "Redis"],
        },
    ]

    op.bulk_insert(
        projects,
        [
            {
                "id": entry["id"],
                "slug": entry["slug"],
                "link": entry["link"],
                "repo_link": entry["repo_link"],
                "start_date": entry["start_date"],
                "end_date": entry["end_date"],
                "is_featured": entry["is_featured"],
            }
            for entry in project_entries
        ],
    )

    project_translation_rows = []
    project_stack_links = []
    for entry in project_entries:
        for translation in entry["translations"]:
            project_translation_rows.append(
                {
                    "id": uuid.uuid4(),
                    "project_id": entry["id"],
                    "language_code": translation["language_code"],
                    "title": translation["title"],
                    "description": translation["description"],
                    "role": translation["role"],
                }
            )
        for stack_name in entry["stacks"]:
            stack_id = stack_ids.get(stack_name)
            if stack_id:
                project_stack_links.append({"project_id": entry["id"], "stack_id": stack_id})

    op.bulk_insert(project_translations, project_translation_rows)
    if project_stack_links:
        op.bulk_insert(project_stacks, project_stack_links)

    # --- Seed testimonials (placeholder) ---
    testimonial_entries = [
        {
            "id": _seed_uuid("testimonial-1"),
            "author_name": "Jane Doe",
            "author_url": None,
            "author_avatar_url": None,
            "kind": "dev",
            "date": date(2024, 5, 1),
            "translations": [
                {
                    "language_code": "en",
                    "author_position": None,
                    "content": "Sample testimonial. The project was delivered on time with clear communication. Replace this with a real quote in /admin.",
                },
                {
                    "language_code": "ru",
                    "author_position": None,
                    "content": "Пример отзыва. Проект сдан в срок, коммуникация была чёткой. Замените на настоящий отзыв в /admin.",
                },
            ],
        },
        {
            "id": _seed_uuid("testimonial-2"),
            "author_name": "John Smith",
            "author_url": None,
            "author_avatar_url": None,
            "kind": "teacher",
            "date": date(2023, 6, 15),
            "translations": [
                {
                    "language_code": "en",
                    "author_position": None,
                    "content": "Sample testimonial. A patient mentor with clear explanations. Replace this with a real quote in /admin.",
                },
                {
                    "language_code": "ru",
                    "author_position": None,
                    "content": "Пример отзыва. Терпеливый ментор, объясняет понятно. Замените на настоящий отзыв в /admin.",
                },
            ],
        },
    ]

    op.bulk_insert(
        testimonials,
        [
            {
                "id": entry["id"],
                "author_name": entry["author_name"],
                "author_url": entry["author_url"],
                "author_avatar_url": entry["author_avatar_url"],
                "kind": entry["kind"],
                "date": entry["date"],
            }
            for entry in testimonial_entries
        ],
    )

    testimonial_translation_rows = []
    for entry in testimonial_entries:
        for translation in entry["translations"]:
            testimonial_translation_rows.append(
                {
                    "id": uuid.uuid4(),
                    "testimonial_id": entry["id"],
                    "language_code": translation["language_code"],
                    "author_position": translation["author_position"],
                    "content": translation["content"],
                }
            )
    op.bulk_insert(testimonial_translations, testimonial_translation_rows)

    # --- Seed resumes ---
    now_ts = datetime.now(UTC)
    op.bulk_insert(
        resumes,
        [
            {
                "id": _seed_uuid("resume-en"),
                "language_code": "en",
                "file_path": "/cv/cv_en.pdf",
                "generated_at": now_ts,
                "is_active": True,
            },
            {
                "id": _seed_uuid("resume-ru"),
                "language_code": "ru",
                "file_path": "/cv/cv_ru.pdf",
                "generated_at": now_ts,
                "is_active": True,
            },
        ],
    )


def downgrade() -> None:
    """Remove seeded profile content and the testimonial kind column."""
    stack_names = [
        "Python",
        "FastAPI",
        "Django",
        "Node.js",
        "REST",
        "SQLAlchemy",
        "RabbitMQ",
        "LangChain",
        "OpenAI API",
        "PostgreSQL",
        "Redis",
        "Airflow",
        "Docker",
        "Kubernetes",
        "Terraform",
        "GitHub Actions",
        "Grafana",
        "Team Leadership",
        "Roadmapping",
        "Tech Writing",
    ]
    stack_ids = [_seed_uuid(f"stack-{name}") for name in stack_names]
    experience_ids = [
        _seed_uuid("work-exp-1"),
        _seed_uuid("work-exp-2"),
    ]
    project_ids = [
        _seed_uuid("project-1"),
        _seed_uuid("project-2"),
    ]
    testimonial_ids = [
        _seed_uuid("testimonial-1"),
        _seed_uuid("testimonial-2"),
    ]
    resume_ids = [
        _seed_uuid("resume-en"),
        _seed_uuid("resume-ru"),
    ]

    # Remove child rows first to satisfy FK constraints
    for pid in project_ids:
        op.execute(
            sa.text("DELETE FROM project_stacks WHERE project_id = :pid").bindparams(pid=pid)
        )
        op.execute(
            sa.text("DELETE FROM project_translations WHERE project_id = :pid").bindparams(pid=pid)
        )
    for wid in experience_ids:
        op.execute(
            sa.text(
                "DELETE FROM work_experience_stacks WHERE work_experience_id = :wid"
            ).bindparams(wid=wid)
        )
        op.execute(
            sa.text(
                "DELETE FROM work_experience_translations WHERE work_experience_id = :wid"
            ).bindparams(wid=wid)
        )
    for tid in testimonial_ids:
        op.execute(
            sa.text("DELETE FROM testimonial_translations WHERE testimonial_id = :tid").bindparams(
                tid=tid
            )
        )

    for pid in project_ids:
        op.execute(sa.text("DELETE FROM projects WHERE id = :pid").bindparams(pid=pid))
    for wid in experience_ids:
        op.execute(sa.text("DELETE FROM work_experiences WHERE id = :wid").bindparams(wid=wid))
    for tid in testimonial_ids:
        op.execute(sa.text("DELETE FROM testimonials WHERE id = :tid").bindparams(tid=tid))
    for rid in resume_ids:
        op.execute(sa.text("DELETE FROM resumes WHERE id = :rid").bindparams(rid=rid))
    for sid in stack_ids:
        op.execute(sa.text("DELETE FROM stacks WHERE id = :sid").bindparams(sid=sid))

    op.drop_column("testimonials", "kind")

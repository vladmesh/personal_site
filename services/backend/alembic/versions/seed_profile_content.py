# ruff: noqa: E501

"""add testimonial kind and seed profile content

Revision ID: seed_profile_content_002
Revises: seed_contacts_001
Create Date: 2025-11-22 05:30:00.000000

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
    """Add testimonial kind column and seed profile content data."""
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

    # --- Seed stacks (skills) ---
    stack_entries = [
        ("Python", "Backend"),
        ("FastAPI", "Backend"),
        ("Django", "Backend"),
        ("Go", "Backend"),
        ("Node.js", "Backend"),
        ("GraphQL", "Backend"),
        ("REST", "Backend"),
        ("gRPC", "Backend"),
        ("LangChain", "Data & AI"),
        ("Langgraph", "Data & AI"),
        ("OpenAI API", "Data & AI"),
        ("PydanticAI", "Data & AI"),
        ("PostgreSQL", "Data & AI"),
        ("ClickHouse", "Data & AI"),
        ("Airflow", "Data & AI"),
        ("Redis", "Data & AI"),
        ("RabbitMQ", "Backend"),
        ("SQLAlchemy", "Backend"),
        ("Docker", "DevOps"),
        ("Kubernetes", "DevOps"),
        ("Terraform", "DevOps"),
        ("GitHub Actions", "DevOps"),
        ("Grafana", "DevOps"),
        ("Prometheus", "DevOps"),
        ("Team Leadership", "Communication"),
        ("Roadmapping", "Communication"),
        ("Stakeholder Management", "Communication"),
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

    # --- Seed work experience ---
    experience_entries = [
        {
            "id": _seed_uuid("work-exp-dnk"),
            "company_name": "DNK IT Solutions",
            "company_url": "https://uppersetup.com",
            "start_date": date(2022, 1, 1),
            "end_date": date(2023, 12, 31),
            "is_current": False,
            "translations": [
                {
                    "language_code": "en",
                    "position": "Python Software Developer",
                    "description": "\n".join(
                        [
                            "Participated in the design and development of a platform that automates company registration in the UAE (uppersetup.com).",
                            "Designed a microservices backend architecture in Python using FastAPI, SQLAlchemy, and Redis.",
                            "Conducted load testing and unit testing.",
                            "Developed and implemented a CI/CD pipeline for automated deployments.",
                        ]
                    ),
                    "location": "Bishkek",
                },
                {
                    "language_code": "ru",
                    "position": "Python разработчик",
                    "description": "\n".join(
                        [
                            "Участвовал в проектировании и разработке платформы, которая подбирает параметры и автоматизирует регистрацию компании в ОАЭ (uppersetup.com).",
                            "Проектировал микросервисную архитектуру для бэкенда на Python, с использованием FastAPI, SQLAlchemy, Redis.",
                            "Проводил нагрузочное и unit тестирование.",
                            "Разработал и внедрил CI/CD pipeline для автоматизации деплоя.",
                        ]
                    ),
                    "location": "Бишкек",
                },
            ],
            "stacks": ["Python", "FastAPI", "SQLAlchemy", "Redis"],
        },
        {
            "id": _seed_uuid("work-exp-practicum"),
            "company_name": "Yandex Practicum",
            "company_url": "https://practicum.yandex.ru",
            "start_date": date(2021, 1, 1),
            "end_date": date(2022, 12, 31),
            "is_current": False,
            "translations": [
                {
                    "language_code": "en",
                    "position": "Backend Engineer",
                    "description": "\n".join(
                        [
                            "Contributed to backend development of a children’s math platform as part of a Scrum team.",
                            "Developed a Python monolith using Django REST Framework, Celery, Redis, and PostgreSQL.",
                            "Optimized for high load: database query tuning, indexing, sharding, etc.",
                        ]
                    ),
                    "location": "Saint Petersburg",
                },
                {
                    "language_code": "ru",
                    "position": "Backend-инженер",
                    "description": "\n".join(
                        [
                            "Участвовал в разработке бэкенда для платформы детской математики, в составе Scrum-команды.",
                            "Разрабатывал монолитную архитектуру на Python, с использованием DRF, Celery, Redis, PostgreSQL.",
                            "Занимался оптимизацией под высокие нагрузки: отладка запросов, индексы, шардирование и т.д.",
                        ]
                    ),
                    "location": "Санкт-Петербург",
                },
            ],
            "stacks": ["Django", "Redis", "PostgreSQL"],
        },
        {
            "id": _seed_uuid("work-exp-piterauto"),
            "company_name": "Piterauto",
            "company_url": "https://www.piteravto.ru",
            "start_date": date(2018, 1, 1),
            "end_date": date(2021, 12, 31),
            "is_current": False,
            "translations": [
                {
                    "language_code": "en",
                    "position": "Software Developer",
                    "description": "\n".join(
                        [
                            "Integrated CRMs, built end-to-end data pipelines (ETL), and set up business process automation.",
                            "Designed and launched a trip fiscalization system using Python, FastAPI, PostgreSQL, RabbitMQ, and Docker; later evolved into a standalone product (mega-fiscal.ru).",
                        ]
                    ),
                    "location": "Saint Petersburg",
                },
                {
                    "language_code": "ru",
                    "position": "Разработчик ПО",
                    "description": "\n".join(
                        [
                            "Интегрировал CRM, строил сквозные пайплайны данных (ETL), настраивал автоматизацию бизнес-процессов.",
                            "Разработал и внедрил систему для фискализации поездок на Python, FastAPI, PostgreSQL, RabbitMQ, Docker. Позже проект вырос в отдельный продукт (mega-fiscal.ru).",
                        ]
                    ),
                    "location": "Санкт-Петербург",
                },
            ],
            "stacks": ["Python", "FastAPI", "PostgreSQL", "Docker", "RabbitMQ"],
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

    # --- Seed projects ---
    project_entries = [
        {
            "id": _seed_uuid("project-ai-assistant"),
            "slug": "ai-assistant",
            "link": "https://t.me/virutual_helper_bot",
            "repo_link": "https://github.com/vladmesh/Assistants",
            "start_date": date(2025, 1, 1),
            "end_date": None,
            "is_featured": True,
            "translations": [
                {
                    "language_code": "en",
                    "title": "AI assistant for personal use, based on messengers",
                    "description": "\n".join(
                        [
                            "AI assistant for messengers with tools for task planning, calendar scheduling, web search/scraping, and long-term memory via RAG (vector store, embeddings, context updating).",
                            "Keeps personal productivity in chat: creates todo lists, breaks large goals into steps, and follows up on deadlines.",
                            "Integrates Google Calendar to schedule meetings and add events automatically; triggers web search/scraping and RAG pipeline backed by a vector store for research-heavy tasks.",
                        ]
                    ),
                    "role": "Builder & product owner",
                },
                {
                    "language_code": "ru",
                    "title": "Ai ассистент для личного пользования, на основе мессенджеров",
                    "description": "\n".join(
                        [
                            "AI-ассистент для мессенджеров с инструментами: планирование задач, запись событий в Google Calendar, веб-поиск/парсинг, долговременная память через RAG (векторное хранилище, эмбеддинги, актуализация контекста).",
                            "Ассистент помогает вести ежедневные задачи в мессенджере: создает todo-листы, разбивает большие задачи на шаги и напоминает о дедлайнах.",
                            "Через интеграцию с Google Calendar может планировать встречи и автоматически добавлять события, подключает веб-поиск/парсинг и RAG-пайплайн для сложных запросов.",
                        ]
                    ),
                    "role": "Разработчик и продукт-менеджер",
                },
            ],
            "stacks": ["Python", "FastAPI", "LangChain", "Langgraph", "Redis", "Docker"],
        },
        {
            "id": _seed_uuid("project-dnd-helper"),
            "slug": "dnd-helper",
            "link": "https://t.me/dnd_helperbot",
            "repo_link": "https://github.com/vladmesh/dnd_helper",
            "start_date": date(2025, 2, 1),
            "end_date": None,
            "is_featured": False,
            "translations": [
                {
                    "language_code": "en",
                    "title": "DnD reference for messengers",
                    "description": "\n".join(
                        [
                            "Simple DnD 5e reference bot: monsters and spells with filters for level, school, and creature type.",
                            "Adds cursor-based pagination to keep answers compact in messenger UI while exposing full data.",
                            "Runs in Docker and exposes a FastAPI + SQLAlchemy backend powering the bot and public API.",
                        ]
                    ),
                    "role": "Backend developer",
                },
                {
                    "language_code": "ru",
                    "title": "Справочник для игры DnD в мессенджерах",
                    "description": "\n".join(
                        [
                            "Справочник по DnD 5e: список монстров и заклинаний с фильтрами по уровню, школе магии и типу существа.",
                            "Реализована пагинация, чтобы ответы оставались компактными в интерфейсе мессенджера.",
                            "Бот разворачивается в Docker и использует FastAPI + SQLAlchemy для API и хранения данных.",
                        ]
                    ),
                    "role": "Разработчик",
                },
            ],
            "stacks": ["Python", "FastAPI", "SQLAlchemy", "Docker"],
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

    # --- Seed testimonials ---
    testimonial_entries = [
        {
            "id": _seed_uuid("testimonial-nikita"),
            "author_name": "Nikita Nikitin",
            "author_url": "https://www.upwork.com/freelancers/~01b6b1e325874479ec",
            "author_avatar_url": None,
            "kind": "dev",
            "date": date(2024, 5, 1),
            "translations": [
                {
                    "language_code": "en",
                    "author_position": None,
                    "content": (
                        "I highly recommend Vladislav for his exceptional work in creating a Telegram bot for our cryptocurrency project. "
                        "He demonstrated a high level of expertise, professionalism, and attention to detail throughout the project. "
                        "His deep understanding of Python, the Telegram API, and cryptocurrency exchanges and APIs was critical in creating a reliable bot that provided our users with real-time alerts. "
                        "His communication and updates were prompt and frequent, and he consistently exceeded our expectations. "
                        "I highly recommend Vladislav for any project that requires expertise in developing Telegram bots or web parsers."
                    ),
                },
                {
                    "language_code": "ru",
                    "author_position": None,
                    "content": (
                        "Я настоятельно рекомендую Владислава за его работу по созданию Telegram-бота для нашего проекта в сфере криптовалют. "
                        "Он демонстрировал высокий уровень экспертизы, профессионализма и внимания к деталям. "
                        "Его глубокое понимание Python, Telegram API, криптобирж и их API было критически важным для создания надежного бота с оповещениями в реальном времени. "
                        "Коммуникация и обновления были оперативными, результаты стабильно превосходили ожидания. "
                        "Рекомендую Владислава для проектов, где требуется экспертиза в разработке Telegram-ботов или веб-парсеров."
                    ),
                },
            ],
        },
        {
            "id": _seed_uuid("testimonial-dmitriy"),
            "author_name": "Dmitriy",
            "author_url": "https://profi.ru/profile/MeshkorudnyyVD/#reviews-tab",
            "author_avatar_url": None,
            "kind": "teacher",
            "date": date(2023, 3, 1),
            "translations": [
                {
                    "language_code": "en",
                    "author_position": None,
                    "content": (
                        "A consummate professional who can handle any programming task. He explains things clearly and is a great listener. "
                        "Willing to take on challenges of any complexity."
                    ),
                },
                {
                    "language_code": "ru",
                    "author_position": None,
                    "content": (
                        "Профессионал своего дела, может разобраться с любой задачей по программированию. Объясняет четко и понятно, умеет слушать. "
                        "Берется за любые сложности."
                    ),
                },
            ],
        },
        {
            "id": _seed_uuid("testimonial-michael"),
            "author_name": "Michael",
            "author_url": "https://profi.ru/profile/MeshkorudnyyVD/#reviews-tab",
            "author_avatar_url": None,
            "kind": "teacher",
            "date": date(2023, 6, 15),
            "translations": [
                {
                    "language_code": "en",
                    "author_position": None,
                    "content": (
                        "Vlad helped me get to grips with FastAPI, Docker, Redis, and Postgres, and he answered my questions over chat. "
                        "Trying to figure it all out alone felt overwhelming due to the amount of information; Vlad’s support made a huge difference."
                    ),
                },
                {
                    "language_code": "ru",
                    "author_position": None,
                    "content": (
                        "Влад помог разобраться с FastAPI, Docker, Redis и Postgres, отвечал на вопросы в переписке. "
                        "Самостоятельно из-за объема информации было сложно, поддержка Влада сильно помогла."
                    ),
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
    """Remove seeded profile content and testimonial kind column."""
    stack_names = [
        "Python",
        "FastAPI",
        "Django",
        "Go",
        "Node.js",
        "GraphQL",
        "REST",
        "gRPC",
        "LangChain",
        "Langgraph",
        "OpenAI API",
        "PydanticAI",
        "PostgreSQL",
        "ClickHouse",
        "Airflow",
        "Redis",
        "RabbitMQ",
        "SQLAlchemy",
        "Docker",
        "Kubernetes",
        "Terraform",
        "GitHub Actions",
        "Grafana",
        "Prometheus",
        "Team Leadership",
        "Roadmapping",
        "Stakeholder Management",
        "Tech Writing",
    ]
    stack_ids = [_seed_uuid(f"stack-{name}") for name in stack_names]
    experience_ids = [
        _seed_uuid("work-exp-dnk"),
        _seed_uuid("work-exp-practicum"),
        _seed_uuid("work-exp-piterauto"),
    ]
    project_ids = [
        _seed_uuid("project-ai-assistant"),
        _seed_uuid("project-dnd-helper"),
    ]
    testimonial_ids = [
        _seed_uuid("testimonial-nikita"),
        _seed_uuid("testimonial-dmitriy"),
        _seed_uuid("testimonial-michael"),
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

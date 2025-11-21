# Personal Site - Microservices Architecture

Персональный сайт-визитка на микросервисной архитектуре с разделением на frontend (Astro) и backend (FastAPI).

## Архитектура

```
personal_site/
├── infra/              # Инфраструктура
│   ├── docker-compose.yml        # Production compose
│   ├── docker-compose.dev.yml    # Development override
│   ├── configs/                  # Конфигурации (Caddy)
│   └── scripts/                  # Скрипты (init-db.sh)
├── services/
│   ├── frontend/       # Astro статический сайт
│   └── backend/        # FastAPI + SQLAlchemy + Alembic
├── docs/               # Документация
└── shared/             # Общие ресурсы (OpenAPI specs)
```

## Быстрый старт

### Разработка

```bash
# Создать .env файл для dev окружения
cat > infra/.env << EOF
POSTGRES_PASSWORD=devpassword
EOF

# Запустить все сервисы в dev режиме
make dev

# Или с пересборкой
make dev-build
```

После запуска:
- Frontend: http://localhost:4321
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Production

```bash
# Установить production переменные окружения
cat > infra/.env << EOF
POSTGRES_PASSWORD=<secure-password>
POSTGRES_DB=personal_site
POSTGRES_USER=postgres
BACKEND_CORS_ORIGINS=https://vladmesh.dev
EOF

# Собрать и запустить
make build
make start
```

## Основные команды

```bash
make help              # Показать все доступные команды

# Docker Compose
make dev               # Запустить dev окружение
make build             # Собрать все сервисы
make start             # Запустить production
make stop              # Остановить все
make clean             # Остановить и удалить volumes
make logs              # Логи всех сервисов

# Backend
make backend-shell     # Открыть shell в backend контейнере
make backend-migrate   # Применить миграции БД
make backend-migration NAME="description"  # Создать новую миграцию
make backend-test      # Запустить тесты
make backend-lint      # Линтер
make backend-format    # Форматирование кода

# Frontend
make frontend-shell    # Открыть shell в frontend контейнере
make frontend-build    # Собрать frontend локально
make frontend-lint     # Линтер

# Все сервисы
make test              # Запустить все тесты
make lint              # Запустить все линтеры
make format            # Форматировать весь код
```

## Сервисы

### Frontend

Статический сайт на Astro с поддержкой RU/EN локализации.

- **Технологии**: Astro, Tailwind CSS, TypeScript
- **Порт (dev)**: 4321
- **Документация**: [services/frontend/README.md](services/frontend/README.md)

### Backend

REST API на FastAPI с асинхронным доступом к PostgreSQL.

- **Технологии**: FastAPI, SQLAlchemy 2.0 (async), Alembic, AsyncPG
- **Порт (dev)**: 8000
- **Документация**: [services/backend/README.md](services/backend/README.md)

## Разработка

### Требования

- Docker и Docker Compose
- (Опционально) Poetry для локальной разработки backend
- (Опционально) Node.js 20+ для локальной разработки frontend

### Структура веток

- `main` - production ветка, автоматический деплой
- `dev` - development ветка для интеграции фич

### Добавление новой миграции

```bash
# 1. Обновить модели в services/backend/src/app/models/
# 2. Создать миграцию
make backend-migration NAME="add user table"
# 3. Применить миграцию
make backend-migrate
```

### CI/CD

GitHub Actions автоматически:
- Собирает Docker образы для frontend и backend
- Запускает тесты и линтеры
- Деплоит на VPS при push в `main`

См. [.github/workflows/](. github/workflows/) для деталей.

## Deployment

Деплой осуществляется через Docker Compose на VPS. Caddy автоматически получает SSL сертификаты от Let's Encrypt.

Подробнее: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)

## Дорожная карта

См. [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) для планов развития проекта.

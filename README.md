# Personal Site - Microservices Architecture

Персональный сайт-визитка на микросервисной архитектуре с разделением на frontend (Astro) и backend (FastAPI).

## Архитектура

```
personal_site/
├── infra/              # Инфраструктура
│   ├── docker-compose.yml        # Base compose (dev/local build)
│   ├── docker-compose.dev.yml    # Development override
│   ├── docker-compose.prod.yml   # Standalone production stack (ghcr images + Caddy on 80/443)
│   ├── docker-compose.tunnel.yml # Production stack behind a Cloudflare Tunnel (what deploy.yml ships)
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
BACKEND_CORS_ORIGINS=https://your-domain.example
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

# Тестирование (Docker-based)
make test              # Запустить все тесты с coverage
make test-unit         # Только unit тесты (SQLite)
make test-integration  # Только integration тесты (PostgreSQL)

# Качество кода (Docker-based)
make lint              # Запустить линтер
make format            # Форматировать код
make typecheck         # Проверка типов

# Pre-commit hooks
make pre-commit-install  # Установить git hooks

# Frontend
make frontend-shell    # Открыть shell в frontend контейнере
make frontend-build    # Собрать frontend локально
make frontend-lint     # Линтер

# Все сервисы
make test              # Запустить все тесты
make lint              # Запустить все линтеры
make format            # Форматировать весь код
```

## Настройка окружения разработки

### Первичная настройка

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd personal_site

# 2. Установить git hooks (автоформат при коммите, проверки перед пушем)
make pre-commit-install

# 3. Создать .env файл
cat > infra/.env << EOF
POSTGRES_PASSWORD=devpassword
EOF

# 4. Запустить dev окружение
make dev
```

### Git Hooks

После установки через `make pre-commit-install`:

- **Pre-commit**: Автоматически форматирует код (`ruff format`) и исправляет линты (`ruff check --fix`) при каждом коммите
- **Pre-push**: Запускает линтер, type checker и все тесты в Docker перед пушем. Блокирует пуш если есть ошибки

### Запуск тестов

Все тесты запускаются в Docker, не требуют локального Python:

```bash
# Все тесты с coverage
make test

# Только unit тесты (быстрые, SQLite in-memory)
make test-unit

# Только integration тесты (реальный PostgreSQL + HTTP запросы)
make test-integration
```

**Типы тестов:**
- **Unit тесты**: Используют SQLite in-memory, быстрые, изолированные
- **Integration тесты**: Поднимают реальный PostgreSQL, делают HTTP запросы к API

### Проверка качества кода

```bash
# Линтер (ruff)
make lint

# Автоформат
make format

# Type checking (mypy)
make typecheck
```

Все команды запускаются в Docker, не требуют локальной установки зависимостей.

## Сервисы

### Frontend

Astro-приложение (RU/EN), теперь тянет профильные данные из backend API (`/api/v1/profile/full`).

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

GitHub Actions автоматически запускает при каждом push/PR:

**Lint Job:**
- Ruff linter
- MyPy type checking

**Test Job** (запускается после успешного lint):
- Unit тесты (SQLite)
- Integration тесты (PostgreSQL в Docker)

Все проверки выполняются в Docker контейнерах для консистентности с локальным окружением.

См. [.github/workflows/ci.yml](.github/workflows/ci.yml) для деталей.


## Deployment

Push в `main` (или ручной `workflow_dispatch`) запускает workflow `Deploy`: CI → сборка образов в ghcr → деплой на VPS по SSH. См. [.github/workflows/deploy.yml](.github/workflows/deploy.yml).

Workflow кладёт на сервер стек [infra/docker-compose.tunnel.yml](infra/docker-compose.tunnel.yml) (`postgres + backend + frontend + caddy + cloudflared`) в `~/personal_site` пользователя деплоя и делает `docker compose pull backend frontend && docker compose up -d`. Портов наружу нет: вход только через Cloudflare Tunnel до внутреннего Caddy на `caddy:8080` ([infra/configs/Caddyfile.tunnel](infra/configs/Caddyfile.tunnel)). Миграции применяются автоматически при старте backend (`alembic upgrade head` в entrypoint).

Workflow рассчитан на чужой/общий хост: без `sudo`, Docker может быть rootless, никаких `prune`, ничего вне `~/personal_site`, и он **никогда не пишет `.env`** — это единственная копия пароля БД, хеша админа и токена туннеля. Если `.env` нет, деплой падает.

Альтернатива для отдельного VPS — [infra/docker-compose.prod.yml](infra/docker-compose.prod.yml), где Caddy сам держит 80/443 и получает Let's Encrypt сертификат; workflow его не использует.

Чтобы развернуть свой инстанс (форк):

1. **Cloudflare Tunnel**: создать туннель, public hostname `your-domain` (и `www`) → `http://caddy:8080`, взять его токен.
2. **На сервере**: Docker с Compose v2 (rootless подходит), `~/personal_site/.env` (0600) с `POSTGRES_PASSWORD`, `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH` (PBKDF2, `python -m app.security '<пароль>'`), `ADMIN_SECRET_KEY`, `SITE_DOMAIN`, `SITE_BRAND`, `TUNNEL_TOKEN`, `REGISTRY_OWNER`. Compose интерполирует `.env`, поэтому `$` в хеше пишется как `$$`.
3. **GitHub**: environment `production` (deployment branches: `main`) с секретами `VPS_HOST`, `VPS_USER`, `VPS_SSH_PORT`, `VPS_SSH_KEY` (приватный ключ, публичная половина — в `~/.ssh/authorized_keys` пользователя, можно с `restrict`). Repo variable `SITE_DOMAIN` включает smoke-check `https://SITE_DOMAIN` после деплоя; `DEPLOY_DIR` переопределяет `personal_site`. `REGISTRY_OWNER` выводится из владельца репозитория (`github.repository_owner`); пакеты ghcr должны быть публичными — workflow не логинится в registry на сервере.
4. Push в `main` → через несколько минут сайт живой на `https://your-domain`. Контент правится в админке `https://your-domain/admin`.

Дорожная карта: [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)

## Дорожная карта

См. [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) для планов развития проекта.

# Docker Infrastructure Audit

**Дата аудита:** 2024-12-06  
**Статус:** Средний - есть возможности для оптимизации

---

## Обзор

Проект содержит 2 основных сервиса (backend, frontend) с multi-stage Dockerfile. Инфраструктура организована достаточно хорошо, но есть несколько проблем, влияющих на размер кэша и скорость сборки.

---

## Выявленные проблемы

### 1. Отсутствует `.dockerignore` (КРИТИЧНО)

**Влияние:** При сборке копируется весь контекст проекта, включая:
- `.git/`
- `node_modules/`
- `__pycache__/`
- `.venv/`

**Решение:** Создать `.dockerignore` в корне проекта:

```gitignore
# Git
.git
.gitignore

# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/

# Node
node_modules/
.npm/
.pnpm-store/

# Testing
.pytest_cache/
.coverage
htmlcov/
coverage/

# Linting
.ruff_cache/
.mypy_cache/
.eslintcache

# IDE
.idea/
.vscode/
*.swp

# Environment
.env
.env.*
!.env.example

# Misc
*.log
*.tmp
Thumbs.db
.DS_Store
```

---

### 2. Backend: Неиспользуемый development stage

**Текущий код:**
```dockerfile
FROM python:3.12-slim AS development  # Этот stage не используется в compose
# ...много кода...

FROM python:3.12-slim AS deps
FROM python:3.12-slim AS production
```

**Проблема:** `development` stage занимает место в кэше, но не используется в docker-compose.

**Решение:** Либо удалить, либо использовать в `docker-compose.dev.yml`:

```yaml
# docker-compose.dev.yml
services:
  backend:
    build:
      context: ../services/backend
      dockerfile: Dockerfile
      target: development  # Использовать development stage
    volumes:
      - ../services/backend:/app
```

---

### 3. Frontend: Копирование node_modules в production

**Текущий код:**
```dockerfile
FROM node:20-alpine AS production

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules  # ~200MB лишнего?
```

**Анализ:** Для Astro SSR это может быть необходимо. Однако стоит проверить:

```bash
# Проверить размер node_modules в production образе
docker run --rm frontend:prod du -sh /app/node_modules
```

**Возможное решение:** Если Astro поддерживает standalone режим:
```dockerfile
# Использовать только необходимые runtime зависимости
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
```

---

### 4. Разные версии Python в экосистеме

**Текущее состояние:**
- personal_site: Python 3.12
- Другие проекты: Python 3.11

**Рекомендация:** Унифицировать версию Python во всех проектах для:
- Уменьшения количества базовых образов в кэше
- Упрощения поддержки
- Консистентности окружения

---

### 5. docker-compose.yml: отсутствует target для build

**Текущий код:**
```yaml
backend:
  build:
    context: ../services/backend
    dockerfile: Dockerfile
    # target не указан - собирается последний stage
```

**Рекомендация:** Явно указывать target:
```yaml
backend:
  build:
    context: ../services/backend
    dockerfile: Dockerfile
    target: production
```

---

## Рекомендуемые изменения

### Шаг 1: Создать `.dockerignore` (5 минут)

Создать файл `/home/vlad/projects/personal_site/.dockerignore` с содержимым из раздела 1.

### Шаг 2: Оптимизировать Backend Dockerfile (15 минут)

```dockerfile
# syntax=docker/dockerfile:1.7

# Dependencies stage
FROM python:3.12-slim AS deps

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --no-root --only main

# Production stage
FROM python:3.12-slim AS production

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY . .

RUN chmod +x /app/entrypoint.sh && \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["/app/entrypoint.sh"]
```

### Шаг 3: Проверить необходимость node_modules (10 минут)

```bash
# Собрать без node_modules и проверить работоспособность
docker build --target production -t frontend:test .
docker run --rm frontend:test node ./dist/server/entry.mjs
```

### Шаг 4: Обновить docker-compose файлы (10 минут)

```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: ../services/backend
      dockerfile: Dockerfile
      target: production
      
  frontend:
    build:
      context: ../services/frontend
      dockerfile: Dockerfile
      target: production
```

---

## Ожидаемый результат

| Метрика | До | После |
|---------|-----|-------|
| Размер build cache | ~3GB | ~1.5GB |
| Время сборки backend (повторная) | ~2 мин | ~30 сек |
| Размер образа frontend | ~400MB | ~250MB* |

*При условии, что node_modules можно убрать

---

## Приоритет исправлений

1. **ВЫСОКИЙ:** Создать `.dockerignore` - мгновенный эффект
2. **СРЕДНИЙ:** Удалить/использовать development stage
3. **СРЕДНИЙ:** Проверить node_modules в production
4. **НИЗКИЙ:** Явно указать target в compose

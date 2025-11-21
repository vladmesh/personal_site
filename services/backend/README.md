# Backend Service

FastAPI backend service for personal site with async SQLAlchemy and Alembic migrations.

## Tech Stack

- FastAPI - Web framework
- SQLAlchemy 2.0 - Async ORM
- Alembic - Database migrations
- AsyncPG - PostgreSQL async driver
- Pydantic - Data validation
- Poetry - Dependency management

## Development

```bash
# Install dependencies
poetry install

# Run development server
poetry run uvicorn app.main:app --reload

# Create new migration
poetry run alembic revision --autogenerate -m "description"

# Run migrations
poetry run alembic upgrade head

# Run tests
poetry run pytest

# Lint
poetry run ruff check .

# Format
poetry run ruff format .
```

## Project Structure

```
services/backend/
├── src/
│   └── app/
│       ├── main.py           # FastAPI application
│       ├── config.py         # Settings
│       ├── database.py       # SQLAlchemy setup
│       ├── api/              # API routes
│       │   └── v1/
│       │       └── health.py
│       ├── models/           # SQLAlchemy models
│       ├── schemas/          # Pydantic schemas
│       └── core/             # Core utilities
├── alembic/                  # Database migrations
├── tests/                    # Tests
├── pyproject.toml           # Poetry config
└── Dockerfile               # Multi-stage build
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

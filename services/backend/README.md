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

# Run only unit tests
poetry run pytest -m unit

# Run only integration tests
poetry run pytest -m integration

# Run with coverage
poetry run pytest --cov=app --cov-report=term-missing

# Lint
poetry run ruff check .

# Format
poetry run ruff format .

# Type check
poetry run mypy src/
```

## Testing

The project uses pytest with two types of tests:

### Unit Tests

Located in `tests/api/`, marked with `@pytest.mark.unit`:
- Use SQLite in-memory database
- Fast and isolated
- No external dependencies
- Run with: `pytest -m unit`

### Integration Tests

Located in `tests/integration/`, marked with `@pytest.mark.integration`:
- Use real PostgreSQL database
- Make actual HTTP requests to API
- Test full request/response cycle
- Run with: `pytest -m integration`

### Running Tests in Docker

All tests can be run in Docker (recommended for CI/CD consistency):

```bash
# From project root
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make test              # All tests with coverage
```

### Writing New Tests

**Unit Test Example:**
```python
@pytest.mark.unit
@pytest.mark.asyncio
async def test_something(client: AsyncClient, db: AsyncSession):
    # Test uses SQLite in-memory
    pass
```

**Integration Test Example:**
```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_something_integration(client: AsyncClient, db: AsyncSession):
    # Test uses real PostgreSQL
    pass
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

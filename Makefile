.PHONY: help dev build start stop clean logs
.PHONY: backend-shell backend-migrate backend-migration backend-test backend-lint backend-format backend-typecheck
.PHONY: frontend-shell frontend-build frontend-lint
.PHONY: test lint format typecheck
.PHONY: test-unit test-integration test-all lint-docker format-docker typecheck-docker pre-commit-install

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-25s\\033[0m %s\\n", $$1, $$2}'

# === Docker Compose Commands ===

dev:  ## Start development environment (detached)
	cd infra && docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dev-build:  ## Build and start development environment (detached)
	cd infra && docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

build:  ## Build all services
	cd infra && docker compose -f docker-compose.yml build

start:  ## Start production environment
	cd infra && docker compose -f docker-compose.yml up -d

stop:  ## Stop all services
	cd infra && docker compose -f docker-compose.yml -f docker-compose.dev.yml down

clean:  ## Stop and remove volumes
	cd infra && docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v

logs:  ## Follow logs from all services
	cd infra && docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

# === Backend Commands ===

backend-shell:  ## Open shell in backend container
	cd infra && docker compose exec backend bash

backend-migrate:  ## Run database migrations
	cd infra && docker compose exec backend alembic upgrade head

backend-migration:  ## Create new migration (use NAME=description)
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME is required. Usage: make backend-migration NAME='description'"; \
		exit 1; \
	fi
	cd infra && docker compose exec backend alembic revision --autogenerate -m "$(NAME)"

backend-test:  ## Run backend tests
	cd services/backend && poetry run pytest

backend-lint:  ## Run backend linter
	cd services/backend && poetry run ruff check .

backend-format:  ## Format backend code
	cd services/backend && poetry run ruff format .

backend-typecheck:  ## Run backend type checker
	cd services/backend && poetry run mypy src/

# === Frontend Commands ===

frontend-shell:  ## Open shell in frontend container (dev only)
	cd infra && docker compose exec frontend sh

frontend-build:  ## Build frontend locally
	cd services/frontend && npm run build

frontend-lint:  ## Run frontend linter
	cd services/frontend && npm run lint || echo "No lint script configured"

# === Testing Commands (Docker-based) ===

test-unit:  ## Run unit tests only (SQLite in Docker)
	cd infra && docker compose -f docker-compose.test.yml run --rm backend-test pytest -m unit -v

test-integration:  ## Run integration tests only (PostgreSQL in Docker)
	cd infra && docker compose -f docker-compose.test.yml run --rm backend-test pytest -m integration -v
	cd infra && docker compose -f docker-compose.test.yml down -v

test-all:  ## Run all tests with coverage (in Docker)
	cd infra && docker compose -f docker-compose.test.yml run --rm backend-test pytest --cov=app --cov-report=term-missing -v
	cd infra && docker compose -f docker-compose.test.yml down -v

# === Quality Checks (Docker-based) ===

lint-docker:  ## Run linter in Docker
	cd infra && docker compose -f docker-compose.test.yml run --rm backend-test ruff check .

format-docker:  ## Run formatter in Docker
	cd infra && docker compose -f docker-compose.test.yml run --rm backend-test ruff format .

typecheck-docker:  ## Run type checker in Docker
	cd infra && docker compose -f docker-compose.test.yml run --rm backend-test mypy src/

# === Pre-commit Setup ===

pre-commit-install:  ## Install pre-commit and pre-push hooks
	cd services/backend && poetry install
	cd services/backend && poetry run pre-commit install
	cp scripts/pre-push .git/hooks/pre-push
	chmod +x .git/hooks/pre-push
	@echo "✅ Pre-commit and pre-push hooks installed!"

# === All Services Commands ===

test: test-all  ## Run all tests

lint: lint-docker  ## Run all linters

format: format-docker  ## Format all code

typecheck: typecheck-docker  ## Run all type checkers

.PHONY: help dev build start stop clean logs
.PHONY: backend-shell backend-migrate backend-migration backend-test backend-lint backend-format backend-typecheck
.PHONY: frontend-shell frontend-build frontend-lint
.PHONY: test lint format typecheck

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

# === Docker Compose Commands ===

dev:  ## Start development environment
	cd infra && docker compose -f docker-compose.yml -f docker-compose.dev.yml up

dev-build:  ## Build and start development environment
	cd infra && docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

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

# === All Services Commands ===

test: backend-test  ## Run all tests

lint: backend-lint frontend-lint  ## Run all linters

format: backend-format  ## Format all code

typecheck: backend-typecheck  ## Run all type checkers

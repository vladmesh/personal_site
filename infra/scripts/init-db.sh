#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -U "${POSTGRES_USER:-postgres}"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is ready!"

echo "Running database migrations..."
cd /app
alembic upgrade head

echo "Database initialization complete!"

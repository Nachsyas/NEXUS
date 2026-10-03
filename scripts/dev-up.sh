#!/usr/bin/env bash
set -euo pipefail

echo "==> Starting NEXUS local infrastructure (PostgreSQL 16 + Redis 7)..."
docker compose -f infrastructure/docker/docker-compose.yml up -d

echo "==> Waiting for PostgreSQL to become healthy..."
docker compose -f infrastructure/docker/docker-compose.yml exec postgres pg_isready -U nexus -d nexus_dev || sleep 2

echo "==> Running backend database migrations..."
cd backend
uv run alembic upgrade head

echo "==> NEXUS local development environment is ready!"

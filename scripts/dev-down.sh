#!/usr/bin/env bash
set -euo pipefail

echo "==> Stopping NEXUS local infrastructure..."
docker compose -f infrastructure/docker/docker-compose.yml down

echo "==> NEXUS local infrastructure stopped."

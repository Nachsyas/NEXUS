# NEXUS Local Infrastructure

Local development services powered by Docker Compose.

## Services
- **PostgreSQL 16 with pgvector:** (`pgvector/pgvector:pg16`) on port `5432`
- **Redis 7:** (`redis:7-alpine`) on port `6379`

## Usage Commands

### Start Services
```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d
```

### Check Service Health
```bash
docker compose -f infrastructure/docker/docker-compose.yml ps
```

### Run Alembic Database Migrations
```bash
cd backend
uv run alembic upgrade head
```

### Stop Services
```bash
docker compose -f infrastructure/docker/docker-compose.yml down
```

### Stop and Wipe Volumes (Reset State)
```bash
docker compose -f infrastructure/docker/docker-compose.yml down -v
```

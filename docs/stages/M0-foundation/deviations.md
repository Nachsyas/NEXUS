# Deviations: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03  

## 1. Architectural Deviations
*None.* The implementation strictly adheres to the approved Phase 1 specification and accepted ADRs.

## 2. Operational & Environment Deviations

### Deviation DEV-001: Local Host Port Conflict Adjustment
- **Context:** The standard local Docker Compose ports for PostgreSQL (`5432`) and Redis (`6379`) were already bound on the host machine by external services (`intelligent-commerce-sync-postgres` and `intelligent-commerce-sync-redis`).
- **Initial Plan:** Expose containers on standard default ports 5432 and 6379.
- **Adjustment Made:** Mapped PostgreSQL container host port to `5433` and Redis container host port to `6380` via `.env` and `docker-compose.yml` environment variable overrides (`${POSTGRES_PORT:-5433}:5432`, `${REDIS_PORT:-6380}:6379`).
- **Impact:** Completely benign. Both host environments coexist seamlessly without disrupting the user's running projects. Application runtime connects cleanly to `localhost:5433` and `localhost:6380`.

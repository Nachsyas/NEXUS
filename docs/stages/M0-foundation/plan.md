# Execution Plan: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Phase:** Phase 1  
**Status:** COMPLETE  

## 1. Objectives & Boundaries
Establish a verified, runnable, and reproducible multi-platform engineering foundation across iOS, macOS Agent, Backend, and Infrastructure.

### Strict Non-Negotiable Boundaries:
- NO Phase 1 business endpoints or premature domain models.
- NO speculative entity abstractions or domain services.
- NO arbitrary shell execution capabilities in Mac Agent (ADR-010).
- NO speculative UI designs; minimal technical launch views only.
- NO secret hardcoding; environment variables and `.env.example` templates only.

## 2. Work Breakdown Structure (WBS)
1. **Tooling & Architecture Decisions (ADRs):**
   - Resolve TBD-013 (`uv`), TBD-014 (`UUIDv7`), TBD-015 (`Ruff + Mypy`), TBD-026 (`PostgreSQL 16 + pgvector`).
   - Create ADR-016, ADR-017, ADR-018, ADR-019. Update TBD registry and active decisions registers.
2. **iOS Project Migration (`apps/ios/`):**
   - Inspect existing starter project (`Untitled Project.xcodeproj` & `MyApp/`).
   - Relocate and reconfigure to `apps/ios/NEXUS.xcodeproj` with target `NEXUS`.
   - Implement clean launch view ("NEXUS — Foundation Ready").
   - Compile and build for macOS and iOS Simulator.
   - Verify execution and remove obsolete root starter scaffold.
3. **Mac Agent Foundation (`apps/mac-agent/`):**
   - Initialize native Swift executable package (`NEXUSAgent`).
   - Establish module boundaries: `App/`, `AgentCore/`, `Capabilities/`, `Security/`, `Realtime/`.
   - Verify build and minimal startup.
4. **FastAPI Backend Skeleton (`backend/`):**
   - Initialize `pyproject.toml` with `uv` dependencies.
   - Configure environment settings via Pydantic (`app/core/config.py`).
   - Implement structured JSON logging with redaction (`app/core/logging.py`).
   - Implement request correlation middleware (`app/core/middleware.py`).
   - Implement async database and Redis managers (`app/core/database.py`, `app/core/redis.py`).
   - Implement technical health endpoints (`GET /health`, `GET /api/v1/health`).
   - Establish Alembic migrations and create baseline migration.
   - Write comprehensive Pytest test suite.
5. **Local Infrastructure (`infrastructure/docker/`):**
   - Create `docker-compose.yml` for PostgreSQL 16 (pgvector) and Redis 7.
   - Configure non-colliding host ports (5433, 6380) to avoid conflict with existing host services.
   - Start containers, verify health checks, and run Alembic baseline migration.
6. **Shared Packages (`packages/`):**
   - Set up `protocols/`, `schemas/`, and `constants/` contract packages with documentation.
7. **CI Pipeline & Developer Tooling:**
   - Update `.github/workflows/ci.yml` with lint, format, type-check, test, and governance checks.
   - Provide local developer scripts: `dev-up.sh`, `dev-down.sh`, `run-tests.sh`.
8. **Stage Evidence & Governance:**
   - Complete all 12 stage documentation files.
   - Update context files: `PROJECT-STATE.md`, `CURRENT-STAGE.md`, `NEXT-ACTIONS.md`, `KNOWN-ISSUES.md`, `HANDOFF.md`.

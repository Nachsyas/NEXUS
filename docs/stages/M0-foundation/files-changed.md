# Files Changed: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03  

## 1. Files Created
- `.gitignore` (Updated to ignore Swift PM `.build/`, Python virtualenvs, and test caches)
- `.env.example`
- `.github/workflows/ci.yml`
- `apps/ios/NEXUS.xcodeproj/project.pbxproj`
- `apps/ios/NEXUS.xcodeproj/project.xcworkspace/contents.xcworkspacedata`
- `apps/ios/NEXUS/App/NEXUSApp.swift`
- `apps/ios/NEXUS/App/ContentView.swift`
- `apps/ios/NEXUS/Assets.xcassets/` (Relocated from starter project)
- `apps/mac-agent/Package.swift`
- `apps/mac-agent/Sources/App/AgentApp.swift`
- `apps/mac-agent/Sources/AgentCore/AgentEngine.swift`
- `apps/mac-agent/Sources/Capabilities/CapabilityProtocol.swift`
- `apps/mac-agent/Sources/Security/SecurityBoundary.swift`
- `apps/mac-agent/Sources/Realtime/RealtimeProtocol.swift`
- `backend/pyproject.toml`
- `backend/uv.lock`
- `backend/README.md`
- `backend/.env.example`
- `backend/.env`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/script.py.mako`
- `backend/alembic/versions/0001_baseline_schema.py`
- `backend/app/__init__.py`
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/core/logging.py`
- `backend/app/core/middleware.py`
- `backend/app/core/database.py`
- `backend/app/core/redis.py`
- `backend/app/api/v1/router.py`
- `backend/app/api/v1/health.py`
- `backend/tests/conftest.py`
- `backend/tests/test_startup.py`
- `backend/tests/test_health.py`
- `backend/tests/test_logging.py`
- `backend/tests/test_middleware.py`
- `infrastructure/docker/docker-compose.yml`
- `infrastructure/docker/README.md`
- `packages/README.md`
- `packages/protocols/README.md`
- `packages/schemas/README.md`
- `packages/constants/README.md`
- `scripts/dev-up.sh`
- `scripts/dev-down.sh`
- `scripts/run-tests.sh`
- `docs/decisions/ADR-016-uv-python-package-manager.md`
- `docs/decisions/ADR-017-uuidv7-primary-id-strategy.md`
- `docs/decisions/ADR-018-ruff-mypy-python-tooling.md`
- `docs/decisions/ADR-019-postgresql-16-major-version-baseline.md`
- `docs/stages/M0-foundation/README.md`
- `docs/stages/M0-foundation/plan.md`
- `docs/stages/M0-foundation/implementation-log.md`
- `docs/stages/M0-foundation/files-changed.md`
- `docs/stages/M0-foundation/commands-run.md`
- `docs/stages/M0-foundation/test-results.md`
- `docs/stages/M0-foundation/performance-results.md`
- `docs/stages/M0-foundation/security-review.md`
- `docs/stages/M0-foundation/architecture-review.md`
- `docs/stages/M0-foundation/deviations.md`
- `docs/stages/M0-foundation/known-issues.md`
- `docs/stages/M0-foundation/completion-report.md`

## 2. Files Modified
- `docs/architecture/TBD-REGISTRY.md` (Updated TBD-013, TBD-014, TBD-015, TBD-026 to RESOLVED)
- `docs/decisions/README.md` (Registered ADR-016 through ADR-019)
- `docs/context/ACTIVE-DECISIONS.md` (Registered ADR-016 through ADR-019)
- `docs/context/PROJECT-STATE.md`
- `docs/context/CURRENT-STAGE.md`
- `docs/context/NEXT-ACTIONS.md`
- `docs/context/KNOWN-ISSUES.md`
- `docs/context/HANDOFF.md`

## 3. Files Deleted (Safe Migration)
- `Untitled Project.xcodeproj/project.pbxproj`
- `Untitled Project.xcodeproj/project.xcworkspace/contents.xcworkspacedata`
- `MyApp/MyApp.swift`
- `MyApp/ContentView.swift`
- `MyApp/Assets.xcassets/AccentColor.colorset/Contents.json`
- `MyApp/Assets.xcassets/Contents.json`

# Known Issues: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03  

## 1. Resolved Issues During M0
- **ISSUE-001 (Xcode Starter at Root):** Migrated starter Xcode project (`Untitled Project.xcodeproj` and `MyApp/`) into `apps/ios/NEXUS.xcodeproj` and verified compilation and launch. Root starter files removed. **STATUS: RESOLVED**.
- **ISSUE-002 (Unresolved M0 TBDs):** TBD-013 (`uv`), TBD-014 (`UUIDv7`), TBD-015 (`Ruff + Mypy`), and TBD-026 (`PostgreSQL 16`) resolved via ADR-016 through ADR-019. **STATUS: RESOLVED**.
- **ISSUE-003 (SQLAlchemy Asyncpg Greenlet Missing):** Identified dependency requirement during initial test run; resolved by installing `greenlet>=3.0.0` in `backend/pyproject.toml`. **STATUS: RESOLVED**.

## 2. Active Known Issues Carried Forward
*None.* All M0 foundation components are compiling, passing tests, and operating without outstanding errors.

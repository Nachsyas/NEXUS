# Known Issues: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03 (Updated 2026-10-04)  

## 1. Resolved Issues During M0
- **ISSUE-001 (Xcode Starter at Root):** Migrated starter Xcode project (`Untitled Project.xcodeproj` and `MyApp/`) into `apps/ios/NEXUS.xcodeproj` and verified compilation and launch. Root starter files removed. **STATUS: RESOLVED**.
- **ISSUE-002 (M0 TBD Implementation Decisions):** TBD-013 (`uv`), TBD-014 (`UUIDv7`), TBD-015 (`Ruff + Mypy`), and TBD-026 (`PostgreSQL 16`) formally approved and ratified as ACCEPTED in ADR-016 through ADR-019. **STATUS: RATIFIED & RESOLVED**.
- **ISSUE-003 (SQLAlchemy Asyncpg Greenlet Missing):** Identified dependency requirement during initial test run; resolved by installing `greenlet>=3.0.0` in `backend/pyproject.toml`. **STATUS: RESOLVED**.
- **ISSUE-004 (iOS Target Platform Pollution):** Unintended template platforms (`macosx`, `xros`) removed from `NEXUS.xcodeproj`; target constrained cleanly to iOS/iPadOS (`iphoneos`, `iphonesimulator`). **STATUS: RESOLVED**.

## 2. Active Governance / Architecture Items Carried Forward
- **TBD-027 (Mac Agent Phase 1 Packaging):** Evaluates transition from M0 Swift Package foundation executable to final Phase 1 macOS application packaging (.app bundle / menu bar status item) before M6/M7. **STATUS: OPEN**.

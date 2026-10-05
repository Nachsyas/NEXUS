# CURRENT STAGE: Milestone M2 Formal Closure Complete (Awaiting M3 Execution)

**Current Stage:** Milestone M2 (Projects Domain Foundation) — CLOSED — COMPLETE (Integrated to `main`)  
**Phase:** Phase 1 (Core Personal Intelligence System)  
**Production NEXUS Implementation:** M1 Account & Identity + M2 Projects Domains Established & Verified on `main`  
**M2 Implementation Status:** COMPLETE  
**M2 Integration to Main:** COMPLETE (PR #1 MERGED — commit `4a5342e33de7e01b602dc38a40e567f0ab352864`)  
**Live Apple E2E Status:** `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED` (Offline mock verifier 100% automated coverage; production verifier code complete)  
**Next Stage:** Milestone M3 (Memory Core) — NOT STARTED (Strictly pending separate explicit user authorization)  
**Standing Autonomous Execution:** HALTED AT M2 BOUNDARY  

---

## 1. Stage Objectives & Accomplishments (Milestone M2 Closure)
Milestone M2 established and hardened the canonical Projects domain across backend services, REST endpoints, database schema, and iOS client integration, and has been successfully merged into `main`.

### Delivered & Verified Deliverables:
- [x] **Canonical Domain Models & Separation:** `Project` and `ProjectTechnology` models with RFC 9562 UUIDv7 primary keys.
- [x] **Database Schema & Migrations:** Created `projects`, `project_technologies`, and added `default_project_id` FK to `user_preferences` via Alembic migration `0003_projects_and_technologies.py`. Forward and rollback migrations fully verified with orphan cleanup safeguards.
- [x] **Database Invariants Enforced:**
  - `uq_projects_user_slug`: Unique slug per user. Bounded retry loop (5 attempts) with nested savepoints (`db.begin_nested()`) ensures concurrent same-name creation does not produce unhandled 500 errors.
  - `chk_projects_progress_bounds`: Progress validated between 0 and 100.
  - `uq_projects_user_active`: Partial unique index guaranteeing at most one active project per user.
  - `uq_project_technologies_project_name`: Unique technology names within a project.
  - `fk_user_preferences_default_project_id`: Referential integrity with `ON DELETE SET NULL`.
- [x] **Preferences Default Project Ownership Validation:** In `UserService.update_user_preferences`, strictly verifies that `default_project_id` belongs to the authenticated user. Cross-tenant assignment is rejected with 404 `PROJECT_NOT_FOUND`; `null` clears default project.
- [x] **Active Focus Invariant & Concurrency Safety:** User row-level lock (`select(User.id).where(User.id == user_id).with_for_update()`) serializes concurrent activation calls, atomically deactivating prior active focus and activating target project. Backed by PostgreSQL partial unique index.
- [x] **Deterministic M2 Context Baseline:** `GET /api/v1/projects/{project_id}/context` returns deterministic project metadata only. Future Memory and Knowledge placeholders (`memory_count`, `knowledge_count`) have been excluded from M2.
- [x] **Soft Archiving:** Setting `status = ARCHIVED`, `is_active = false`, and recording `archived_at`. Default listings exclude archived projects unless `include_archived=true`.
- [x] **RESTful API Surface:** 7 endpoints under `/api/v1/projects` implemented with RFC-compliant response envelopes, canonical priorities (`LOW`, `NORMAL`, `HIGH`), and bounded pagination (`limit <= 100`).
- [x] **iOS Client Architecture:**
  - `ProjectModels.swift`: Swift domain models and payloads aligned to canonical priorities and metadata-only context.
  - `NexusAPIClient.swift`: Added 7 typed networking methods with fractional-second ISO8601 date decoding.
  - `ProjectManager.swift`: Observable state store managing projects, active focus, loading state, and error handling.
  - `ProjectsListView.swift`, `CreateProjectSheet.swift`, `ProjectDetailView.swift`: SwiftUI views for browsing, creating, inspecting, activating, and archiving projects.
  - `ContentView.swift`: Authenticated TabView navigation between Projects and Account.
- [x] **Target Compilation:** iOS target builds cleanly (`** BUILD SUCCEEDED **`); macOS agent regression builds cleanly (`Build complete!`).
- [x] **Automated Tests:** 37/37 backend tests passing cleanly (14 dedicated project domain tests including concurrent slug generation, concurrent activation safety, and default project ownership validation).
- [x] **Quality Tooling:** Ruff check, Ruff format check, and Mypy strict mode 100% passing across 37 source files.
- [x] **Stage Documentation:** All 12 files completed and synchronized in canonical path `docs/stages/phase-1/M2-projects/`.
- [x] **Integration & Closure:** PR #1 merged into `main` via merge commit `4a5342e33de7e01b602dc38a40e567f0ab352864`.

---

## 2. Milestone M1 Foundation (Preserved Baseline)
- All M1 deliverables (Apple Sign In, sessions, refresh token rotation, user preferences) remain operational and fully regression tested.
- `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED` remains documented until physical hardware testing.

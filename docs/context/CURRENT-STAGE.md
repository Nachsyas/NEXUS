# CURRENT STAGE: Milestone M2 Implementation Complete (Pending PR Merge)

**Current Stage:** Milestone M2 (Projects Domain Foundation) — IMPLEMENTATION COMPLETE ON `milestone/m2-projects`  
**Phase:** Phase 1 (Core Personal Intelligence System)  
**Production NEXUS Implementation:** M1 Identity + M2 Projects Subsystems Established & Verified  
**M2 Implementation Status:** COMPLETE ON `milestone/m2-projects`  
**M2 Integration to Main:** PENDING PR MERGE  
**Live Apple E2E Status:** `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED` (Offline mock verifier 100% automated coverage; production verifier code complete)  
**Next Stage:** Milestone M3 (Memory Core) — PENDING PR MERGE & EXPLICIT USER AUTHORIZATION  

---

## 1. Stage Objectives & Accomplishments (Milestone M2)
Milestone M2 established the canonical Projects domain across backend services, REST endpoints, database schema, and iOS client integration.

### Completed Deliverables:
- [x] **Canonical Domain Models & Separation:** `Project` and `ProjectTechnology` models with RFC 9562 UUIDv7 primary keys.
- [x] **Database Schema & Migrations:** Created `projects`, `project_technologies`, and added `default_project_id` FK to `user_preferences` via Alembic migration `0003_projects_and_technologies.py`. Forward and rollback migrations fully verified.
- [x] **Database Invariants Enforced:**
  - `uq_projects_user_slug`: Unique slug per user.
  - `chk_projects_progress_bounds`: Progress validated between 0 and 100.
  - `uq_projects_user_active`: Partial unique index guaranteeing at most one active project per user.
  - `uq_project_technologies_project_name`: Unique technology names within a project.
  - `fk_user_preferences_default_project_id`: Referential integrity with `ON DELETE SET NULL`.
- [x] **Slug Strategy:** Pure-Python Unicode-safe deterministic slug generator with NFKD normalization and safe per-user collision handling (`slug-2`, `slug-3`).
- [x] **Multi-Tenant Isolation & Anti-IDOR:** Strict ownership checks (`WHERE id = :id AND user_id = :user_id`) on all operations. Access to cross-user projects returns 404 Not Found to prevent existence probing.
- [x] **Active Focus Invariant:** Single-transaction deactivation of prior active project and activation of target project. Backed by PostgreSQL partial unique index.
- [x] **Soft Archiving:** Setting `status = ARCHIVED`, `is_active = false`, and recording `archived_at`. Default listings exclude archived projects unless `include_archived=true`.
- [x] **M2 Context Foundation Endpoint:** `GET /api/v1/projects/{project_id}/context` returns deterministic project metadata without invoking any M3+ memory, AI, or retrieval subsystems.
- [x] **RESTful API Surface:** 7 endpoints under `/api/v1/projects` implemented with RFC-compliant response envelopes and bounded pagination (`limit <= 100`).
- [x] **iOS Client Architecture:**
  - `ProjectModels.swift`: Swift domain models and payloads.
  - `NexusAPIClient.swift`: Added 7 typed networking methods with fractional-second ISO8601 date decoding.
  - `ProjectManager.swift`: Observable state store managing projects, active focus, loading state, and error handling.
  - `ProjectsListView.swift`, `CreateProjectSheet.swift`, `ProjectDetailView.swift`: SwiftUI views for browsing, creating, inspecting, activating, and archiving projects.
  - `ContentView.swift`: Authenticated TabView navigation between Projects and Account.
- [x] **Target Compilation:** iOS target builds cleanly (`** BUILD SUCCEEDED **`); macOS agent regression builds cleanly (`Build complete!`).
- [x] **Automated Tests:** 36/36 backend tests passing cleanly in 2.34s (13 dedicated project domain tests).
- [x] **Quality Tooling:** Ruff check, Ruff format check, and Mypy strict mode 100% passing across 37 source files.
- [x] **Stage Documentation:** All 12 files completed in canonical path `docs/stages/phase-1/M2-projects/`.

---

## 2. Milestone M1 Foundation (Preserved Baseline)
- All M1 deliverables (Apple Sign In, sessions, refresh token rotation, user preferences) remain operational and fully regression tested.
- `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED` remains documented until physical hardware testing.

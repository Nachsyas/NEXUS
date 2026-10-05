# Stage M2: Projects Domain Foundation

## Milestone Overview
- **Milestone Code:** M2
- **Milestone Name:** Projects Domain Foundation
- **Phase:** Phase 1 — Core Personal Intelligence System
- **Status:** IMPLEMENTATION COMPLETE — PENDING PR MERGE
- **Governance:** ADR-001 (Modular Monolith), ADR-002 (PostgreSQL + pgvector), ADR-006 (RFC 9562 UUIDv7), ADR-020 (Session Security)
- **Lead Agent:** Antigravity (Autonomous Execution)

## Objective
Establish the canonical multi-tenant Projects domain for NEXUS. Projects represent persistent, isolated context workspaces belonging to a single user. Every higher-level milestone (M3 Memory Core, M4 Goal Engine, M5 Context Engine, and M6 Device Mesh) mounts its context and operations on top of this foundation. M2 establishes project identity, ownership invariants, active focus management, technology tagging, deterministic slug generation, coarse progress tracking, and structured metadata context retrieval without prematurely introducing intelligence systems.

## Scope Delivered
1. **Core Database Schema & Migrations:**
   - PostgreSQL 16 schema with UUIDv7 primary keys via RFC 9562 (`uuid6.uuid7`).
   - Tables: `projects`, `project_technologies`.
   - Constraints:
     - `uq_projects_user_slug`: `UNIQUE (user_id, slug)`
     - `chk_projects_progress_bounds`: `CHECK (progress >= 0 AND progress <= 100)`
     - `uq_projects_user_active`: `UNIQUE (user_id) WHERE is_active = true` (Partial unique index)
     - `uq_project_technologies_project_name`: `UNIQUE (project_id, name)`
     - `fk_user_preferences_default_project_id`: Foreign key on `user_preferences.default_project_id` referencing `projects.id` with `ON DELETE SET NULL`.
   - Migration `0003_projects_and_technologies.py` validated forward and backward (`downgrade -1` / `upgrade head`).
2. **Backend Domain Architecture:**
   - Modular monolith domain `backend/app/domains/projects` containing `models.py`, `schemas.py`, `service.py`, `exceptions.py`.
   - Pure-Python deterministic slugification with Unicode NFKD normalization and safe per-user collision suffixing (`slug`, `slug-2`, `slug-3`).
   - Strict tenant isolation: every query is scoped by `user_id`. IDOR requests return 404 to avoid leaking existence.
   - Atomic focus activation: single-transaction deactivation of prior active project and activation of target project, guaranteed by database partial unique index.
   - Deterministic project context metadata foundation (`/api/v1/projects/{project_id}/context`) returning metadata without M3+ memory or AI entities.
3. **RESTful API Surface (`/api/v1/projects`):**
   - `POST /api/v1/projects`: Create project with technologies.
   - `GET /api/v1/projects`: Bounded, paginated listing with status and active filtering.
   - `GET /api/v1/projects/{id}`: Detailed project retrieval with eager-loaded technologies.
   - `PATCH /api/v1/projects/{id}`: Selective updates preserving slug stability.
   - `POST /api/v1/projects/{id}/activate`: Idempotent active project focus assignment.
   - `POST /api/v1/projects/{id}/archive`: Soft archive setting status to ARCHIVED, clearing active state, recording `archived_at`.
   - `GET /api/v1/projects/{id}/context`: Deterministic context metadata endpoint.
4. **iOS Client Experience:**
   - `ProjectModels.swift`: Swift Codable domain structs and enums.
   - `NexusAPIClient.swift`: URLSession API methods for all project operations.
   - `ProjectManager.swift`: MainActor observable state store managing projects, active focus, loading state, and error handling.
   - `ProjectsListView.swift`: Tab-based navigation, active focus banner, project listing, pull-to-refresh, swipe actions (activate/archive).
   - `CreateProjectSheet.swift`: Clean form with sliders, pickers, and technology tag input.
   - `ProjectDetailView.swift`: Detailed view displaying metadata, progress, technologies, M2 context foundation, and action controls.
   - `ContentView.swift`: Tab navigation linking Projects and Account once authenticated.
5. **Quality Gates & Regression:**
   - 36/36 backend tests passing (including 13 dedicated M2 project tests).
   - Ruff linting & formatting 100% clean.
   - Mypy strict type checking 100% clean.
   - iOS Simulator build (`xcodebuild`) SUCCEEDED.
   - Mac Agent regression build (`swift build`) SUCCEEDED.

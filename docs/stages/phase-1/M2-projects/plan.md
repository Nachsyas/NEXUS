# Milestone M2 Plan: Projects Domain Foundation

## 1. Objectives & Approach
1. **Model & Migration Design:**
   - Define `Project` and `ProjectTechnology` models in `backend/app/domains/projects/models.py`.
   - Implement PostgreSQL constraints: `uq_projects_user_slug`, `chk_projects_progress_bounds`, partial unique index `uq_projects_user_active`, and technology uniqueness.
   - Update `UserPreference` with `default_project_id` foreign key.
   - Author and test Alembic migration `0003_projects_and_technologies.py`.
2. **Business Logic & Service Layer:**
   - Implement pure-Python deterministic `slugify` with Unicode normalization and per-user collision suffixing.
   - Implement `ProjectService` with strict `user_id` ownership filtering.
   - Implement atomic project activation in a single database transaction.
   - Implement soft archiving lifecycle (`status = ARCHIVED`, `is_active = false`, `archived_at = now()`).
   - Implement eager relationship loading (`selectinload`) to eliminate N+1 queries and avoid async greenlet exceptions.
   - Implement deterministic context foundation endpoint returning project metadata with `memory_count = 0` and `knowledge_count = 0`.
3. **Transport & Routing:**
   - Create `backend/app/api/v1/projects.py` with 7 endpoints.
   - Register router in `backend/app/api/v1/router.py`.
   - Register domain exception handlers in `backend/app/main.py`.
4. **Backend Test Suite:**
   - Create comprehensive test suite in `backend/tests/test_projects.py` covering creation, ownership, IDOR, slug collisions, activation invariants, concurrency, archiving, progress validation, and pagination.
5. **iOS Client Layer:**
   - Implement domain models in `apps/ios/NEXUS/Domain/Projects/ProjectModels.swift`.
   - Extend `NexusAPIClient` with project networking methods.
   - Implement `@MainActor ProjectManager: ObservableObject`.
   - Implement SwiftUI views: `ProjectsListView`, `CreateProjectSheet`, `ProjectDetailView`.
   - Connect authenticated state in `ContentView.swift`.
6. **Validation & Stage Evidence:**
   - Run ruff, mypy, pytest, xcodebuild, and swift build.
   - Generate all 12 stage documentation files.
   - Sync API contract and context handoff files.
   - Commit, push branch `milestone/m2-projects`, and open Pull Request.

# Milestone M2: Files Changed

## 1. Backend Domain & API

### Created:
- `backend/app/domains/projects/__init__.py`: Domain package exports.
- `backend/app/domains/projects/exceptions.py`: Custom domain exceptions (`ProjectError`, `ProjectNotFoundError`, `ProjectSlugConflictError`, `ProjectInvalidStateError`).
- `backend/app/domains/projects/models.py`: SQLAlchemy models `Project` and `ProjectTechnology`, enums `ProjectStatus` and `ProjectPriority`, and constraints.
- `backend/app/domains/projects/schemas.py`: Pydantic request/response schemas for project lifecycle and context.
- `backend/app/domains/projects/service.py`: Business logic, deterministic slugification, ownership scoping, eager loading, and activation transactions.
- `backend/app/api/v1/projects.py`: FastAPI router implementing 7 RESTful endpoints.
- `backend/alembic/versions/0003_projects_and_technologies.py`: Alembic migration script for tables, indexes, constraints, and foreign keys.
- `backend/tests/test_projects.py`: Comprehensive test suite with 13 test functions.

### Modified:
- `backend/alembic/env.py`: Imported `Project` and `ProjectTechnology` models for metadata discovery.
- `backend/app/api/v1/router.py`: Registered `projects_router` under `/projects` prefix.
- `backend/app/domains/users/models.py`: Added `default_project_id` foreign key reference to `projects.id` and `User.projects` relationship.
- `backend/app/main.py`: Registered `ProjectError` exception handler with RFC error envelope formatting.

## 2. iOS Application

### Created:
- `apps/ios/NEXUS/Domain/Projects/ProjectModels.swift`: Swift domain models, enums, payloads, and context representation.
- `apps/ios/NEXUS/Domain/Projects/ProjectManager.swift`: MainActor observable state store for projects and active focus.
- `apps/ios/NEXUS/Features/Projects/CreateProjectSheet.swift`: SwiftUI modal sheet for project creation.
- `apps/ios/NEXUS/Features/Projects/ProjectDetailView.swift`: Detailed project view with active badge, progress, technologies flow layout, and context foundation.
- `apps/ios/NEXUS/Features/Projects/ProjectsListView.swift`: Main projects view with active focus card, list rows, pull-to-refresh, and swipe actions.

### Modified:
- `apps/ios/NEXUS/App/ContentView.swift`: Added `TabView` coordinating `ProjectsListView` and `AuthView` upon authentication.
- `apps/ios/NEXUS/Data/Network/NexusAPIClient.swift`: Added 7 typed networking methods for project operations.
- `apps/ios/NEXUS/Domain/Auth/AuthManager.swift`: Exposed `currentAccessToken` property for authenticated feature navigation.
- `apps/ios/NEXUS/Features/Auth/AuthView.swift`: Added `onLogout` callback to safely clear project state upon session termination.

## 3. Documentation & Evidence

### Created:
- `docs/stages/phase-1/M2-projects/README.md`
- `docs/stages/phase-1/M2-projects/plan.md`
- `docs/stages/phase-1/M2-projects/implementation-log.md`
- `docs/stages/phase-1/M2-projects/files-changed.md`
- `docs/stages/phase-1/M2-projects/commands-run.md`
- `docs/stages/phase-1/M2-projects/test-results.md`
- `docs/stages/phase-1/M2-projects/performance-results.md`
- `docs/stages/phase-1/M2-projects/security-review.md`
- `docs/stages/phase-1/M2-projects/architecture-review.md`
- `docs/stages/phase-1/M2-projects/deviations.md`
- `docs/stages/phase-1/M2-projects/known-issues.md`
- `docs/stages/phase-1/M2-projects/completion-report.md`

### Modified:
- `docs/api/api-contract.md`: Updated Section 3 with live Projects API endpoints and schemas.
- `docs/context/PROJECT-STATE.md`: Recorded M2 completion status.
- `docs/context/CURRENT-STAGE.md`: Updated active stage to M2 completion and PR verification.
- `docs/context/NEXT-ACTIONS.md`: Formulated next steps for PR review and M3 preparation.
- `docs/context/HANDOFF.md`: Updated agent handoff state.

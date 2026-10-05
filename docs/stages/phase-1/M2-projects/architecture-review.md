# Stage M2: Architecture Review

## Architectural Evaluation

### 1. Modular Monolith Alignment (ADR-001)
- **Domain Encapsulation:** The Projects domain is strictly isolated inside `backend/app/domains/projects/`. All internal business logic, database queries, and slug algorithms reside in `ProjectService`.
- **Independence from Intelligence Layers:** Projects does NOT import or depend on Memory Core (M3), AI Conversation (M4), Context Engine (M5), or Device Pairing (M6). Future milestones will depend on Projects for context scoping, preserving a unidirectional dependency hierarchy:
  ```
  [Device Pairing (M6)]
            │
            ▼
  [Context Engine (M5)]
            │
            ▼
  [AI Conversation (M4)]
            │
            ▼
  [Memory Core (M3)]
            │
            ▼
  [Projects Domain (M2)]
            │
            ▼
  [Identity & Users (M1)]
  ```
- **Cross-Domain Reference via Service Layer:** In `backend/app/domains/users/service.py`, `UserService.update_user_preferences` verifies that `default_project_id` references a project owned by the authenticated user using `select(Project.id).where(Project.id == target, Project.user_id == user_id)`. Non-owned or non-existent projects trigger `ProjectNotFoundError`, preventing cross-tenant leakage.

### 2. Relational Schema & Persistence (ADR-002, ADR-006)
- **Primary Keys:** RFC 9562 UUIDv7 (`uuid6.uuid7`) generated at model creation for time-ordered locality in B-Tree indexes.
- **Foreign Key Cascades:** `projects.user_id -> users.id` with `ON DELETE CASCADE`. `project_technologies.project_id -> projects.id` with `ON DELETE CASCADE`.
- **User Preference Reference:** `user_preferences.default_project_id -> projects.id` with `ON DELETE SET NULL`. Migration `0003` includes safe cleanup for orphaned references prior to foreign key creation.
- **Constraints & Indexes:**
  - `uq_projects_user_slug`: Enforces slug uniqueness per tenant. Bounded retry loop (5 attempts) with nested savepoints prevents raw 500 errors on concurrent creation.
  - `chk_projects_progress_bounds`: Validates progress is between 0 and 100 at the DB engine level.
  - `uq_projects_user_active`: Partial unique index `UNIQUE (user_id) WHERE is_active = true` guarantees that no tenant can ever possess more than one active project.
  - Serialization: `ProjectService.activate_project` executes `select(User.id).where(User.id == user_id).with_for_update()` to prevent race conditions during concurrent activation calls.

### 3. Context Boundary Defense
- **M2 Context Foundation:** The context endpoint `/api/v1/projects/{project_id}/context` is strictly confined to deterministic metadata (`project_id`, `name`, `slug`, `summary`, `status`, `priority`, `progress`, `is_active`, `active_technologies`).
- **No Premature Placeholders:** Placeholders for memory or knowledge counts have been removed to prevent prematurely freezing downstream API contracts.

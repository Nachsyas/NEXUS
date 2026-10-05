# Milestone M2: Architecture Review

## 1. Domain Separation & Modular Monolith Alignment
The Projects domain strictly respects the Modular Monolith architecture defined in ADR-001:
- **Clean Boundaries:** `backend/app/domains/projects` encapsulates all project entities, schemas, business logic, and exceptions.
- **Independence from Intelligence Layers:** Projects does NOT import or depend on Memory Core (M3), Goal Engine (M4), Context Engine (M5), or Device Mesh (M6). Future milestones will depend on Projects for context scoping, preserving a unidirectional dependency hierarchy:
  `M3 (Memory) -> M2 (Projects) -> M1 (Users & Identity) -> M0 (Foundation)`
- **RFC Envelope Integrity:** All 7 RESTful endpoints return responses enveloped inside `{ "success": true, "data": ..., "error": null, "meta": ... }`. Errors use typed application exceptions (`ProjectError` family) with RFC-compliant error envelopes and numeric status codes.

## 2. Invariant Architecture
1. **One Active Project per User:**
   - Enforced at the persistence layer using PostgreSQL partial unique index `uq_projects_user_active`.
   - Guaranteed at the application service layer via atomic transactions.
2. **Per-User Slug Uniqueness:**
   - Slugs are scoped per user via unique constraint `(user_id, slug)`.
   - Generated using Unicode NFKD normalization with deterministic collision suffixes (`-2`, `-3`).
3. **Referential Integrity:**
   - `User.projects` cascade on delete.
   - `Project.technologies` cascade on delete.
   - `UserPreference.default_project_id` foreign key sets null on delete (`ON DELETE SET NULL`), preventing cascading destruction of user profile settings.

## 3. iOS Client Architecture
- **Layer Separation:**
  - Network transport: `NexusAPIClient` protocol-backed URLSession layer.
  - State management: `@MainActor ProjectManager: ObservableObject`.
  - Presentation: Lightweight SwiftUI views (`ProjectsListView`, `ProjectDetailView`, `CreateProjectSheet`).
- **No Mock in Production:** Production views interact directly with `NexusAPIClient` initialized against the configured base URL.
- **Session Preservation:** Authenticated access tokens are read securely from Keychain without saving tokens in user defaults or memory caches.

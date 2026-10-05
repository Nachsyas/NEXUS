# Milestone M2: Security Review

## 1. Threat Modeling & Verification

### 1.1 Insecure Direct Object Reference (IDOR)
- **Threat:** Malicious authenticated User A attempts to view, update, activate, archive, or retrieve the context of a project belonging to User B by supplying User B's UUID.
- **Mitigation:**
  - Every SQL query in `ProjectService` enforces `WHERE projects.id = :id AND projects.user_id = :user_id`.
  - When a project does not exist under the caller's `user_id`, the service raises `ProjectNotFoundError`, which translates to `404 Not Found`.
  - Returning 404 rather than 403 prevents attackers from probing the system to confirm whether a specific project ID exists.
- **Verification:** Proven in `test_cross_user_isolation_and_idor`.

### 1.2 Mass Assignment & Tenant Injection
- **Threat:** Client supplies `user_id`, `id`, `slug`, or timestamps in the request body to reassign project ownership or manipulate audit fields.
- **Mitigation:**
  - `ProjectCreate` and `ProjectUpdate` schemas omit `user_id`, `id`, `slug`, `created_at`, `updated_at`, and `archived_at`.
  - The server explicitly sets `user_id = user.user_id` from the cryptographically verified JWT context (`UserContext`).
  - Slugs are generated server-side through NFKD normalization.
- **Verification:** Proven in schema validation and unit tests.

### 1.3 State Invariant & Concurrency Exploits
- **Threat:** An attacker sends concurrent activation requests in an attempt to activate two projects simultaneously for a single user account.
- **Mitigation:**
  - Database engine enforces partial unique index:
    `CREATE UNIQUE INDEX uq_projects_user_active ON projects (user_id) WHERE is_active = true;`
  - In addition, the application executes project deactivation and activation inside an atomic SQL transaction block.
- **Verification:** Proven in `test_concurrent_activation_safety`.

### 1.4 Denial of Service via Large Payloads & Pagination
- **Threat:** Client requests millions of projects or sends thousands of technology tags to exhaust server memory and bandwidth.
- **Mitigation:**
  - Listing endpoint bounds pagination: `limit` parameter is capped at 100 via Pydantic `Query(le=100)`.
  - Technology tags are constrained in length and deduplicated.
- **Verification:** Proven in `test_project_pagination_and_filtering`.

### 1.5 Soft Archiving Integrity
- **Threat:** Archiving a project allows it to remain the active contextual focus or allows active projects to be bypassed.
- **Mitigation:**
  - `archive_project` explicitly verifies `is_active = false` and sets `archived_at = now()`.
  - `activate_project` explicitly rejects archived projects with `ProjectInvalidStateError` (HTTP 400).
- **Verification:** Proven in `test_project_archiving_flow`.

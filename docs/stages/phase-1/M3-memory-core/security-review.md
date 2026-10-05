# Milestone M3 Security Review: Memory Core & Secret Safety

## 1. NEVER_STORE Policy Enforcement
- **Objective:** Prevent accidental or malicious persistence of high-entropy credentials, private keys, authentication tokens, and passwords in the companion memory store.
- **Enforcement Architecture (Design Invariant):**
  - Pre-persistence validation via `MemorySafetyPolicy.validate()` strictly runs before database insertion or updates.
  - Pattern matchers reject:
    - PEM Private Keys (`-----BEGIN ... PRIVATE KEY-----`).
    - Bearer tokens & JWTs (`eyJ...`).
    - Vendor API keys: OpenAI (`sk-...`), GitHub (`ghp_...`, `github_pat_...`), AWS (`AKIA...`).
    - Assignment heuristics for passwords, credentials, OTP codes, and seed phrases.
  - Pre-validation secret redaction: global `RequestValidationError` handler in `backend/app/main.py` deliberately omits raw user `input` from 422 validation error bodies to prevent secret leakage on malformed requests.
  - Error responses emit generic `MEMORY_SECRET_REJECTED` code without reflecting matched candidate secrets.
  - Structured audit telemetry records `memory_rejected_by_safety_policy` with event-level metadata and zero payload content.
- **Verification (Test Evidence):**
  - Evaluated against the explicit synthetic credential-pattern test matrix (`test_never_store_secret_safety_policy`, `test_pre_validation_secret_redaction`).
  - No candidate secret reflection observed across the current explicit synthetic test matrix and validation pathways.
  - Evaluated against benign text: discussions of cryptographic concepts, password managers, and JWT session mechanics show no false positives observed in the current benign test matrix.

## 2. Multi-Tenant Authorization & IDOR Protection
- **Ownership Invariants (Design Invariant):**
  - Every memory record is bound to a tenant `user_id`.
  - All read, write, update, forget, and search operations enforce explicit `Memory.user_id == current_user.user_id` predicates.
  - Access to nonexistent or other users' memories consistently returns HTTP 404 (`MEMORY_NOT_FOUND`) rather than 403, preventing resource enumeration.
- **Project Scoping Invariants (Design Invariant):**
  - Attaching a project-scoped memory requires verifying that the target project exists and belongs to the authenticated user.
  - Attempting to attach memory to another user's project returns HTTP 404 (`PROJECT_NOT_FOUND`).
- **Verification (Test Evidence):**
  - Verified across `test_multi_tenant_isolation_and_idor` and `test_project_memory_scope_invariants`.

## 3. Concurrency & Integrity Controls
- **User Row-Level Lock (Design Invariant):**
  - Writes acquire `SELECT id FROM users WHERE id = :user_id FOR UPDATE` to serialize concurrent requests from the same user.
  - Eliminates race conditions between simultaneous deduplication checks and superseding updates.
- **Verification (Test Evidence):**
  - Verified across `test_concurrent_identical_writes` and `test_concurrent_conflicting_writes`.

## 4. Embedding Vector & Payload Invariants
- **Vector Dimension Boundary:**
  - Runtime validation enforces `expected_dim == provider.dimension` for all generated embeddings.
  - Flat exact vector scans in PostgreSQL include `func.vector_dims(Memory.embedding) == expected_dim` to safely filter out incompatible dimensions without database operator errors.
- **Payload Bounds:**
  - `value_text` is bounded to 1..10000 characters.
  - `value_json` is bounded to 64 KB serialized bytes and nesting depth 5.

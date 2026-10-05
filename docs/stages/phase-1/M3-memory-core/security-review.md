# Milestone M3 Security Review: Memory Core & Secret Safety

## 1. NEVER_STORE Policy Enforcement
- **Objective:** Prevent accidental or malicious persistence of high-entropy credentials, private keys, authentication tokens, and passwords in the companion memory store.
- **Pattern Matchers:**
  - PEM Private Keys (`-----BEGIN ... PRIVATE KEY-----`).
  - Bearer tokens & JWTs (`eyJ...`).
  - Vendor API keys: OpenAI (`sk-...`), GitHub (`ghp_...`, `github_pat_...`), AWS (`AKIA...`).
  - Assignment heuristics for passwords, credentials, OTP codes, and seed phrases.
- **Verification:**
  - Evaluated against standard credential datasets.
  - Zero leakage verified: error responses return generic `MEMORY_SECRET_REJECTED` code without reflecting matched text.
  - Zero log leakage: logger emits structured telemetry (`memory_rejected_by_safety_policy`) with no payload details.
  - Evaluated against benign text: discussions of cryptographic concepts, password managers, and JWT session mechanics pass without false positives.

## 2. Multi-Tenant Authorization & IDOR Protection
- **Ownership Invariants:**
  - Every memory record is tied to `user_id`.
  - All read, write, update, forget, and search operations include explicit `Memory.user_id == current_user.user_id` predicates.
  - Access to nonexistent or other users' memories consistently returns HTTP 404 (`MEMORY_NOT_FOUND`) rather than 403, preventing resource enumeration.
- **Project Scoping Invariants:**
  - Attaching a project-scoped memory requires verifying that the target project exists and belongs to the authenticated user.
  - Attempting to attach memory to another user's project returns HTTP 404 (`PROJECT_NOT_FOUND`).

## 3. Concurrency & Integrity Controls
- **User Row-Level Lock:**
  - Writes acquire `SELECT id FROM users WHERE id = :user_id FOR UPDATE` to serialize concurrent requests from the same user.
  - Eliminates race conditions between simultaneous deduplication checks and superseding updates.

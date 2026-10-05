# Milestone M3 Architecture Review: Memory Core & Semantic Storage

## 1. Domain Modeling & Schema
- **Entity Identity & Lifecycle:**
  `Memory` represents curated, high-salience knowledge triples (`subject`, `predicate`, `value_text`, optional `value_json`).
  Primary key uses RFC 9562 UUIDv7. Status lifecycle transitions:
  - `ACTIVE` -> default operational state for newly created memories.
  - `SUPERSEDED` -> when a newer memory replaces an existing memory with identical identity triple.
  - `EXPIRED` -> when `expires_at <= now()`.
  - `FORGOTTEN` -> user-initiated deletion (soft deletion that preserves auditability while completely excluding from active retrieval).
  - `PENDING_CONFIRMATION` -> reserved for autonomous agent extraction requiring user confirmation.
- **Taxonomy Enforcement:**
  Personal memory types (`PERSONAL_FACT`, `PREFERENCE`, `INTEREST`, `SKILL`, `GOAL`, `BEHAVIOR_PATTERN`) require `project_id = null`.
  Project memory types (`PROJECT_FACT`, `PROJECT_DECISION`, `PROJECT_PROGRESS`, `PROJECT_NEXT_ACTION`) require a valid `project_id` owned by the caller.
  Generic catch-all types are forbidden at schema validation level.

## 2. Concurrency & Deduplication Architecture
- **Per-User Write Serialization & Transaction Boundaries:**
  In concurrent environments, multiple calls attempting to write identical or conflicting memories could create race conditions.
  `MemoryService` executes `SELECT id FROM users WHERE id = :user_id FOR UPDATE` before querying existing active memories.
  This serializes concurrent mutations for a single tenant without blocking other tenants.
  `MemoryService` delegates transaction commits to the API / unit-of-work layer (`get_db` and router), utilizing `db.flush()` internally to support composable multi-domain transactions.
- **Deterministic Identity & Bounded Hash (identity_hash):**
  Incoming subject and predicate are normalized (`NFKD`, lowercase, stripped) and deterministically encoded into a canonical JSON array `[norm_subject, norm_predicate]` hashed with SHA-256 into `identity_hash` (`CHAR(64)`).
  This eliminates index entry size overflows from Unicode normalization expansion while supporting fast composite index lookups via `ix_memories_identity_lookup` on `(user_id, project_id, memory_type, identity_hash, status)`.
  A defensive in-memory check confirms exact normalized text equivalence against rare hash collision.
- **Deterministic Deduplication:**
  If an active memory exists with the matching `identity_hash` and identical normalized value, the existing row is returned without duplicate insertion.
- **Supersede Mechanism:**
  When an incoming memory matches the `identity_hash` but provides a different value, the existing memory is updated to `status = 'SUPERSEDED'`, `superseded_by = :new_id`, and the new memory is inserted as `ACTIVE`.

## 3. Vector Storage & Provider Boundary (TBD-004)
- **Database Column:**
  `embedding` is stored as unconstrained `Vector()` using `pgvector.sqlalchemy`, avoiding premature dimension locking.
- **Search Operator:**
  Cosine distance `<=>` is executed via SQLAlchemy (`Memory.embedding.cosine_distance(query_vector)`).
  Similarity score is derived as `max(0.0, min(1.0, 1.0 - distance))`.
- **Provider Protocol:**
  Per ADR-004 and ADR-011, production embedding generation is decoupled behind `EmbeddingProvider`.
  In production, until governance resolves `TBD-004`, `UnavailableEmbeddingProvider` raises `EmbeddingUnavailableError` (HTTP 503).
  For automated integration testing, `DeterministicTestEmbeddingProvider` computes unit-normalized 1536-dimensional vectors deterministically via SHA-512/SHA-256 digests. Vector validation layer (`validate_embedding_vector`) strictly verifies non-emptiness, finiteness, and dimension consistency without exposing raw vector data.
- **Index Strategy (TBD-025):**
  Per `TBD-025`, no premature HNSW or IVFFlat index is created; flat exact scan is maintained for initial scale.

## 4. Security Architecture (NEVER_STORE Policy)
- **Scanning Engine:**
  `MemorySafetyPolicy` validates all candidate memories before persistence.
  High-confidence regex rules detect private keys, JWTs, Bearer authorization tokens, API keys (OpenAI, GitHub, AWS), password assignments, OTP assignments, and recovery seed phrases.
- **Leakage Prevention:**
  If a secret pattern matches, `MemorySecretRejectedError` (HTTP 400 `MEMORY_SECRET_REJECTED`) is thrown.
  The candidate secret is NEVER logged, NEVER echoed in error messages, and NEVER written to disk.
- **Multi-Tenant Scoping:**
  All read, write, update, forget, and search operations include strict `user_id == current_user.user_id` predicates. Cross-tenant access attempts return HTTP 404 (safe IDOR protection).

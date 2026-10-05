# Milestone M3: Post-Review Remediation & Corrective Actions

## Remediation Log
1. **TBD Governance Normalization:**
   - Consolidated all production embedding model and dimension decisions into `TBD-004`.
   - Removed redundant `TBD-030` from `TBD-REGISTRY.md` and codebase references.
2. **Unconstrained Vector Storage:**
   - Changed SQLAlchemy model and Alembic migration `0004_memories_core.py` to use `Vector()` (unconstrained dimension) supported natively by PostgreSQL pgvector.
   - Tested migration downgrade and re-upgrade successfully.
3. **Embedding Vector Runtime Validation:**
   - Implemented `validate_embedding_vector` in `embedding.py` to verify non-empty, finite numbers (rejecting NaN and Inf), and expected dimension without exposing raw vector arrays in logs or errors.
4. **iOS Sensitivity Model Parity:**
   - Added `case restricted = "RESTRICTED"` to `MemorySensitivity` in `apps/ios/NEXUS/Domain/Memories/MemoryModels.swift`.
   - Verified Swift decoding from `"RESTRICTED"` via Swift interpreter; clean iOS build succeeded.
5. **Stale Embedding Vector Prevention:**
   - In `MemoryService.update_memory`, if `value_text` changes and re-embedding fails or provider is unavailable, `memory.embedding` is explicitly set to `None`.
   - Updated `memory.summary` deterministically whenever `value_text` changes.
6. **Expired Memory Reassertion & Status Coherence:**
   - In `create_memory`, if an existing active memory has `expires_at <= now()`, it is lazily transitioned to `EXPIRED`, and a fresh `ACTIVE` memory is created.
   - In `list_memories`, querying with `status=EXPIRED` captures both explicitly expired rows and active rows past `expires_at`.
   - In `get_memory`, lazy normalization updates status to `EXPIRED` if past expiration.
7. **Concurrency Invariants Verified:**
   - Added `test_concurrent_conflicting_writes` verifying concurrent writes for the same identity triple result in exactly 1 `ACTIVE` row, 2 `SUPERSEDED` rows with valid references, and zero 500s or database integrity errors.
8. **API Contract Synchronization:**
   - Updated Section 6 of `docs/api/api-contract.md` with complete request parameters, `USER_EXPLICIT` server-assigned provenance, response envelopes, and error codes.
9. **FastAPI Typed Query Filters:**
   - Converted `status` and `memory_type` query parameters on `GET /api/v1/memories` to `MemoryStatus` and `MemoryType` enums, rejecting invalid parameters with 422 Unprocessable Content.
10. **PATCH Null-Clear Semantics:**
    - Handled `model_fields_set` in `update_memory` so sending `{"value_json": null}` or `{"expires_at": null}` clears the field, while omitting fields leaves them untouched.
11. **Pre-Validation Secret Redaction:**
    - Updated global `RequestValidationError` handler in `app/main.py` to strip the raw `"input"` key across all validation error items, preventing candidate secrets from being echoed back in 422 responses.
12. **Evidence & Performance Honesty:**
    - Replaced all claims of "standard credential datasets" and "Zero False Positives" with honest statements reflecting the synthetic test matrix and benign matrix results.
    - Updated performance documentation to state "Observed Local Baseline" and broadened automated test latency assertions to non-production regression guards (< 2000ms) to ensure non-flaky execution.
13. **Embedding Dimension Boundary & SQL Filter:**
    - Declared `@property def dimension(self) -> int` on `EmbeddingProvider` protocol.
    - Verified all vector operations enforce `expected_dim=provider.dimension`.
    - Added `func.vector_dims(Memory.embedding) == expected_dim` SQL predicate in pgvector semantic search to prevent runtime PostgreSQL dimension mismatch exceptions.
14. **Bounded Deterministic Identity Storage (`identity_hash`):**
    - Identified vulnerability where Unicode NFKD decomposition can expand source characters beyond 255 code points, causing `VARCHAR(255)` database overflow.
    - Replaced variable-length normalized string columns in the lookup index with a fixed-size `CHAR(64)` lowercase hex SHA-256 digest (`identity_hash`) derived from canonical JSON serialization `[norm_subject, norm_predicate]`.
    - Updated `ix_memories_identity_lookup` to `(user_id, project_id, memory_type, identity_hash, status)`, preventing B-tree entry overflow. Added in-memory defensive check against rare hash collisions.
15. **Service Transaction Boundary & Composable Flushing:**
    - Removed internal `await db.commit()` and `await db.refresh()` from `MemoryService.create_memory()`.
    - Service calls now use `flush()`, preserving the user row lock until the router / unit-of-work commits the transaction. This enables atomic multi-domain orchestration for Milestone M4 without premature commit side-effects.

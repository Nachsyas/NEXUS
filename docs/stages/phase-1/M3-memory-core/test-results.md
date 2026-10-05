# Milestone M3 Test Results

## 1. Automated Test Summary
- **Backend Test Suite:** 54/54 passed
  - `tests/test_memories.py`: 17/17 passed
  - `tests/test_auth_identity.py`: 15/15 passed
  - `tests/test_projects.py`: 14/14 passed
  - `tests/test_health.py`: 2/2 passed
  - `tests/test_logging.py`: 2/2 passed
  - `tests/test_middleware.py`: 2/2 passed
  - `tests/test_startup.py`: 2/2 passed
- **Linter & Formatter (Ruff):** Clean pass (0 errors, 52 files checked).
- **Type Checker (Mypy):** Clean pass (0 errors in 46 source files).
- **iOS Simulator Target (`xcodebuild`):** Clean build succeeded (`** BUILD SUCCEEDED **`).
- **Mac Agent Target (`swift build`):** Clean build complete (0.80s).
- **iOS Contract Verification:** Swift decoding of `MemorySensitivity.restricted` from `"RESTRICTED"` verified; Xcode project has no separate XCTest target (documented as `NOT AUTOMATED` for XCTest suite, verified via clean build and runtime decoding script).

## 2. Memory Test Breakdown (`tests/test_memories.py`)
1. `test_anonymous_memory_access_rejected`: Verified 401 Unauthorized across all endpoints.
2. `test_memory_creation_and_attributes`: Verified UUIDv7, default values, user ownership, summary generation.
3. `test_all_10_canonical_memory_types`: Verified all 10 types pass; verified invented types (`FACT`, `NOTE`, `OTHER`) are rejected (422).
4. `test_project_memory_scope_invariants`: Verified scope constraints and cross-tenant project 404 safe rejection.
5. `test_never_store_secret_safety_policy`: Verified rejection of API keys, JWTs, passwords, private keys, OTPs, seed phrases without secret leakage; verified benign discussions pass without false positives in test matrix; verified `RESTRICTED` sensitivity persistence.
6. `test_pre_validation_secret_redaction`: Verified candidate secrets in malformed requests rejected by Pydantic v2 validation are completely stripped from 422 error response bodies.
7. `test_deterministic_deduplication`: Verified identical memory submissions reuse existing row without duplicate insertion.
8. `test_conflict_and_supersede`: Verified conflicting values transition old memory to `SUPERSEDED` and link `superseded_by`.
9. `test_concurrent_identical_writes`: Verified user row-level locking handles concurrent identical submissions cleanly (1 deduplicated row created).
10. `test_concurrent_conflicting_writes`: Verified concurrent submissions of conflicting values for the same identity triple result in exactly 1 `ACTIVE` row and 2 `SUPERSEDED` rows with valid references, zero 500s or DB integrity exceptions.
11. `test_expired_reassertion_and_status_coherence`: Verified reasserting an expired memory creates a fresh `ACTIVE` memory, lazily transitions the prior row to `EXPIRED`, and coherent query filtering for `status=EXPIRED`.
12. `test_typed_query_filters`: Verified FastAPI boundary enforces typed `MemoryStatus` and `MemoryType` filters, rejecting invalid parameters with 422.
13. `test_patch_nullable_semantics_and_stale_embedding_prevention`: Verified `model_fields_set` null-clearing for `value_json` and `expires_at`, and verified `memory.embedding` is set to `None` if re-embedding fails on `value_text` modification, preventing stale vector retention.
14. `test_forget_memory_semantics`: Verified `FORGOTTEN` status transition, exclusion from listings, and idempotent calls.
15. `test_multi_tenant_isolation_and_idor`: Verified cross-tenant GET, PATCH, FORGET return 404 safe IDOR.
16. `test_semantic_search_with_and_without_provider`: Verified 503 when provider is unconfigured, and accurate cosine similarity ranking when test provider is active.
17. `test_memory_performance_and_latency`: Broad sanity regression guard (< 2000ms) with observed local baseline (~10 - 45ms).

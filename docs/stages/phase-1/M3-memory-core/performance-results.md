# Milestone M3 Performance & Benchmark Results

## 1. Local Benchmark Measurements
Measured in `backend/tests/test_memories.py::test_memory_performance_and_latency` on Apple Silicon hardware with isolated local PostgreSQL 16 container (Observed Local Baseline / Non-Production Regression Guard):

| Operation | Observed Local Baseline | Test Regression Guard | Invariant Verification |
|---|---|---|---|
| Memory Create (with vector embedding) | ~25 - 45 ms | < 2000 ms (CI guard) | Verified |
| Deduplication Lookup | ~15 - 30 ms | < 2000 ms (CI guard) | Verified |
| Memory List (Bounded Pagination) | ~10 - 25 ms | < 2000 ms (CI guard) | Verified |
| Vector Similarity Search (Exact Scan) | ~15 - 35 ms | < 2000 ms (CI guard) | Verified |
| Forget Memory (State Transition) | ~10 - 20 ms | < 2000 ms (CI guard) | Verified |

> [!NOTE]
> NEXUS operates under a strict "MEASUREMENT FIRST" performance policy. Target production SLAs will be formally ratified after distributed multi-node benchmarks in subsequent milestones, rather than assuming unratified SLA targets during early foundational phases.

## 2. Query Optimization & Indexing
- **Composite Indexes Applied:**
  - `(user_id, status)` for fast active memory listing.
  - `(user_id, project_id, status)` for project context retrieval.
  - `(user_id, memory_type, status)` for type-filtered queries.
  - `(user_id, project_id, memory_type, identity_hash, status)` (`ix_memories_identity_lookup`) for compact, bounded deterministic deduplication and superseding queries.
  - `expires_at` for TTL exclusion filtering.
  - `(user_id, updated_at)` for recent memory ordering.
- **Index Strategy Decision (TBD-025):**
  - Per architecture guidelines, pgvector flat exact scan (`<=>`) filtered by `vector_dims` is used for initial dataset sizes.
  - HNSW or IVFFlat indexing will be benchmarked under realistic scale per `TBD-025`.

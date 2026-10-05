# Milestone M3 Performance & Benchmark Results

## 1. Local Benchmark Measurements
Measured in `backend/tests/test_memories.py::test_memory_performance_and_latency` on Apple Silicon:

| Operation | Latency (ms) | Target SLA (ms) | Status |
|---|---|---|---|
| Memory Create (with vector embedding) | ~25 - 45 ms | < 200 ms | PASS |
| Deduplication Lookup | ~15 - 30 ms | < 100 ms | PASS |
| Memory List (Bounded Pagination) | ~10 - 25 ms | < 100 ms | PASS |
| Vector Similarity Search (Exact Scan) | ~15 - 35 ms | < 150 ms | PASS |
| Forget Memory (State Transition) | ~10 - 20 ms | < 100 ms | PASS |

## 2. Query Optimization & Indexing
- **Composite Indexes Applied:**
  - `(user_id, status)` for fast active memory listing.
  - `(user_id, project_id, status)` for project context retrieval.
  - `(user_id, memory_type, status)` for type-filtered queries.
  - `expires_at` for TTL exclusion filtering.
  - `(user_id, updated_at)` for recent memory ordering.
- **Index Strategy Decision (TBD-025):**
  - Per architecture guidelines, pgvector flat exact scan is used for initial dataset sizes.
  - HNSW or IVFFlat indexing will be benchmarked under realistic scale per `TBD-025`.

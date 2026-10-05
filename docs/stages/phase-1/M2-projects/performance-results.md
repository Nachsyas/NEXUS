# Milestone M2: Performance Results

## 1. Test Methodology
- Environment: Local Docker PostgreSQL 16 container, Python 3.12 with async HTTPX ASGI test transport.
- Execution: 20 sequential requests per endpoint with real DB transactions, UUIDv7 generation, and JWT verification.
- Metrics Recorded: Mean, P95, Min, and Max response latency (milliseconds).

## 2. Benchmark Summary

| Endpoint / Operation | Sample Count | Mean Latency | P95 Latency | Min Latency | Max Latency |
|---|---|---|---|---|---|
| `POST /api/v1/projects` (Create with Techs) | 20 | 11.67 ms | 35.63 ms | 9.10 ms | 36.67 ms |
| `GET /api/v1/projects/{id}` (Get Single) | 20 | 6.67 ms | 14.32 ms | 5.24 ms | 14.62 ms |
| `GET /api/v1/projects` (List 20 Projects) | 20 | 11.78 ms | 23.11 ms | 8.33 ms | 23.44 ms |
| `POST /api/v1/projects/{id}/activate` (Focus Shift) | 20 | 11.69 ms | 20.61 ms | 8.59 ms | 20.83 ms |
| `GET /api/v1/projects/{id}/context` (Metadata) | 20 | 7.85 ms | 13.38 ms | 5.36 ms | 13.44 ms |

## 3. Query Efficiency & N+1 Prevention
- **Eager Loading Strategy:** `Project.technologies` is configured with `lazy="selectin"`. When projects are fetched in bulk or individually, SQLAlchemy issues a single primary query followed by a single batched `WHERE project_id IN (...)` query.
- **Index Utilization:**
  - `ix_projects_user_id`: Efficiently scopes all list and count queries per user.
  - `uq_projects_user_slug`: B-tree index provides O(log N) lookup for slug uniqueness checks.
  - `uq_projects_user_active`: Partial unique index provides instant lookup and engine-level uniqueness for active project determination without scanning inactive rows.
- **Transaction Footprint:** Project activation operates in an explicit single-transaction boundary:
  ```sql
  UPDATE projects SET is_active = false WHERE user_id = $1 AND is_active = true AND id != $2;
  UPDATE projects SET is_active = true, updated_at = now() WHERE id = $2 AND user_id = $1;
  COMMIT;
  ```

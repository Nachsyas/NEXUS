# Stage M2: Test Results & Execution Evidence

## Test Summary
- **Execution Date:** 2026-10-05
- **Test Runner:** `pytest` 9.1.1, `anyio` 4.15.1, `asyncio` 1.4.0
- **Python Version:** 3.12.14
- **Database:** PostgreSQL 16 (Local Docker Container)
- **Total Backend Tests:** 37
- **Passed:** 37
- **Failed:** 0
- **Pass Rate:** 100%

## M2 Project Domain Test Breakdown (`tests/test_projects.py`)

| Test Function | Description | Result |
| :--- | :--- | :--- |
| `test_anonymous_access_rejected` | Verifies all project endpoints reject unauthenticated requests with 401 | PASSED |
| `test_project_creation_and_ownership` | Verifies UUIDv7 generation, owner user_id binding, technologies creation | PASSED |
| `test_slug_generation_and_deterministic_collision` | Verifies deterministic per-user slug suffixing (`slug`, `slug-2`, `slug-3`) | PASSED |
| `test_concurrent_same_name_slug_creation` | Verifies concurrent creation of same-name projects via `asyncio.gather` with savepoint retries | PASSED |
| `test_cross_user_isolation_and_idor` | Verifies tenant isolation: GET, PATCH, activate, archive, context return 404 for foreign users | PASSED |
| `test_project_activation_flow_and_invariant` | Verifies single active focus assignment and deactivation of previous focus | PASSED |
| `test_concurrent_activation_safety` | Verifies concurrent activations via `asyncio.gather` and checks DB invariant `COUNT(is_active) == 1` | PASSED |
| `test_project_archiving_flow` | Verifies soft archiving, exclusion from default list, rejection of activation on archived | PASSED |
| `test_project_status_validation` | Verifies rejection of invalid status values with 422 | PASSED |
| `test_project_progress_validation` | Verifies rejection of progress out of bounds (<0 or >100) with 422 | PASSED |
| `test_project_technologies_deduplication_and_update`| Verifies case-insensitive deduplication and replacement of technologies | PASSED |
| `test_project_pagination_and_filtering` | Verifies limit, page, and max-limit (100) bounds | PASSED |
| `test_project_context_metadata_endpoint` | Verifies deterministic metadata context retrieval without M3+ memory placeholders | PASSED |
| `test_default_project_ownership_validation` | Verifies preferences default project validation, cross-user 404 rejection, and null clearing | PASSED |

## Client Verification
- **iOS Simulator Build:** `xcodebuild -project NEXUS.xcodeproj -scheme NEXUS -destination "generic/platform=iOS Simulator" clean build CODE_SIGNING_ALLOWED=NO` -> **BUILD SUCCEEDED**
- **Mac Agent Swift Build:** `cd apps/mac-agent && swift build` -> **Build complete!**
- **Migration Rollback & Re-apply:** `alembic downgrade -1 && alembic upgrade head` -> **SUCCESS**

# Milestone M3: Files Changed & Added

## Backend Domain & Migration
- `backend/alembic/versions/0004_memories_core.py`: Alembic migration for `memories` table with unconstrained `Vector()` pgvector column, normalized Unicode `identity_subject` and `identity_predicate` columns, and composite indexes (`ix_memories_identity_lookup`).
- `backend/app/domains/memories/models.py`: SQLAlchemy `Memory` model with `identity_subject` and `identity_predicate` columns, enums (`MemoryType`, `MemoryStatus`, `MemorySensitivity`, `MemorySourceType`), and composite index definitions.
- `backend/app/domains/memories/schemas.py`: Pydantic v2 schemas (`MemoryCreate`, `MemoryUpdate`, `MemoryResponse`, `MemorySearchRequest`, `MemorySearchHit`) with `value_text` bound (1..10000) and `value_json` safety bounds (max 64KB, max depth 5).
- `backend/app/domains/memories/exceptions.py`: Domain exception definitions (`MemoryNotFoundError`, `MemorySecretRejectedError`, `EmbeddingUnavailableError`, `EmbeddingValidationError`).
- `backend/app/domains/memories/safety.py`: `MemorySafetyPolicy` with regex scanning for NEVER_STORE credential policy and dictionary key scanning.
- `backend/app/domains/memories/embedding.py`: `EmbeddingProvider` protocol with `.dimension` property contract, `UnavailableEmbeddingProvider`, `DeterministicTestEmbeddingProvider`, and `validate_embedding_vector`.
- `backend/app/domains/memories/service.py`: `MemoryService` implementing CRUD, user row-level locking, Unicode-normalized deterministic deduplication, conflict superseding, lazy expiration normalization, stale embedding prevention, dimension validation, and pgvector cosine similarity search guarded by `func.vector_dims`.
- `backend/app/api/v1/memories.py`: FastAPI endpoints for `/api/v1/memories` with typed enum query filters.
- `backend/app/api/v1/router.py`: Registered `memories_router`.
- `backend/app/main.py`: Pre-validation secret redaction in `RequestValidationError` handler omitting raw input and sanitizing `ctx`.
- `backend/tests/test_memories.py`: 21 comprehensive test cases covering auth, schema invariants, NEVER_STORE policy, secret redaction, deduplication, conflict superseding, concurrent writes, lazy expiration, typed query filters, PATCH null-clearing, stale embedding prevention, multi-tenancy, semantic search, vector validation boundary, payload size/depth bounds, Unicode canonical equivalence, mixed dimension search safety, and performance regression guards.

## iOS Client Foundation
- `apps/ios/NEXUS/Domain/Memories/MemoryModels.swift`: Swift data models, enums (`MemoryType`, `MemoryStatus`, `MemorySensitivity` including `RESTRICTED`), and presentation helpers.
- `apps/ios/NEXUS/Data/Network/NexusAPIClient.swift`: Added typed network requests for memory management.
- `apps/ios/NEXUS/Domain/Memories/MemoryManager.swift`: Observable `@MainActor` state manager for memory operations.
- `apps/ios/NEXUS/Features/Memories/MemoriesListView.swift`: SwiftUI view for browsing, filtering, and searching memories.
- `apps/ios/NEXUS/Features/Memories/CreateMemorySheet.swift`: SwiftUI modal sheet for creating memories.
- `apps/ios/NEXUS/Features/Memories/MemoryDetailView.swift`: SwiftUI detail view for inspecting, editing, and soft-forgetting memories.
- `apps/ios/NEXUS/App/ContentView.swift`: Integrated Memories tab into main TabView navigation.

## Architecture & Governance Documentation
- `docs/api/api-contract.md`: Updated Section 6 with accurate schemas, query params, null-clear PATCH semantics, response envelopes, payload bounds, and error codes.
- `docs/architecture/TBD-REGISTRY.md`: Refined `TBD-004` to cover production provider, model, and dimension; removed redundant `TBD-030`.
- `docs/stages/phase-1/M3-memory-core/`: 12 canonical stage documentation files plus 2 supplemental review/remediation evidence files (`review-record.md`, `post-review-remediation.md`).
- `docs/context/`: `PROJECT-STATE.md`, `CURRENT-STAGE.md`, `NEXT-ACTIONS.md`, `HANDOFF.md` synchronized.

# Milestone M3: Files Changed

## 1. Backend Domain & API
- `backend/app/domains/memories/models.py`: Added `Memory` model, enums (`MemoryType`, `MemoryStatus`, `MemorySensitivity`, `MemorySourceType`), constraints, and indexes.
- `backend/app/domains/users/models.py`: Added `memories` relationship to `User`.
- `backend/app/domains/projects/models.py`: Added `memories` relationship to `Project`.
- `backend/app/domains/memories/exceptions.py`: Added domain exception hierarchy (`MemoryError`, `MemoryNotFoundError`, `MemorySecretRejectedError`, `MemoryInvalidStateError`, `MemoryScopeError`, `EmbeddingUnavailableError`).
- `backend/app/domains/memories/safety.py`: Implemented `MemorySafetyPolicy` for NEVER_STORE credential rejection.
- `backend/app/domains/memories/embedding.py`: Implemented `EmbeddingProvider` protocol, `UnavailableEmbeddingProvider`, and `DeterministicTestEmbeddingProvider`.
- `backend/app/domains/memories/schemas.py`: Pydantic request/response schemas with project scope validation.
- `backend/app/domains/memories/service.py`: Implemented `MemoryService` business logic with user locking, dedup, superseding, expiration, and semantic search.
- `backend/app/domains/memories/__init__.py`: Exported domain symbols.
- `backend/alembic/versions/0004_memories_core.py`: Alembic migration for `memories` table.
- `backend/app/api/v1/memories.py`: Router for 6 memory endpoints.
- `backend/app/api/v1/router.py`: Registered `memories_router`.
- `backend/app/main.py`: Registered `MemoryError` handler and `jsonable_encoder` in validation handler.
- `backend/tests/test_memories.py`: 14 automated test cases.

## 2. iOS Client Layer
- `apps/ios/NEXUS/Domain/Memories/MemoryModels.swift`: Swift domain models.
- `apps/ios/NEXUS/Data/Network/NexusAPIClient.swift`: Added 6 memory API methods.
- `apps/ios/NEXUS/Domain/Memories/MemoryManager.swift`: Observable memory state store.
- `apps/ios/NEXUS/Features/Memories/MemoriesListView.swift`: SwiftUI memories list with scope filters and search.
- `apps/ios/NEXUS/Features/Memories/CreateMemorySheet.swift`: SwiftUI memory creation form with taxonomy picker.
- `apps/ios/NEXUS/Features/Memories/MemoryDetailView.swift`: SwiftUI memory detail, editing, and forget action.
- `apps/ios/NEXUS/App/ContentView.swift`: Added Memories tab to TabView.

## 3. Architecture & Documentation
- `docs/architecture/TBD-REGISTRY.md`: Recorded `TBD-030`.
- `docs/stages/phase-1/M3-memory-core/`: 12 stage documentation files.

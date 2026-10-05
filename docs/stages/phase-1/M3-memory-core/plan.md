# Milestone M3 Plan: Memory Core Domain & Control Center Foundation

## 1. Objectives & Approach
1. **Core Product Principle Alignment:**
   - Preserve foundational axiom: *"Store meaning, not everything."*
   - Strictly avoid anti-patterns: Memory is NOT raw conversation logs, uncurated note dumps, document corpus storage, or telemetry streams.
   - Enforce the 10 canonical memory types:
     - Global / Personal (6): `PERSONAL_FACT`, `PREFERENCE`, `INTEREST`, `SKILL`, `GOAL`, `BEHAVIOR_PATTERN`.
     - Project-Scoped (4): `PROJECT_FACT`, `PROJECT_DECISION`, `PROJECT_PROGRESS`, `PROJECT_NEXT_ACTION`.
     - Strictly reject generic types (`FACT`, `NOTE`, `DECISION`, `CONTEXT`, `OTHER`).
2. **Model & Migration Design:**
   - Define `Memory` model in `backend/app/domains/memories/models.py`.
   - Setup composite indexes (`user_id, status`, `user_id, project_id, status`, `user_id, memory_type, status`, `expires_at`, `user_id, updated_at`).
   - Setup check constraints for `importance` (0.0 to 1.0) and `confidence` (0.0 to 1.0).
   - Incorporate `Vector(1536)` embedding column via pgvector.
   - Author and validate Alembic migration `0004_memories_core.py` with clean upgrade/downgrade/upgrade cycle.
3. **Safety & Security (NEVER_STORE Policy):**
   - Implement `MemorySafetyPolicy` with deterministic pattern scanning for secret tokens, credentials, private keys, JWTs, and API keys.
   - Enforce rejection with HTTP 400 (`MEMORY_SECRET_REJECTED`) without echoing secret content or logging credentials.
4. **Service & Domain Invariants:**
   - Implement user row locking (`with_for_update()`) to serialize writes per user.
   - Enforce exact deduplication for identical logical memories.
   - Implement superseding logic: same identity key with changed value sets `status = SUPERSEDED`, `superseded_by = new.id`.
   - Implement query-time expiration exclusion.
   - Implement idempotent `forget_memory` transitioning status to `FORGOTTEN`.
   - Implement pgvector cosine similarity search (`search_memories`).
   - Decouple embedding generation behind `EmbeddingProvider` protocol with default `UnavailableEmbeddingProvider` (HTTP 503 per `TBD-004`) and test-only `DeterministicTestEmbeddingProvider`.
5. **Transport & Routing:**
   - Create `backend/app/api/v1/memories.py` covering all 6 canonical endpoints.
   - Register router in `backend/app/api/v1/router.py`.
   - Register `MemoryError` handler in `backend/app/main.py`.
6. **Backend Test Suite:**
   - Author comprehensive suite in `backend/tests/test_memories.py` testing auth, creation, taxonomy, scope rules, secrets rejection, dedup, supersede, concurrency, expiration, forget, update, IDOR isolation, and semantic search.
7. **iOS Client Layer:**
   - Implement domain models in `apps/ios/NEXUS/Domain/Memories/MemoryModels.swift`.
   - Extend `NexusAPIClient` with memory networking methods.
   - Implement `@MainActor MemoryManager: ObservableObject`.
   - Implement SwiftUI views: `MemoriesListView`, `CreateMemorySheet`, `MemoryDetailView`.
   - Add Memories tab to TabView in `ContentView.swift`.
8. **Validation & Quality Gates:**
   - Run Ruff, Mypy, Pytest, Xcodebuild, and Swift build.
   - Author all 12 stage documentation files.
   - Record `TBD-004` in `TBD-REGISTRY.md`.
   - Update canonical handoff files, commit, push, and open PR.

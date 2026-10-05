# PROJECT STATE — NEXUS

**Product:** NEXUS (Personal AI Companion & Intelligence Ecosystem)  
**Canonical Remote:** `https://github.com/Nachsyas/NEXUS.git`  
**Repository Visibility:** PUBLIC (Intentionally public repository)  
**Primary Branch:** `main`  
**Milestone Branch:** `milestone/m3-memory-core`  
**Local Repository (Current Machine):** `/Users/user/Documents/Nexus`  
**Current Phase:** Phase 1 (Core Personal Intelligence System)  
**Current Milestone:** Milestone M3 (Memory Core) — IMPLEMENTED & VALIDATED  
**Current Stage:** Milestone M3 implementation complete, tested, documented, and prepared for PR  
**Production NEXUS Implementation:** M1 Account & Identity + M2 Projects + M3 Memory Core  
**iOS Project:** Canonical location `apps/ios/NEXUS.xcodeproj` (Target `NEXUS`, Swift 6 Approachable Concurrency, Sign in with Apple UI, Projects & Memories Control Center, build succeeded)  
**macOS Agent:** Canonical location `apps/mac-agent/` (Native Swift Package executable foundation; Phase 1 packaging tracked in TBD-027)  
**Backend:** Canonical location `backend/` (FastAPI modular monolith, `uv` baseline, PostgreSQL 16 + pgvector, Redis 7, Alembic migrations 0001-0004 applied, 54/54 Pytest passing)  
**Apple Auth Status:** Code complete; mock verifier 100% passing; iOS UI builds; `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`  
**M0 Status:** CLOSED — COMPLETE  
**M1 Status:** CLOSED — COMPLETE & RATIFIED  
**M2 Status:** CLOSED — COMPLETE  
**M3 Status:** IMPLEMENTATION COMPLETE — PRE-MERGE CORRECTIVE PASS COMPLETED — READY FOR FINAL PR MERGE  
**Next Milestone:** Milestone M4 — AI Conversation (Canonical Phase 1 order: M0 Foundation -> M1 Account & Identity -> M2 Projects -> M3 Memory Core -> M4 AI Conversation; strictly awaiting PR review and explicit authorization)  
**Standing Autonomous Execution:** HALTED AT M3 PR BOUNDARY  

---

## 1. Stack Resmi & Status Keputusan

### Accepted Architectural Baseline (ADR-001 s/d ADR-020)
- **iOS Client:** Swift Native, SwiftUI, SwiftData (cache only), Keychain (`apps/ios/NEXUS.xcodeproj`) — Node produk terpisah dari Mac Agent (ADR-006).
- **Mac Agent:** Swift Native, Outbound WSS protocol skeleton, Capability-based execution node (`apps/mac-agent/`) — Larangan mutlak shell arbitrer (ADR-007, ADR-008, ADR-009, ADR-010).
- **Backend:** Python, FastAPI (Modular Monolith, ADR-001, ADR-002), Async Database Engine, Redis Manager (`backend/`).
- **Database:** PostgreSQL 16 dengan pgvector extension (`infrastructure/docker/`, ADR-003, ADR-004, ADR-019 / TBD-026 RESOLVED).
- **Ephemeral / State:** Redis 7 (`infrastructure/docker/`, ADR-005).
- **Package & Env Manager:** `uv` baseline Phase 1 (`backend/`, ADR-016 / TBD-013 RESOLVED).
- **Primary ID Strategy:** RFC 9562 `UUIDv7` untuk seluruh entitas persisten (`backend/app/core/`, ADR-017 / TBD-014 RESOLVED).
- **Memory Vector Search:** `Vector(1536)` via pgvector with `<=>` cosine distance, decoupled behind `EmbeddingProvider` (TBD-030).

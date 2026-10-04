# PROJECT STATE — NEXUS

**Product:** NEXUS (Personal AI Companion & Intelligence Ecosystem)  
**Current Phase:** Phase 1 (Foundation & Core Skeleton)  
**Current Milestone:** Milestone M0 (Foundation) — CLOSED / COMPLETE  
**Current Stage:** Milestone M0 Formally Ratified & Closed; Ready for M1  
**Production NEXUS Implementation:** M0 Bedrock Established & Verified  
**iOS Project:** Canonical location `apps/ios/NEXUS.xcodeproj` (Target `NEXUS`, supported destinations: iOS/iPadOS `iphoneos`, `iphonesimulator`)  
**macOS Agent:** Canonical location `apps/mac-agent/` (Native Swift Package executable foundation; Phase 1 packaging tracked in TBD-027)  
**Backend:** Canonical location `backend/` (FastAPI modular monolith, `uv` baseline, PostgreSQL 16 + pgvector, Redis 7, Alembic baseline, 8/8 Pytest passing)  
**M0 Status:** CLOSED — COMPLETE (Implementation Verified, Governance Ratified)  
**Next Milestone:** Milestone M1 — Account & Identity Foundation (UNBLOCKED)  

---

## 1. Stack Resmi & Status Keputusan

### Accepted Architectural Baseline (ADR-001 s/d ADR-019)
- **iOS Client:** Swift Native, SwiftUI, SwiftData (cache only), Keychain (`apps/ios/NEXUS.xcodeproj`) — Node produk terpisah dari Mac Agent (ADR-006).
- **Mac Agent:** Swift Native, Outbound WSS protocol skeleton, Capability-based execution node (`apps/mac-agent/`) — Larangan mutlak shell arbitrer (ADR-007, ADR-008, ADR-009, ADR-010). Packaging M0 berstatus Foundation Executable; packaging final Phase 1 dievaluasi di TBD-027.
- **Backend:** Python, FastAPI (Modular Monolith, ADR-001, ADR-002), Async Database Engine, Redis Manager (`backend/`).
- **Database:** PostgreSQL 16 dengan pgvector extension (`infrastructure/docker/`, ADR-003, ADR-004, ADR-019 / TBD-026 RESOLVED).
- **Ephemeral / State:** Redis 7 (`infrastructure/docker/`, ADR-005).
- **Package & Env Manager:** `uv` baseline Phase 1 (`backend/`, ADR-016 / TBD-013 RESOLVED).
- **Primary ID Strategy:** RFC 9562 `UUIDv7` untuk seluruh entitas persisten (`backend/app/core/`, ADR-017 / TBD-014 RESOLVED).
- **Quality Tooling:** `Ruff` (linter/formatter) + `Mypy` (strict mode) (ADR-018 / TBD-015 RESOLVED).

### Implementation Baselines vs Locked Architecture
- Redis 7, SQLAlchemy async engine, driver `asyncpg`/`psycopg`, dan port lokal `5433` / `6380` berstatus sebagai **implementation baselines**, bukan batasan arsitektural yang kaku.

---

## 2. Status Keputusan & Registry
- **Accepted ADRs:** Seluruh ADR-001 hingga ADR-019 ACCEPTED (Ratifikasi formal pengguna selesai).
- **TBD Registry:** TBD-013, TBD-014, TBD-015, TBD-026 RESOLVED. TBD-027 OPEN (Evaluasi packaging final Mac Agent).
- **Open Defect Issues:** 0 defect aktif.
- **Latest Relevant Commit:** M0 Decision Batch Formal Ratification & Stage Closure  
- **Last Updated:** 2026-10-04  

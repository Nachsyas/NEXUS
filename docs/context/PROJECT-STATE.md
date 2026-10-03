# PROJECT STATE — NEXUS

**Product:** NEXUS (Personal AI Companion & Intelligence Ecosystem)  
**Current Phase:** Phase 1 (Foundation & Core Skeleton)  
**Current Milestone:** Milestone M0 (Foundation) — COMPLETE (Governance Normalized)  
**Current Stage:** Milestone M0 Completed / Ready for M1  
**Production NEXUS Implementation:** M0 Bedrock Established  
**iOS Project:** Canonical location `apps/ios/NEXUS.xcodeproj` (Target `NEXUS`, supported destinations: iOS/iPadOS `iphoneos`, `iphonesimulator`)  
**macOS Agent:** Canonical location `apps/mac-agent/` (Native Swift Package executable foundation; Phase 1 packaging tracked in TBD-027)  
**Backend:** Canonical location `backend/` (FastAPI modular monolith, `uv` baseline, PostgreSQL 16 + pgvector, Redis 7, Alembic baseline, 8/8 Pytest passing)  
**M0 Status:** COMPLETED, NORMALIZED, AND VERIFIED  

---

## 1. Stack Resmi & Status Keputusan

### Accepted Architectural Baseline (ADR-001 s/d ADR-015)
- **iOS Client:** Swift Native, SwiftUI, SwiftData (cache only), Keychain (`apps/ios/NEXUS.xcodeproj`) — Node produk terpisah dari Mac Agent.
- **Mac Agent:** Swift Native, Outbound WSS protocol skeleton, Capability-based execution node (`apps/mac-agent/`) — Larangan mutlak shell arbitrer (ADR-010).
- **Backend:** Python, FastAPI (Modular Monolith, ADR-001/ADR-002), Async Database Engine, Redis Manager (`backend/`).
- **Database:** PostgreSQL dengan pgvector extension (`infrastructure/docker/`).

### Proposed by M0 Implementation (Menunggu Ratifikasi Formal Pengguna)
- **TBD-013 (ADR-016):** `uv` Python package & environment manager.
- **TBD-014 (ADR-017):** `UUIDv7` (RFC 9562) primary identifier strategy.
- **TBD-015 (ADR-018):** `Ruff` (linter/formatter) + `Mypy` (strict mode).
- **TBD-026 (ADR-019):** `PostgreSQL 16` major version baseline dengan pgvector.

### Implementation Baselines vs Locked Architecture
- Redis 7, SQLAlchemy async engine, driver `asyncpg`/`psycopg`, dan port lokal `5433` / `6380` berstatus sebagai **implementation baselines**, bukan batasan arsitektural yang kaku.

---

## 2. Status Keputusan & Registry
- **Accepted ADRs:** ADR-001 hingga ADR-015 ACCEPTED.
- **Proposed ADRs:** ADR-016 hingga ADR-019 PROPOSED BY M0 IMPLEMENTATION.
- **TBD Registry:** TBD-001 s/d TBD-027 tercatat aktif di `docs/architecture/TBD-REGISTRY.md`.
- **Open Issues:** 0 defect aktif; TBD-027 terbuka untuk evaluasi packaging final Mac Agent.
- **Latest Relevant Commit:** Milestone M0 Foundation Final Normalization  
- **Last Updated:** 2026-10-03  

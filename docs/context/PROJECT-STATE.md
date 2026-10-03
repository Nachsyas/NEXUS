# PROJECT STATE — NEXUS

**Product:** NEXUS (Personal AI Companion & Intelligence Ecosystem)  
**Current Phase:** Phase 1 (Foundation & Core Skeleton)  
**Current Milestone:** Milestone M0 (Foundation) — COMPLETE  
**Current Stage:** Milestone M0 Completed / Ready for M1  
**Production NEXUS Implementation:** M0 Bedrock Established  
**iOS Project:** Canonical location `apps/ios/NEXUS.xcodeproj` (Target `NEXUS`, builds and launches cleanly)  
**macOS Agent:** Canonical location `apps/mac-agent/` (Native Swift executable, builds and launches cleanly)  
**Backend:** Canonical location `backend/` (FastAPI modular monolith, `uv`, PostgreSQL 16 + pgvector, Redis 7, Alembic baseline, 8/8 Pytest passing)  
**M0 Status:** COMPLETED AND VERIFIED  

---

## 1. Stack Resmi Disetujui (Approved Stack Baseline)
- **iOS Client:** Swift, SwiftUI, SwiftData (cache only), Keychain (`apps/ios/NEXUS.xcodeproj`)
- **Mac Agent:** Swift Native (Menu bar utility skeleton), Outbound WSS protocol skeleton, Capability-based execution node (`apps/mac-agent/`)
- **Backend:** Python, FastAPI (Modular Monolith), SQLAlchemy, Alembic, `uv` package manager (`backend/`)
- **Database:** PostgreSQL 16 with pgvector extension (`infrastructure/docker/`)
- **Ephemeral / Presence:** Redis 7 (`infrastructure/docker/`)
- **Linting & Typing:** Ruff + Mypy strict mode
- **Primary ID Strategy:** RFC 9562 UUIDv7

---

## 2. Status Keputusan & Registry
- **Accepted ADRs:** ADR-001 hingga ADR-019 ACCEPTED.
- **TBD Registry:** TBD-013, TBD-014, TBD-015, TBD-026 RESOLVED. Remaining TBDs remain tracked in `docs/architecture/TBD-REGISTRY.md`.
- **Open Issues:** 0 open issues (ISSUE-001, ISSUE-002, ISSUE-003 resolved).
- **Latest Relevant Commit:** Milestone M0 Foundation Completed  
- **Last Updated:** 2026-10-03  

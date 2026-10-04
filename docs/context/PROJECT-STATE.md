# PROJECT STATE — NEXUS

**Product:** NEXUS (Personal AI Companion & Intelligence Ecosystem)  
**Canonical Remote:** `https://github.com/Nachsyas/NEXUS.git`  
**Repository Visibility:** PUBLIC (Intentionally public repository)  
**Primary Branch:** `main`  
**Local Repository (Current Machine):** `/Users/user/Documents/Nexus`  
**Current Phase:** Phase 1 (Core Personal Intelligence System)  
**Current Milestone:** Milestone M1 (Account & Identity Foundation) — CLOSED / COMPLETE  
**Current Stage:** Milestone M1 Completed, Verified, Ratified, and Documented; Ready for M2  
**Production NEXUS Implementation:** M1 Account & Identity Subsystem Established & Verified  
**iOS Project:** Canonical location `apps/ios/NEXUS.xcodeproj` (Target `NEXUS`, Swift 6 Approachable Concurrency, Sign in with Apple UI, Keychain security, build succeeded)  
**macOS Agent:** Canonical location `apps/mac-agent/` (Native Swift Package executable foundation; Phase 1 packaging tracked in TBD-027)  
**Backend:** Canonical location `backend/` (FastAPI modular monolith, `uv` baseline, PostgreSQL 16 + pgvector, Redis 7, Alembic migration 0002 applied, 23/23 Pytest passing)  
**Apple Auth Status:** Code complete; mock verifier 100% passing; iOS UI builds; `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`  
**M1 Status:** CLOSED — COMPLETE (Implementation Verified, Tested, Ratified, Documented)  
**Next Milestone:** Milestone M2 — Projects (Canonical Phase 1 order: M0 Foundation -> M1 Account & Identity -> M2 Projects -> M3 Memory Core; awaiting explicit user authorization)  

---

## 1. Stack Resmi & Status Keputusan

### Accepted Architectural Baseline (ADR-001 s/d ADR-020)
- **iOS Client:** Swift Native, SwiftUI, SwiftData (cache only), Keychain (`apps/ios/NEXUS.xcodeproj`) — Node produk terpisah dari Mac Agent (ADR-006).
- **Mac Agent:** Swift Native, Outbound WSS protocol skeleton, Capability-based execution node (`apps/mac-agent/`) — Larangan mutlak shell arbitrer (ADR-007, ADR-008, ADR-009, ADR-010). Packaging M0 berstatus Foundation Executable; packaging final Phase 1 dievaluasi di TBD-027.
- **Backend:** Python, FastAPI (Modular Monolith, ADR-001, ADR-002), Async Database Engine, Redis Manager (`backend/`).
- **Database:** PostgreSQL 16 dengan pgvector extension (`infrastructure/docker/`, ADR-003, ADR-004, ADR-019 / TBD-026 RESOLVED).
- **Ephemeral / State:** Redis 7 (`infrastructure/docker/`, ADR-005).
- **Package & Env Manager:** `uv` baseline Phase 1 (`backend/`, ADR-016 / TBD-013 RESOLVED).
- **Primary ID Strategy:** RFC 9562 `UUIDv7` untuk seluruh entitas persisten (`backend/app/core/`, ADR-017 / TBD-014 RESOLVED).
- **Quality Tooling:** `Ruff` (linter/formatter) + `Mypy` (strict mode) (ADR-018 / TBD-015 RESOLVED).
- **Session & Token Architecture:** HS256 JWT access tokens (15m configurable TTL, owned by `Settings`), 256-bit opaque refresh tokens (30d configurable TTL) with SHA-256 hash storage and token family reuse revocation (ADR-020 ACCEPTED / TBD-028 & TBD-029 RESOLVED).

### Milestone M1 Deliverables
- **Alembic Migration 0002:** `users`, `auth_identities`, `user_preferences`, `sessions`, `rotated_token_hashes`. Validated forward and backward.
- **Security & Quality:** Production secret entropy validator, algorithm confusion prevention (`algorithms=["HS256"]`), 6-dimension cross-user multi-tenancy isolation verified.
- **Stage Documentation:** Canonical path `docs/stages/phase-1/M1-account-identity/` (12/12 artifacts complete).

---

## 2. Status Keputusan & Registry
- **Accepted ADRs:** ADR-001 hingga ADR-020 ACCEPTED (Semua 20 ADR berstatus ACCEPTED).
- **Proposed ADRs:** Tidak ada.
- **TBD Registry:** TBD-013, TBD-014, TBD-015, TBD-026, TBD-028, TBD-029 RESOLVED. TBD-027 OPEN.
- **Open Defect Issues:** 0 defect aktif.
- **Latest Relevant Commit:** M1 Account & Identity Foundation Ratified & Closed  
- **Last Updated:** 2026-10-04  

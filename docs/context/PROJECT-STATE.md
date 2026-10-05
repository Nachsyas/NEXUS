# PROJECT STATE — NEXUS

**Product:** NEXUS (Personal AI Companion & Intelligence Ecosystem)  
**Canonical Remote:** `https://github.com/Nachsyas/NEXUS.git`  
**Repository Visibility:** PUBLIC (Intentionally public repository)  
**Primary Branch:** `main`  
**Local Repository (Current Machine):** `/Users/user/Documents/Nexus`  
**Current Phase:** Phase 1 (Core Personal Intelligence System)  
**Current Milestone:** Milestone M2 (Projects Domain Foundation) — IMPLEMENTATION COMPLETE  
**Current Stage:** Milestone M2 Implementation Complete on milestone/m2-projects, Pending PR Merge  
**Production NEXUS Implementation:** M1 Account & Identity Subsystem + M2 Projects Domain Established & Verified  
**iOS Project:** Canonical location `apps/ios/NEXUS.xcodeproj` (Target `NEXUS`, Swift 6 Approachable Concurrency, Sign in with Apple UI, Keychain security, build succeeded)  
**macOS Agent:** Canonical location `apps/mac-agent/` (Native Swift Package executable foundation; Phase 1 packaging tracked in TBD-027)  
**Backend:** Canonical location `backend/` (FastAPI modular monolith, `uv` baseline, PostgreSQL 16 + pgvector, Redis 7, Alembic migration 0003 applied, 37/37 Pytest passing)  
**Apple Auth Status:** Code complete; mock verifier 100% passing; iOS UI builds; `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`  
**M1 Status:** CLOSED — COMPLETE (Implementation Verified, Tested, Ratified, Documented)  
**M2 Implementation Status:** COMPLETE ON milestone/m2-projects  
**M2 Integration to Main:** PENDING PR MERGE  
**Next Milestone:** Milestone M3 — Memory Core (Canonical Phase 1 order: M0 Foundation -> M1 Account & Identity -> M2 Projects -> M3 Memory Core; awaiting PR merge and explicit user authorization)  

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

### Milestone M2 Deliverables
- **Alembic Migration 0003:** `projects`, `project_technologies`, `user_preferences.default_project_id` foreign key. Validated forward and backward.
- **Security & Invariants:** Partial unique index `uq_projects_user_active` enforcing single active project focus, (user_id, slug) uniqueness, cross-user IDOR rejection (404), atomic activation transactions.
- **API Surface:** 7 endpoints under `/api/v1/projects` (CRUD, activate, archive, deterministic context foundation).
- **iOS Client:** `ProjectModels.swift`, `ProjectManager.swift`, `ProjectsListView.swift`, `CreateProjectSheet.swift`, `ProjectDetailView.swift` with TabView integration in `ContentView.swift`.
- **Quality Gates:** 37/37 Pytest passing, Ruff check/format clean, Mypy strict clean, iOS Simulator build succeeded, Mac Agent build succeeded.
- **Stage Documentation:** Canonical path `docs/stages/phase-1/M2-projects/` (12/12 artifacts complete).

---

## 2. Status Keputusan & Registry
- **Accepted ADRs:** ADR-001 hingga ADR-020 ACCEPTED (Semua 20 ADR berstatus ACCEPTED).
- **Proposed ADRs:** Tidak ada.
- **TBD Registry:** TBD-013, TBD-014, TBD-015, TBD-026, TBD-028, TBD-029 RESOLVED. TBD-027 OPEN.
- **Open Defect Issues:** 0 defect aktif.
- **Latest Relevant Commit:** M1 Account & Identity Foundation Ratified & Closed  
- **Last Updated:** 2026-10-04  

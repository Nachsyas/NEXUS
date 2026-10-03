# PROJECT STATE — NEXUS

**Product:** NEXUS (Personal AI Companion & Intelligence Ecosystem)  
**Current Phase:** Phase 0 (Governance Bootstrap)  
**Current Milestone:** Pre-M0 (Governance Corrective Review)  
**Current Stage:** Governance Corrective Review / Pre-M0  
**Production NEXUS Implementation:** NOT STARTED  
**Pre-existing Xcode Scaffold:** PRESENT (Default starter scaffold `Untitled Project.xcodeproj` & `MyApp/` remains at repository root; migration to `apps/ios/` scheduled for M0 Foundation)  
**M0 Status:** BLOCKED UNTIL GOVERNANCE CORRECTIVE PASS IS VERIFIED BY USER  

---

## 1. Stack Resmi Disetujui (Approved Stack Baseline)
- **iOS Client:** Swift, SwiftUI, SwiftData (cache only), Keychain (App structure: apps/ios/)
- **Mac Agent:** Swift Native (Menu bar utility), Outbound WSS, Capability-based execution node (App structure: apps/mac-agent/)
- **Backend:** Python, FastAPI (Modular Monolith), SQLAlchemy, Alembic (Structure: backend/)
- **Database:** PostgreSQL (Major version baseline: TBD-026) dengan pgvector (Index & latency target: TBD-025)
- **Ephemeral / Presence:** Redis (Pub/sub, rate limit, presence heartbeat)
- **Realtime:** WebSocket (WSS) dengan bounded reconnect dan heartbeat terkonfigurasi (TBD-022)

---

## 2. Status Keputusan & Registry
- **Accepted ADRs:** ADR-001 hingga ADR-015 ACCEPTED (asumsi unapproved seperti 16+, Pydantic V2, Ed25519 locked, dan HNSW/<80ms telah dibersihkan).
- **TBD Registry:** TBD-001 hingga TBD-026 tercatat aktif di `docs/architecture/TBD-REGISTRY.md`.
- **Open Issues:** Temuan audit korektif tata kelola telah diperbaiki dan diverifikasi; menunggu persetujuan eksplisit pengguna untuk membuka Milestone M0.
- **Latest Relevant Commit:** Governance Corrective Pass (Pre-M0)  
- **Last Updated:** 2026-10-03

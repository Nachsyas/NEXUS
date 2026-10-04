# Architecture Decision Records (ADR) — NEXUS

Dokumentasi ini menyimpan seluruh rekaman keputusan arsitektural penting (*Architecture Decision Records*) untuk ekosistem NEXUS.

## 1. Hirarki Otoritas Keputusan
```text
NEXUS PRODUCT VISION
        ↓
APPROVED PRODUCT SPECIFICATION
        ↓
APPROVED ARCHITECTURE
        ↓
ACCEPTED ADR
        ↓
ENGINEERING CONSTITUTION
        ↓
PHASE / MILESTONE SPECIFICATION
        ↓
AGENTS.md / SOP / SKILLS
        ↓
IMPLEMENTATION
```

## 2. Aturan Tata Kelola ADR
1. **Status Lifecycle:** Setiap ADR baru wajib diawali dengan status `PROPOSED`.
2. **Larangan Self-Approval:** AI Agent dilarang keras mengubah status ADR menjadi `ACCEPTED` secara sepihak. Perubahan status hanya sah setelah ada persetujuan eksplisit dari pengguna.
3. **Template:** Gunakan [`ADR-template.md`](ADR-template.md) saat menyusun proposal ADR baru.
4. **Pendaftaran:** Setiap ADR baru wajib didaftarkan di `docs/context/ACTIVE-DECISIONS.md`.

## 3. Daftar ADR Phase 1 yang Diterima (Accepted Baseline)
- [ADR-001: Modular Monolith Architecture for Phase 1 Backend](ADR-001-modular-monolith-phase-1.md)
- [ADR-002: FastAPI Framework for Backend Core](ADR-002-fastapi-backend.md)
- [ADR-003: PostgreSQL as Primary Relational Database](ADR-003-postgresql-primary-database.md)
- [ADR-004: pgvector as Phase 1 Vector Store Baseline](ADR-004-pgvector-phase-1-vector-store.md)
- [ADR-005: Redis for Ephemeral State, Presence, and Pub/Sub](ADR-005-redis-ephemeral-state.md)
- [ADR-006: Native Swift & SwiftUI for iOS Client](ADR-006-swift-native-ios.md)
- [ADR-007: Swift Native Menu Bar Utility for macOS Agent](ADR-007-swift-native-macos-agent.md)
- [ADR-008: Persistent Outbound WebSocket (WSS) for Mac Agent](ADR-008-outbound-wss-for-mac-agent.md)
- [ADR-009: Capability-Based Execution Model for Mac Actions](ADR-009-capability-based-mac-execution.md)
- [ADR-010: Prohibition of Arbitrary Terminal / Shell Execution](ADR-010-no-arbitrary-remote-shell.md)
- [ADR-011: Model-Agnostic AI Provider Architecture](ADR-011-model-agnostic-ai-provider-architecture.md)
- [ADR-012: Absolute Data Semantic Separation](ADR-012-data-semantic-separation.md)
- [ADR-013: Documentation-First & Stage Governance](ADR-013-documentation-first-stage-governance.md)
- [ADR-014: Measurement-First Performance Engineering](ADR-014-measurement-first-performance-engineering.md)
- [ADR-015: Deterministic Permission and Risk Model Outside LLM](ADR-015-deterministic-permission-and-risk-outside-llm.md)
- [ADR-016: uv as Python Package and Environment Manager](ADR-016-uv-python-package-manager.md)
- [ADR-017: UUIDv7 Primary Identifier Strategy](ADR-017-uuidv7-primary-id-strategy.md)
- [ADR-018: Ruff and Mypy for Python Formatting, Linting, and Type-Checking](ADR-018-ruff-mypy-python-tooling.md)
- [ADR-019: PostgreSQL 16 Major Version Baseline with pgvector](ADR-019-postgresql-16-major-version-baseline.md)
- [ADR-020: Session Token Format, Signing Architecture, and Rotation Strategy](ADR-020-session-token-format-and-signing.md)

## 4. Daftar ADR Diusulkan (Proposed)
*(Tidak ada ADR yang berstatus PROPOSED saat ini. Seluruh ADR-001 hingga ADR-020 telah berstatus ACCEPTED).*

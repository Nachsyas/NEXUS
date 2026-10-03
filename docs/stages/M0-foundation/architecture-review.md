# Architecture Review: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03  
**Status:** COMPLIANT WITH ENGINEERING CONSTITUTION & ADRS  

## 1. Compliance with Accepted ADRs

| ADR | Title | Compliance Evidence |
|---|---|---|
| **ADR-001** | Modular Monolith Phase 1 Backend | Single FastAPI backend repository structure with decoupled module folders under `backend/app/`. |
| **ADR-002** | FastAPI Framework Backend Core | FastAPI 0.115+ application factory with lifespan hooks and async routers. |
| **ADR-003** | PostgreSQL Primary Relational Database | PostgreSQL 16 engine configured with async SQLAlchemy 2.0 and asyncpg. |
| **ADR-004** | pgvector Vector Store Baseline | Official `pgvector/pgvector:pg16` image; baseline migration enables `vector` extension. |
| **ADR-005** | Redis Ephemeral State & Presence | Redis 7 container and async Redis client manager initialized. |
| **ADR-006** | Swift Native iOS Client | SwiftUI app structure in `apps/ios/NEXUS/` with target `NEXUS`. |
| **ADR-007** | Swift Native macOS Agent | Native Swift executable in `apps/mac-agent/`. |
| **ADR-008** | Persistent Outbound WSS for Mac Agent | Module boundary protocol `RealtimeProtocol` prepared in Mac Agent. |
| **ADR-009** | Capability-Based Execution Model | Protocol boundary `CapabilityProtocol` established without arbitrary execution. |
| **ADR-010** | Strict Prohibition of Arbitrary Shell | `SecurityBoundary.isArbitraryShellPermitted = false`; zero shell APIs exposed. |
| **ADR-012** | Semantic Separation of Data Concepts | No premature entity mixing; clear boundary established for Phase 1 expansion. |
| **ADR-013** | Documentation-First Stage Governance | All 12 stage documentation files generated with empirical data. |
| **ADR-014** | Measurement-First Performance Engineering | Baseline benchmarks recorded in `performance-results.md`. |
| **ADR-016** | uv Python Package Manager | `backend/pyproject.toml` and `backend/uv.lock` managed exclusively with `uv`. |
| **ADR-017** | UUIDv7 Primary Identifier Strategy | UUIDv7 standard implemented via `uuid6.uuid7()` for request IDs and future entities. |
| **ADR-018** | Ruff + Mypy Tooling Baseline | Fully automated Ruff linting, formatting, and strict Mypy checks configured in CI. |
| **ADR-019** | PostgreSQL 16 Major Version Baseline | Standardized container version `pgvector/pgvector:pg16`. |

## 2. Dependency Direction Evaluation
- **Transport (`api/v1/`):** Depends only on schemas and core utilities; does not contain domain business logic.
- **Infrastructure (`core/`):** Manages DB, Redis, and configuration adapters without circular references.
- **Strict Separation:** Verified zero circular imports across backend modules.

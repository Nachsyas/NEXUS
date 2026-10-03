# Architecture Review: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03  
**Status:** COMPLIANT WITH ENGINEERING CONSTITUTION & ADRS  

## 1. Compliance with Accepted ADRs & Proposed M0 Decisions

| ADR | Title | Status | Compliance Evidence |
|---|---|---|---|
| **ADR-001** | Modular Monolith Phase 1 Backend | ACCEPTED | Single FastAPI backend repository structure with decoupled module folders under `backend/app/`. |
| **ADR-002** | FastAPI Framework Backend Core | ACCEPTED | FastAPI 0.115+ application factory with lifespan hooks and async routers. |
| **ADR-003** | PostgreSQL Primary Relational Database | ACCEPTED | PostgreSQL engine configured with async SQLAlchemy 2.0 and asyncpg. |
| **ADR-004** | pgvector Vector Store Baseline | ACCEPTED | Official `pgvector/pgvector:pg16` image; baseline migration enables `vector` extension. |
| **ADR-005** | Redis Ephemeral State & Presence | ACCEPTED | Redis 7 container and async Redis client manager initialized. |
| **ADR-006** | Swift Native iOS Client | ACCEPTED | SwiftUI app structure in `apps/ios/NEXUS/` with target `NEXUS`. |
| **ADR-007** | Swift Native macOS Agent | ACCEPTED | Native Swift executable in `apps/mac-agent/`. |
| **ADR-008** | Persistent Outbound WSS for Mac Agent | ACCEPTED | Module boundary protocol `RealtimeProtocol` prepared in Mac Agent. |
| **ADR-009** | Capability-Based Execution Model | ACCEPTED | Protocol boundary `CapabilityProtocol` established without arbitrary execution. |
| **ADR-010** | Strict Prohibition of Arbitrary Shell | ACCEPTED | `SecurityBoundary.isArbitraryShellPermitted = false`; zero shell APIs exposed. |
| **ADR-012** | Semantic Separation of Data Concepts | ACCEPTED | No premature entity mixing; clear boundary established for Phase 1 expansion. |
| **ADR-013** | Documentation-First Stage Governance | ACCEPTED | All 12 stage documentation files generated with empirical data. |
| **ADR-014** | Measurement-First Performance Engineering | ACCEPTED | Baseline benchmarks recorded in `performance-results.md`. |
| **ADR-016** | uv Python Package Manager | PROPOSED BY M0 IMPLEMENTATION | `backend/pyproject.toml` and `backend/uv.lock` managed exclusively with `uv`. |
| **ADR-017** | UUIDv7 Primary Identifier Strategy | PROPOSED BY M0 IMPLEMENTATION | UUIDv7 standard implemented via `uuid6.uuid7()` for request IDs and future entities. |
| **ADR-018** | Ruff + Mypy Tooling Baseline | PROPOSED BY M0 IMPLEMENTATION | Fully automated Ruff linting, formatting, and strict Mypy checks configured in CI. |
| **ADR-019** | PostgreSQL 16 Major Version Baseline | PROPOSED BY M0 IMPLEMENTATION | Standardized container version `pgvector/pgvector:pg16`. |

## 2. Implementation Baselines vs Locked Architecture
- **Locked Architectural Constraints:** Structural choices (Modular Monolith, Prohibition of Remote Shell, PostgreSQL relational foundation, Capability-based execution) are locked by Accepted ADRs.
- **Implementation Baselines:** Specific operational versions and settings (Redis 7, SQLAlchemy async engine, `asyncpg`/`psycopg` drivers, and local dev host ports `5433` and `6380`) are classified as *implementation baselines*, not immutable architectural constraints, allowing fluid evolution without unnecessary governance friction.

## 3. Platform Boundary & Node Separation
- **Strict Node Separation:** NEXUS iOS Client and NEXUS Mac Agent represent independent architectural nodes.
- **iOS Client Scope:** Constrained strictly to `iphoneos` and `iphonesimulator` for iPhone and iPad (`TARGETED_DEVICE_FAMILY = "1,2"`). Unintended starter scaffold destinations (`macosx`, `xros`) have been purged.
- **Catalyst Rule:** A Mac-compatible iOS build must never be treated as or substituted for the NEXUS Mac Agent.

## 4. Mac Agent Packaging Lifecycle
- **M0 Foundation Packaging:** Swift Package executable (`apps/mac-agent/Package.swift`). Sufficient for verifying module compilation and security boundaries.
- **Phase 1 Application Packaging (TBD-027):** Remains open pending evaluation before M6/M7 of macOS App Bundle requirements (Keychain access, TCC entitlements, background lifecycle, menu bar status item).

## 5. Dependency Direction Evaluation
- **Transport (`api/v1/`):** Depends only on schemas and core utilities; does not contain domain business logic.
- **Infrastructure (`core/`):** Manages DB, Redis, and configuration adapters without circular references.
- **Strict Separation:** Verified zero circular imports across backend modules.

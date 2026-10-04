# CURRENT STAGE: Milestone M1 Closed & Complete

**Current Stage:** Milestone M1 (Account & Identity Foundation) — CLOSED / COMPLETE  
**Phase:** Phase 1 (Core Personal Intelligence System)  
**Production NEXUS Implementation:** M1 Subsystem Established & Verified  
**M1 Governance Status:** IMPLEMENTED, TESTED, RATIFIED (ADR-020 ACCEPTED), VERIFIED, DOCUMENTED  
**Live Apple E2E Status:** `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED` (Offline mock verifier 100% automated coverage; production verifier code complete)  
**Next Stage:** Milestone M2 (Projects) — PENDING USER AUTHORIZATION  
**M1 Final Status:** CLOSED — COMPLETE  

---

## 1. Stage Objectives & Accomplishments
Milestone M1 established the canonical account and identity subsystem across backend domains, REST endpoints, database schema, and iOS client integration.

### Completed Deliverables:
- [x] **Canonical Domain Models & Separation:** `User` (UUIDv7 PK) strictly separated from `AuthIdentity` (`provider = 'APPLE'`). `User` != `Authentication Provider`.
- [x] **Database Schema & Migrations:** Created `users`, `auth_identities`, `user_preferences`, `sessions`, `rotated_token_hashes` via Alembic migration `0002_identity_and_sessions.py`. Forward and rollback migrations fully verified.
- [x] **External Provider Verification Boundary:** Abstract `AppleIdentityVerifier` with `ProductionAppleVerifier` (JWKS RS256 validation) and deterministic offline `MockAppleVerifier`.
- [x] **Token & Session Architecture (ADR-020 ACCEPTED):** Short-lived HS256 JWT access tokens (15m configurable TTL), 256-bit opaque refresh tokens (30d configurable TTL). Plaintext refresh tokens are never persisted in the database (only SHA-256 hashes).
- [x] **Security Invariants & Algorithm Safety:** Decoding explicitly restricted to `algorithms=["HS256"]`; `none` or unexpected algorithms strictly rejected. Production security validator forbids placeholder secrets in production.
- [x] **Token Rotation & Replay Defense:** Atomic refresh token rotation with `rotated_token_hashes` archival. Reuse detection instantly revokes the entire token family with immediate database commit. Revoked sessions cannot refresh.
- [x] **User Preferences:** Initialized on first Apple sign-in, manageable via `/api/v1/me/preferences`.
- [x] **Multi-Tenant Isolation & IDOR Protection:** Enforced across all endpoints. Comprehensive tests verify isolation across read/modify profile, read/modify preferences, and list/revoke sessions. Cross-tenant access attempts return 403 `FORBIDDEN_ACCESS`.
- [x] **iOS Client Architecture:**
  - `NexusKeychainService`: Hardware-backed secure storage via iOS Security framework (`kSecClassGenericPassword`, `kSecAttrAccessibleAfterFirstUnlock`).
  - `NexusAPIClient`: URLSession client conforming to canonical envelope.
  - `AuthManager`: Observable auth state machine (`.unauthenticated`, `.authenticating`, `.authenticated`, `.error`).
  - `AuthView`: Minimal, functional SwiftUI interface with `SignInWithAppleButton`, loading state, profile view, and logout action.
- [x] **Target Compilation:** iOS target builds cleanly (`** BUILD SUCCEEDED **`); macOS agent builds cleanly.
- [x] **Automated Tests:** 23/23 backend tests passing cleanly in 1.06s.
- [x] **Quality Tooling:** Ruff check, Ruff format, and Mypy strict mode 100% passing across 30 source files.
- [x] **Stage Documentation:** All 12 files completed in canonical path `docs/stages/phase-1/M1-account-identity/`.

---

## 2. Gate Verification Status
All Milestone M1 requirements and security invariants have been verified, tested, ratified, and documented.

## 3. Boundary & Stop Condition
Milestone M1 is officially **CLOSED**. In accordance with the canonical roadmap (M0 Foundation -> M1 Account & Identity -> M2 Projects -> M3 Memory Core), the next milestone is **Milestone M2 — Projects**. Milestone M2 requires explicit user authorization (`START M2 PROJECTS`) before execution begins. Standing Autonomous Execution halts here.

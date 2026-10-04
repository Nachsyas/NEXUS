# Stage M1: Account & Identity Foundation

## Milestone Overview
- **Milestone Code:** M1
- **Milestone Name:** Account & Identity Foundation
- **Phase:** Phase 1 — Core Personal Intelligence System
- **Status:** CLOSED — COMPLETE
- **Governance:** ADR-020 ACCEPTED (User Ratified 2026-10-04)
- **Lead Agent:** Antigravity (Autonomous Execution)

## Objective
Establish the canonical multi-tenant account and identity subsystem for NEXUS, anchored on Sign in with Apple for external identity verification while maintaining strict separation between external authentication providers and internal NEXUS user identity (`USER != AUTH_PROVIDER`). Implement short-lived HS256 access tokens, cryptographically secure rotating refresh tokens with token family reuse detection, user preferences initialization, iOS Keychain credential storage, and a functional Sign in with Apple authentication UI.

## Scope Delivered
1. **Core Database Schema & Migrations:**
   - PostgreSQL 16 schema with UUIDv7 primary keys via RFC 9562 (`uuid6.uuid7`).
   - Tables: `users`, `auth_identities`, `user_preferences`, `sessions`, `rotated_token_hashes`.
   - Migration `0002_identity_and_sessions.py` validated forward and backward (`downgrade -1` / `upgrade head`).
2. **Provider Boundary & Apple Verification:**
   - `AppleIdentityVerifier` protocol isolating Apple SDK/claims parsing from core services.
   - `ProductionAppleVerifier` verifying Apple JWKS RSA keys, claims, issuer, and audience.
   - `MockAppleVerifier` providing deterministic offline test fixture.
   - **Verification Status:** Production verification code exists; Mock/offline verifier tests pass (100%); iOS Sign in with Apple UI builds cleanly.
   - **Live Apple E2E Status:** `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED` (requires real Apple Developer account provisioning and device runtime).
3. **Session & Security Subsystem (ADR-020 Accepted Baseline):**
   - Short-lived HS256 JWT access tokens (15m configurable TTL, owned canonically in `Settings`).
   - Opaque cryptographically secure 256-bit refresh tokens (30d configurable TTL, owned canonically in `Settings`).
   - Only SHA-256 hashes persisted in database (plaintext refresh tokens never stored).
   - Algorithm confusion defense: strict constraint to `algorithms=["HS256"]`; `none` or unexpected algorithms rejected.
   - Token family rotation and automatic reuse detection / session family revocation with immediate DB commit.
   - Production security validator preventing development placeholder secrets in production.
4. **API Endpoints & Contracts:**
   - `POST /api/v1/auth/apple`: Sign in with Apple and session creation.
   - `POST /api/v1/auth/refresh`: Refresh token rotation with reuse detection.
   - `POST /api/v1/auth/logout`: Current session revocation.
   - `GET /api/v1/auth/sessions`: List active authenticated sessions.
   - `DELETE /api/v1/auth/sessions/{id}`: Manual session termination with cross-tenant authorization guard.
   - `GET /api/v1/me`: Current user profile.
   - `PATCH /api/v1/me`: Profile display name update.
   - `GET /api/v1/me/preferences`: User interaction preferences.
   - `PATCH /api/v1/me/preferences`: Update preferences.
5. **Cross-User Isolation & IDOR Defense:**
   - Comprehensive test evidence demonstrating User A cannot read/modify User B profile, read/modify User B preferences, or list/revoke User B sessions.
6. **iOS Client:**
   - `NexusKeychainService`: Hardware-backed secure storage using `kSecClassGenericPassword` with `kSecAttrAccessibleAfterFirstUnlock`.
   - `NexusAPIClient`: URLSession networking adapter.
   - `AuthManager`: Observable auth state machine (`.unauthenticated`, `.authenticating`, `.authenticated`, `.error`).
   - `AuthView`: SwiftUI Sign in with Apple interface, loading indicator, error handling, authenticated state card, and logout action.

## Stage Artifacts
- [Execution Plan](plan.md)
- [Implementation Log](implementation-log.md)
- [Architecture Review](architecture-review.md)
- [Security Review](security-review.md)
- [Test Results](test-results.md)
- [Performance Results](performance-results.md)
- [Deviations Log](deviations.md)
- [Known Issues](known-issues.md)
- [Commands Run](commands-run.md)
- [Files Changed](files-changed.md)
- [Completion Report](completion-report.md)

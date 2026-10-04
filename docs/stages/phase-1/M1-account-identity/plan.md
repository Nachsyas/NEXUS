# M1: Account & Identity — Execution Plan

## 1. Objectives & Scope
Deliver the core personal account and identity baseline for NEXUS Phase 1:
- Canonical domain separation: `User` != `AuthIdentity`.
- External Identity Provider: Sign in with Apple (SIWA) foundation.
- Token Architecture: Short-lived access token + rotating opaque refresh token family (ADR-020).
- Storage Security: Plaintext refresh token never persisted; Keychain on iOS.
- Multi-tenancy: Strict isolation and IDOR defense across all user endpoints.
- Client Interface: Minimal, focused Sign in with Apple UI and session coordinator.

## 2. Planned Workstreams

### Workstream 1: Governance & Decision Modeling
- Propose and ratify ADR-020 for session token format, signing algorithms, and rotation strategy.
- Ratify TBD-028 (Access Token Format & Signing Architecture) and TBD-029 (Default Token Expiration & Rotation TTLs) as RESOLVED via ADR-020.
- Document Phase 1 baseline vs future evolution path.

### Workstream 2: Database Schema & Migrations
- Define SQLAlchemy declarative models with UUIDv7 primary keys.
- Create tables: `users`, `auth_identities`, `user_preferences`, `sessions`, `rotated_token_hashes`.
- Add foreign keys, uniqueness constraints, and performance indexes.
- Author Alembic migration `0002_identity_and_sessions.py` with fully reversible downgrade path.

### Workstream 3: Backend Security & Domain Logic
- Implement `AppleIdentityVerifier` interface with production JWKS RS256 decoding and mock offline implementation.
- Implement token utilities: HS256 JWT access tokens, SHA-256 token hashing, `secrets.token_urlsafe(32)` refresh tokens.
- Implement `AuthService`:
  - First-time Apple login (user + identity + default preferences + session creation).
  - Repeat Apple login (identity lookup, last_login_at timestamp update, new session).
  - Session refresh with atomic rotation.
  - Refresh token reuse detection revoking entire session family with immediate commit.
  - Logout and manual session revocation.
- Implement `UserService`: profile read/update, preference lazy loading and update.
- Implement `get_current_user_context` dependency with database session validation.
- Implement algorithm confusion prevention and production secret validation.

### Workstream 4: REST API & Error Envelope Conformance
- Mount `/api/v1/auth` and `/api/v1/users` routes.
- Enforce canonical JSON error envelopes (`AUTH_INVALID_CREDENTIALS`, `AUTH_TOKEN_EXPIRED`, `AUTH_REFRESH_TOKEN_REUSED`, `FORBIDDEN_ACCESS`, `VALIDATION_ERROR`).

### Workstream 5: iOS Client Architecture
- Implement `NexusKeychainService` utilizing native iOS Security framework.
- Implement `NexusAPIClient` URLSession networking adapter.
- Implement `AuthManager` state machine using Swift structured concurrency.
- Implement `AuthView` SwiftUI interface with `SignInWithAppleButton`.

### Workstream 6: Verification & Governance Closure
- Backend unit and integration test suite covering 100% of critical auth paths.
- Multi-tenant isolation / IDOR tests covering profile, preferences, and session boundaries.
- Format, lint, and strict Mypy verification.
- iOS Simulator build verification.
- Author all 12 stage documentation artifacts at `docs/stages/phase-1/M1-account-identity/`.

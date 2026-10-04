# M1: Account & Identity — Architecture Review

## 1. Domain Separation Principles
The central architectural invariant delivered in Milestone M1 is:
$$\text{User} \neq \text{Authentication Provider}$$

- `User` represents the core canonical NEXUS identity, keyed by UUIDv7 (RFC 9562).
- `AuthIdentity` encapsulates the external identity relationship (`provider = 'APPLE'`, `provider_subject = '<apple-sub>'`).
- This decouples NEXUS internal data models and future multi-provider capabilities from Apple-specific identifiers. Apple email or subject claims are never used as foreign keys or primary keys in application tables.

```
+--------------------------------------------------------+
|                      User (UUIDv7)                     |
+--------------------------------------------------------+
        | 1:N                          | 1:1
        v                              v
+-----------------------+      +-------------------------+
|     AuthIdentity      |      |     UserPreference      |
| provider = 'APPLE'    |      | language, detail, etc.  |
| provider_subject      |      +-------------------------+
+-----------------------+
        |
        | 1:N
        v
+--------------------------------------------------------+
|                     Session (UUIDv7)                   |
| refresh_token_hash (SHA-256)                           |
| token_family_id (UUIDv7)                               |
| rotation_counter, expires_at, revoked_at               |
+--------------------------------------------------------+
        | 1:N
        v
+--------------------------------------------------------+
|                RotatedTokenHash                        |
| token_hash, session_id, token_family_id, rotated_at    |
+--------------------------------------------------------+
```

## 2. Token Security Architecture (ADR-020 — ACCEPTED)
- **Access Tokens:**
  - Stateless JSON Web Tokens (JWT) signed with HMAC-SHA256 (HS256).
  - Claims: `sub` (User UUIDv7), `session_id` (Session UUIDv7), `exp` (15m default), `iat`, `jti`.
  - Canonical configuration: `ACCESS_TOKEN_EXPIRE_MINUTES: int = 15` in `app.core.config.Settings`. Not hardcoded as magic constants.
  - Every authenticated request verifies both the cryptographic JWT signature (strictly constrained to `HS256`) and the active session state in PostgreSQL.
- **Refresh Tokens:**
  - High-entropy cryptographic strings (`secrets.token_urlsafe(32)`, 256 bits).
  - Canonical configuration: `REFRESH_TOKEN_EXPIRE_DAYS: int = 30` in `app.core.config.Settings`.
  - Plaintext refresh tokens are **never stored** in the database; only their SHA-256 hash is persisted.
  - Refresh rotation is atomic: when presented, the existing hash is moved to `rotated_token_hashes`, a new token is generated and hashed into `sessions.refresh_token_hash`, and the rotation counter is incremented.
- **Token Family Reuse Detection:**
  - If a refresh token whose hash matches an entry in `rotated_token_hashes` is received, it signifies token replay or theft.
  - The entire token family (`token_family_id`) is immediately marked revoked with `revocation_reason = 'REUSE_DETECTED'`.
  - This change is committed immediately to the database prior to raising `RefreshTokenReusedError` to ensure subsequent calls using any token in that family are permanently rejected with `401 AUTH_REFRESH_TOKEN_REUSED`.
- **Evolutionary Governance:**
  - HS256 is the ratified Phase 1 baseline. Asymmetric signing (RS256/ES256) or distributed token verification can be evaluated in subsequent phases via normal ADR governance without breaking database schema or client contracts.

## 3. Provider Boundary Abstraction
- The `AppleIdentityVerifier` abstract class provides an isolated interface for verifying credentials.
- `ProductionAppleVerifier` connects to Apple JWKS, caches keys for 24 hours, validates RS256 signatures, and confirms `iss` and `aud`.
- `MockAppleVerifier` allows deterministic, offline integration testing without making external network calls to Apple during CI/test execution.
- **Verification Status:** Production verification code exists; unit tests pass with mock verifier; iOS UI builds cleanly; `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`.

## 4. Multi-Tenant Authorization Guard
- Every session operation (`/api/v1/auth/sessions/{id}`) and preference mutation (`/api/v1/me/preferences`) strictly checks `session.user_id == current_user.user_id`.
- Attempts to query, mutate, or revoke another user's session or profile immediately return `403 FORBIDDEN_ACCESS`.
- Explicit 6-dimension cross-user isolation test suite verified in CI.

## 5. iOS Client Concurrency & Storage
- Native `Security` framework with `kSecClassGenericPassword` and `kSecAttrAccessibleAfterFirstUnlock`.
- Tokens are never persisted to `UserDefaults`, `SwiftData`, or plain files.
- Uses Swift 6 Approachable Concurrency with `@MainActor` state coordination and `nonisolated` DTOs.

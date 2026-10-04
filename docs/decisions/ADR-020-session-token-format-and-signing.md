# ADR-020: Session Token Format, Signing Architecture, and Rotation Strategy

**Status:** ACCEPTED  
**Date:** 2026-10-04  
**Deciders:** User (Formal Ratification 2026-10-04)  
**Resolves:** TBD-028 (RESOLVED), TBD-029 (RESOLVED)  

## Context
Milestone M1 introduces authentication and session management for NEXUS. The system requires a secure, auditable, and performant session credential strategy between iOS clients (and later Mac Agent nodes) and the backend modular monolith.

Key requirements:
1. Short-lived access token for stateless API authorization without requiring a database query on every micro-request.
2. Rotating, long-lived refresh token for maintaining continuous authenticated sessions across client restarts.
3. Cryptographic protection against token forgery, tampering, and theft.
4. Immediate revocation support (logout, specific session revocation, remote wipe).
5. Refresh token reuse detection (stolen token replay detection triggering family revocation).
6. Absolute multi-tenant isolation and secure, unguessable identifiers.

## Decision
Adopt **HMAC-SHA256 (HS256) JWT** for short-lived access tokens and **Cryptographically Random Opaque Hashed Strings** for rotating refresh tokens as the approved Phase 1 baseline:

1. **Access Token Format (RFC 7519 JWT):**
   - Signed using `HS256` with a backend secret key (`JWT_SECRET_KEY`) stored in secure environment configuration.
   - Claims:
     - `sub`: User ID (RFC 9562 UUIDv7 string)
     - `session_id`: Active Session ID (UUIDv7 string)
     - `exp`: Expiration Unix timestamp (UTC)
     - `iat`: Issued-at Unix timestamp (UTC)
     - `jti`: Unique token ID (UUIDv7)
   - Default lifetime: 15 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`, not hardcoded as a magic constant).
   - Verification explicitly constrains algorithm to `["HS256"]`; unexpected algorithms (e.g. `none`, asymmetric) are strictly rejected.

2. **Refresh Token Format (Opaque & Hashed):**
   - 256-bit entropy baseline generated via `secrets.token_urlsafe(32)`.
   - Plaintext refresh tokens MUST NOT be persisted server-side.
   - Server persists only the SHA-256 digest (`refresh_token_hash`).
   - Default lifetime: 30 days (configurable via `REFRESH_TOKEN_EXPIRE_DAYS`, not hardcoded as a magic constant).

3. **Rotation & Reuse Defense:**
   - Every refresh operation issues a new refresh token and marks the previous refresh token as rotated/consumed in `rotated_token_hashes`.
   - Each session belongs to a `token_family_id`.
   - Presenting an already-rotated/consumed refresh token triggers reuse detection: the entire session family is immediately revoked with status `REUSE_DETECTED`, committed durably to PostgreSQL, and `AUTH_REFRESH_TOKEN_REUSED` is returned.

4. **Session Revocation:**
   - Active sessions are recorded in the `sessions` table.
   - Revocation sets `revoked_at` timestamp.
   - Logout, user deletion, or manual session termination invalidates the session immediately.
   - Revoked sessions cannot be used to refresh tokens.

5. **HS256 Security Invariants:**
   - Signing secret is generated with high entropy (>= 32 characters / 256 bits).
   - Signing secret is not committed to Git (loaded from `.env` / environment).
   - Signing secret is never logged (sanitized to `[REDACTED]` in logging middleware).
   - Production environment rejects development placeholder secrets via Settings validation.
   - Token algorithm is explicitly constrained to `HS256` during decoding (`algorithms=[settings.JWT_ALGORITHM]`).
   - Future key rotation remains possible by rotating `JWT_SECRET_KEY` or adding key ID (`kid`) support in configuration.

## Evolution Path
This decision is approved as the Phase 1 baseline. It is NOT an immutable lifetime guarantee. Future changes to:
- signing architecture;
- token lifetime;
- asymmetric access-token signing (RS256/ES256);
- distributed token verification;
may evolve later through evidence-based ADR governance.

## Alternatives Considered
- *Opaque Access Tokens with Redis lookup on every call:* Fully stateful, but adds network/DB I/O latency to every API request and couples core request authorization to Redis availability.
- *Asymmetric RS256/ES256 JWT:* Adds cryptographic verification CPU overhead without benefit for a Phase 1 modular monolith where the backend is the sole token issuer and verifier. Can be adopted in later phases if distributed verifiers are introduced.

## Consequences
- Fast, secure stateless validation of access tokens with sub-millisecond CPU overhead.
- Immediate revocation enforceable via session record checks and short 15-minute token TTL.
- Zero plaintext refresh token exposure in database dumps or storage leaks.
- Seamless compatibility with iOS URLSession and Apple Keychain.

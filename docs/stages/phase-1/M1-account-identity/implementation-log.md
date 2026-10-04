# M1: Account & Identity — Implementation Log

## Session 1: Governance, Dependencies & Schema
- Formulated proposed **ADR-020** (`docs/decisions/ADR-020-session-token-format-and-signing.md`) establishing HS256 JWT access tokens, opaque 256-bit SHA-256 hashed refresh tokens, and token family replay detection.
- Registered **TBD-028** and **TBD-029** in `docs/architecture/TBD-REGISTRY.md`.
- Added `pyjwt[crypto]>=2.8.0` to `backend/pyproject.toml` via `uv add` (`pyjwt==2.15.1`, `cryptography==50.0.2`).
- Defined domain models:
  - `User` and `UserPreference` in `backend/app/domains/users/models.py`.
  - `AuthIdentity`, `Session`, and `RotatedTokenHash` in `backend/app/domains/auth/models.py`.
- Authored Alembic migration `0002_identity_and_sessions.py`.
- Executed migration forward: `uv run alembic upgrade head`.
- Tested migration rollback: `uv run alembic downgrade -1` (verified table deletion).
- Re-executed migration: `uv run alembic upgrade head` (verified clean recreation).

## Session 2: Backend Domain & Security Implementation
- Created `backend/app/domains/auth/security.py`:
  - `create_access_token`: Generates signed HS256 JWT with `sub`, `session_id`, `exp`, `iat`, `jti`.
  - `decode_access_token`: Validates JWT claims, signature, and expiration, explicitly constrained to `["HS256"]`.
  - `generate_opaque_token`: Creates 32-byte cryptographic random token using `secrets.token_urlsafe(32)`.
  - `hash_token`: Computes SHA-256 hex digest for database indexing and comparison.
  - Custom exceptions: `AuthenticationError`, `InvalidCredentialsError`, `TokenExpiredError`, `RefreshTokenReusedError`, `ForbiddenAccessError`.
- Created `backend/app/domains/auth/apple_verifier.py`:
  - `AppleIdentityVerifier` abstract base class.
  - `ProductionAppleVerifier`: Async fetch and caching of Apple JWKS, unverified header key lookup, RSA public key construction, and RS256 token verification.
  - `MockAppleVerifier`: Offline deterministic verification for testing.
- Created schemas:
  - `backend/app/domains/users/schemas.py`: Pydantic models for user profile and preferences.
  - `backend/app/domains/auth/schemas.py`: Pydantic models for Apple login, token refresh, sessions, and responses.
- Implemented services:
  - `backend/app/domains/users/service.py`: `UserService` methods for fetching user, updating display name, and managing user preferences.
  - `backend/app/domains/auth/service.py`: `AuthService` handling full authentication lifecycle:
    - `login_with_apple`: User creation / identity resolution, default preferences, active session creation.
    - `refresh_session`: Opaque token hash lookup, atomic rotation with `RotatedTokenHash` archival.
    - `refresh_session` reuse detection: Checks `RotatedTokenHash`. When replayed, revokes entire `token_family_id` with `REUSE_DETECTED` and immediately commits to database before raising `RefreshTokenReusedError`.
    - `logout`: Revokes active session.
    - `list_user_sessions`: Queries non-revoked active sessions for user.
    - `revoke_user_session`: Validates session ownership and terminates session.
- Implemented dependencies & API routes:
  - `backend/app/core/dependencies.py`: `get_current_user_context` extracting Bearer token, decoding claims, verifying database session active state and expiration.
  - `backend/app/api/v1/auth.py`: Endpoints for `/auth/apple`, `/auth/refresh`, `/auth/logout`, `/auth/sessions`, `/auth/sessions/{session_id}`.
  - `backend/app/api/v1/users.py`: Endpoints for `/me`, `/me/preferences`.
  - `backend/app/api/v1/router.py`: Mounted auth and user routers.
  - `backend/app/main.py`: Configured custom exception handlers mapping domain exceptions to canonical API envelope error responses.

## Session 3: Testing & Backend Verification
- Created comprehensive test suite in `backend/tests/test_auth_identity.py` covering all core auth flows.
- Resolved transaction rollback issue on reuse detection by executing explicit commit prior to raising exception.
- Verified test suite: 20/20 backend tests passing.
- Verified code quality: Ruff check clean, Ruff format clean, Mypy strict clean (0 errors across 30 files).

## Session 4: iOS Client Implementation & Build
- Created `apps/ios/NEXUS/Data/Keychain/KeychainService.swift`:
  - Implemented `NexusKeychainService` conforming to `KeychainServiceProtocol`.
  - Uses `kSecClassGenericPassword` and `kSecAttrAccessibleAfterFirstUnlock`.
- Created `apps/ios/NEXUS/Domain/Auth/AuthModels.swift`:
  - `NexusUser`, `AuthTokens`, `AuthResponseData`, `APIEnvelope<T>`, `AuthState`.
  - Annotated models with `nonisolated` for Swift 6 Approachable Concurrency compatibility.
- Created `apps/ios/NEXUS/Data/Network/NexusAPIClient.swift`:
  - Network client with `loginWithApple`, `fetchCurrentUser`, and `logout`.
- Created `apps/ios/NEXUS/Domain/Auth/AuthManager.swift`:
  - `@MainActor` observable auth state machine coordinating Keychain, API client, and UI.
- Created `apps/ios/NEXUS/Features/Auth/AuthView.swift`:
  - SwiftUI interface providing Sign in with Apple button, loading spinner, error display, and authenticated user view with logout action.
- Updated `apps/ios/NEXUS/App/ContentView.swift` to render `AuthView`.
- Verified iOS project build:
  `xcodebuild -project apps/ios/NEXUS.xcodeproj -scheme NEXUS -destination 'generic/platform=iOS Simulator' build CODE_SIGNING_ALLOWED=NO`
  Build succeeded with 0 errors.
- Verified macOS agent product build:
  `swift build --package-path apps/mac-agent`
  Build succeeded in 0.29s.

## Session 5: Decision Ratification, Security Hardening & Milestone Closure
- Formally ratified **ADR-020** (Status: `ACCEPTED` by user).
- Marked **TBD-028** (Access Token Format & Signing) and **TBD-029** (Token Expiration TTLs) as `RESOLVED`.
- Added strict production secret validator in `backend/app/core/config.py` preventing placeholder values and requiring minimum 256 bits of entropy.
- Added comprehensive token algorithm safety tests (verifying rejection of `none` algorithm, wrong signature, malformed tokens, and expired tokens).
- Added multi-tenant cross-user isolation tests verifying all 6 resource isolation operations (read/modify profile, read/modify preferences, list/revoke sessions).
- Added test verifying revoked sessions cannot be refreshed.
- All 23 backend tests passing cleanly.
- Canonical stage documentation relocated to `docs/stages/phase-1/M1-account-identity/` (symlink removed).
- Documented factual verification status: `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`.
- Corrected roadmap drift: Milestone M2 is `Projects`, Milestone M3 is `Memory Core`.

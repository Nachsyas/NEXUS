# M1: Account & Identity — Files Changed

## 1. Architecture & Governance
- `docs/decisions/ADR-020-session-token-format-and-signing.md`: Created and ratified ADR-020 (Status: ACCEPTED).
- `docs/decisions/README.md`: Added ADR-020 to accepted decisions registry.
- `docs/context/ACTIVE-DECISIONS.md`: Added ADR-020 to active register table with ACCEPTED status.
- `docs/architecture/TBD-REGISTRY.md`: Registered and marked TBD-028 and TBD-029 as RESOLVED.
- `docs/stages/phase-1/M1-account-identity/`: Established canonical stage directory path.

## 2. Backend Infrastructure & Core
- `backend/pyproject.toml`: Added `pyjwt[crypto]>=2.8.0`.
- `backend/app/core/config.py`: Added JWT secret, algorithms, expiration TTLs, Apple client configurations, and production secret security validator.
- `backend/app/core/dependencies.py`: Added `get_current_user_context` dependency and `UserContext`.
- `backend/app/core/responses.py`: Created canonical response helper `api_success`.
- `backend/app/main.py`: Configured global exception handlers for `AuthenticationError` and `RequestValidationError`.
- `backend/alembic/env.py`: Imported `users` and `auth` models into Alembic metadata.
- `backend/alembic/versions/0002_identity_and_sessions.py`: Migration creating all M1 tables, foreign keys, and indexes.

## 3. Backend Domains & API
- `backend/app/domains/users/models.py`: Created `User` and `UserPreference` models with UUIDv7 PKs.
- `backend/app/domains/users/schemas.py`: Created schemas for user profile and preference requests/responses.
- `backend/app/domains/users/service.py`: Created `UserService` for profile and preference operations.
- `backend/app/domains/auth/models.py`: Created `AuthIdentity`, `Session`, and `RotatedTokenHash` models.
- `backend/app/domains/auth/schemas.py`: Created schemas for Apple login, refresh, sessions, and envelopes.
- `backend/app/domains/auth/security.py`: Implemented JWT creation/decoding (algorithm strictly constrained to HS256), token hashing, and auth exceptions.
- `backend/app/domains/auth/apple_verifier.py`: Implemented `AppleIdentityVerifier`, `ProductionAppleVerifier`, and `MockAppleVerifier`.
- `backend/app/domains/auth/service.py`: Implemented `AuthService` handling full login, rotation, reuse detection (with explicit pre-exception commit), logout, and session lifecycle.
- `backend/app/api/v1/auth.py`: Implemented auth endpoints.
- `backend/app/api/v1/users.py`: Implemented user profile and preference endpoints.
- `backend/app/api/v1/router.py`: Mounted auth and user routers under `/api/v1`.

## 4. Backend Tests
- `backend/tests/test_auth_identity.py`: Authored 15 tests covering first login, repeat login, unverified token rejection, profile access/mutation, preferences flow, token rotation, reuse detection, session listing/revocation, logout, revoked session refresh rejection, multi-tenant 6-dimension isolation, token algorithm confusion/expiration safety, and production secret validation.
- Overall backend test suite expanded to 23 passing tests.

## 5. iOS Client (`apps/ios/NEXUS/`)
- `apps/ios/NEXUS/Data/Keychain/KeychainService.swift`: Native Keychain service using Security framework.
- `apps/ios/NEXUS/Data/Network/NexusAPIClient.swift`: Network client with URLSession.
- `apps/ios/NEXUS/Domain/Auth/AuthModels.swift`: User, token, session, and API envelope models with `nonisolated` annotations.
- `apps/ios/NEXUS/Domain/Auth/AuthManager.swift`: Observable auth state machine.
- `apps/ios/NEXUS/Features/Auth/AuthView.swift`: SwiftUI Sign in with Apple and session management screen.
- `apps/ios/NEXUS/App/ContentView.swift`: Integrated `AuthView` into main content view.

## 6. Stage Documentation (`docs/stages/phase-1/M1-account-identity/`)
- `README.md`, `plan.md`, `implementation-log.md`, `architecture-review.md`, `security-review.md`, `test-results.md`, `performance-results.md`, `deviations.md`, `known-issues.md`, `commands-run.md`, `files-changed.md`, `completion-report.md`.

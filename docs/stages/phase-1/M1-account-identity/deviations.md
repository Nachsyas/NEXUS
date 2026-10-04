# M1: Account & Identity — Deviations Log

## 1. Intentional Architectural Scope Adjustments

### Deviation 1: Explicit Database Commit on Token Reuse Detection
- **Initial Implementation:** When refresh token reuse was detected, sessions in the token family were marked revoked with `s.revoked_at = now`, followed by `await db.flush()` and raising `RefreshTokenReusedError`.
- **Observed Behavior:** FastAPI's `get_db` async generator catches any unhandled or domain exception raised out of route handlers and issues a database `ROLLBACK`. Consequently, the security revocation was reverted, allowing potential race conditions or subsequent reuse attempts.
- **Adjustment:** In `AuthService.refresh_session`, before raising `RefreshTokenReusedError`, the service explicitly invokes `await db.commit()`. This guarantees the revocation of the compromised token family is durably persisted to PostgreSQL regardless of downstream exception handling.
- **Classification:** Security Invariant Enforcement.

### Deviation 2: Non-Isolated Conformance for Swift 6 Approachable Concurrency
- **Initial Implementation:** Standard Swift structs without actor isolation keywords.
- **Observed Behavior:** The Xcode target configured with `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` caused Codable conformance in generic types (`APIEnvelope<T>`) to be marked main-actor isolated, conflicting with URLSession background thread decoding requirements.
- **Adjustment:** Explicitly marked DTO models (`NexusUser`, `AuthTokens`, `AuthResponseData`, `APIEnvelope`, etc.) and non-UI service classes (`NexusAPIClient`, `NexusKeychainService`) as `nonisolated`.
- **Classification:** Compiler Compatibility & Swift Concurrency Standard Compliance.

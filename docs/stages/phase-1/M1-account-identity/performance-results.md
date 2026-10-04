# M1: Account & Identity — Performance Results

## 1. Backend Performance Baseline

- **Full Test Suite Execution Time:** ~1.06s for 23 async test cases.
- **Average Authentication Roundtrip (Local Test Client):** ~12ms per request.
- **Cryptographic Operations Benchmark:**
  - HS256 JWT encoding/decoding: < 0.2ms per token.
  - SHA-256 token hashing: < 0.05ms per operation.
  - Secret random generation (`secrets.token_urlsafe(32)`): < 0.02ms.

## 2. Database Index Coverage & Query Optimization

All database lookup paths in `app/domains/auth` and `app/domains/users` utilize indexed columns:
1. `auth_identities.ix_auth_identities_provider_subject`: Unique composite B-tree index on `(provider, provider_subject)` ensuring $O(\log N)$ identity lookup on login.
2. `sessions.ix_sessions_refresh_token_hash`: Unique B-tree index on `refresh_token_hash` ensuring $O(\log N)$ session lookup during token refresh.
3. `sessions.ix_sessions_token_family_id`: B-tree index on `token_family_id` ensuring instant retrieval and revocation of session families during reuse detection.
4. `rotated_token_hashes.ix_rotated_token_hashes_token_hash`: B-tree index ensuring $O(\log N)$ replay detection checks.
5. `user_preferences.ix_user_preferences_user_id`: Unique index ensuring 1:1 foreign key lookup in sub-millisecond time.

## 3. iOS Client Performance
- Universal binary compile time: ~12s clean build.
- Incremental compile time: < 1.5s.
- Zero main-thread blocking during Keychain cryptographic operations or network exchanges.

# NEXT ACTIONS — Post-M0 / Transition to M1

1. **User Review of M0 Completion:** Review final M0 Foundation completion report and test verifications.
2. **Authorize Milestone M1 (Account & Identity Foundation):**
   - User grants explicit authorization to proceed with Phase 1 / Milestone M1.
3. **M1 Planning & Execution (Post-Authorization):**
   - Resolve M1-related architectural decisions (e.g. password hashing argon2id parameters, session token lifespans).
   - Implement user entity models, repositories, and authentication services in `backend/app/domain/identity/`.
   - Implement authentication endpoints (`POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`).
   - Implement iOS Identity & Keychain onboarding feature in `apps/ios/NEXUS/Features/Auth/`.
   - Apply migrations for users and sessions tables.

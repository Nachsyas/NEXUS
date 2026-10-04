# NEXT ACTIONS — Post-M0 / Transition to M1

1. **M0 Governance Ratification & Stage Closure:**
   - Formal user ratification of ADR-016 through ADR-019: **COMPLETED**.
   - M0 Foundation: **CLOSED — COMPLETE**.
   - M1 Readiness: **UNBLOCKED**.

2. **Milestone M1 Authorization Gateway:**
   - Awaiting explicit user execution trigger: `START M1 ACCOUNT & IDENTITY`.
   - Execution halts strictly at the M0/M1 milestone boundary until this command is provided.

3. **M1 Planning & Execution (Post-Authorization Roadmap):**
   - Setup `docs/stages/M1-account-identity/` stage workspace and verification plan.
   - Design and verify identity domain models (User, Session, Device) using RFC 9562 UUIDv7 primary keys.
   - Implement password hashing via Argon2id and JWT/session token management in `backend/app/domain/identity/`.
   - Implement authentication endpoints (`POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `GET /api/v1/auth/me`).
   - Create Alembic migrations for identity schema.
   - Implement iOS Identity & Keychain onboarding feature in `apps/ios/NEXUS/Features/Auth/`.
   - Validate with unit, integration, and security tests.

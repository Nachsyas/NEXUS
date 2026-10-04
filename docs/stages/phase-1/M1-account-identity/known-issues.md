# M1: Account & Identity — Known Issues & Limitations

## 1. Governance State
- **ADR-020 (Session Token Format & Signing):** Formally approved and ratified by user as `ACCEPTED` (2026-10-04).
- **TBD-028 (Access Token Format & Signing Architecture):** Formally `RESOLVED` via ADR-020 as Phase 1 baseline.
- **TBD-029 (Default Token Expiration & Rotation TTLs):** Formally `RESOLVED` via ADR-020 (15m access / 30d refresh).

## 2. Environment & Network Caveats
- **Live Apple SIWA Network Verification:**
  - Status: `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`.
  - In local development and unit tests, `MockAppleVerifier` is activated by default to provide 100% reliable, fast, offline automated testing.
  - Production code (`ProductionAppleVerifier`) is fully implemented with Apple JWKS RS256 decoding, issuer verification, and audience matching.
  - Manual end-to-end verification against live Apple servers requires a provisioned Apple Developer Account Team ID, Services ID, and runtime device execution.
- **Localhost Networking on Physical iOS Devices:**
  - In `NexusAPIClient`, default baseURL is `http://127.0.0.1:8000/api/v1`, which works on iOS Simulator. For testing on physical hardware, this must be pointed to the LAN IP address of the development workstation or staging server.

# Deviations: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03  

## 1. Architectural Deviations
*None.* The implementation strictly adheres to the approved Phase 1 specification and accepted ADRs.

## 2. Operational & Environment Deviations

### Deviation DEV-001: Local Host Port Conflict Adjustment
- **Context:** The standard local Docker Compose ports for PostgreSQL (`5432`) and Redis (`6379`) were already bound on the host machine by external services (`intelligent-commerce-sync-postgres` and `intelligent-commerce-sync-redis`).
- **Initial Plan:** Expose containers on standard default ports 5432 and 6379.
- **Adjustment Made:** Mapped PostgreSQL container host port to `5433` and Redis container host port to `6380` via `.env` and `docker-compose.yml` environment variable overrides (`${POSTGRES_PORT:-5433}:5432`, `${REDIS_PORT:-6380}:6379`).
- **Impact:** Completely benign. Both host environments coexist seamlessly without disrupting the user's running projects. Application runtime connects cleanly to `localhost:5433` and `localhost:6380`.

### Deviation DEV-002: iOS Starter Scaffold Platforms Normalization
- **Context:** The starter Xcode project migrated from the repository root inherited `SUPPORTED_PLATFORMS = "iphoneos iphonesimulator macosx xros xrsimulator"` and `TARGETED_DEVICE_FAMILY = "1,2,7"`.
- **Initial Plan:** Compile and verify starter project with inherited settings.
- **Adjustment Made:** Removed `macosx`, `xros`, and `xrsimulator` from `SUPPORTED_PLATFORMS`, reset `SDKROOT` to `iphoneos`, and set `TARGETED_DEVICE_FAMILY = "1,2"`.
- **Impact:** Strictly preserves the architectural boundary between the NEXUS iOS Client and NEXUS Mac Agent nodes. The iOS app builds cleanly for iPhone and iPad on iOS Simulator, while preventing the iOS app from compiling as a macOS Catalyst executable that might conflate with the Mac Agent.

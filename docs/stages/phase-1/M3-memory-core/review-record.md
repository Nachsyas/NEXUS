# Milestone M3: Pre-Merge Review Record

## Review Metadata
- **Milestone:** M3 — Memory Core & Control Center
- **Pull Request:** #2 (`milestone/m3-memory-core` -> `main`)
- **Base Commit:** `e1168161ace9f13c75cf31df8f9bac9472808397`
- **Initial Head Reviewed:** `f949afa0742fdf24a9e1899ec6a060a69d463c3f`
- **Review Date:** 2026-10-05

## Findings Summary
1. **Embedding Governance Ambiguity:** `TBD-030` was introduced creating duplicate governance ambiguity against pre-existing `TBD-004`.
2. **Premature Dimension Locking:** Database column in Alembic migration and SQLAlchemy model was specified as `Vector(1536)` rather than unconstrained `Vector()`.
3. **Embedding Vector Validation:** Lack of runtime validation for vector non-emptiness, finiteness (no NaN/Inf), and dimension consistency.
4. **iOS Sensitivity Enum Parity:** Backend supported `RESTRICTED` sensitivity, but iOS Swift model omitted `RESTRICTED`, which would break JSON decoding.
5. **Stale Embedding Vector After PATCH:** Updating `value_text` on an active memory without an active embedding provider preserved the old vector instead of setting it to `NULL`.
6. **Expired Memory Reassertion Bug:** Reasserting an expired memory returned the expired row or superseded it inappropriately rather than transitioning the old row to `EXPIRED` and generating a new `ACTIVE` memory.
7. **Query Status Coherence:** `status=EXPIRED` query filtering lacked coherence with lazy expiration state.
8. **Missing Concurrent Conflict Test:** Need explicit test verifying concurrent conflicting writes under user row-locking.
9. **API Contract Desynchronization:** Section 6 of `docs/api/api-contract.md` lacked full parameter, response envelope, and provenance details.
10. **Query Filter Types:** `status` and `memory_type` query parameters were untyped strings rather than validated enums.
11. **PATCH Null-Clear Semantics:** `MemoryUpdate` did not differentiate omitted fields from explicit `null` via `model_fields_set`.
12. **Pre-Validation Secret Reflection:** Pydantic v2 `RequestValidationError` default serialization echoed raw invalid input values in HTTP 422 responses.
13. **Security Evidence Honesty:** Overstated claims regarding "standard credential datasets" and "Zero False Positives".
14. **Performance Measurement First:** Fictitious "Target SLAs" declared prior to distributed benchmarks.

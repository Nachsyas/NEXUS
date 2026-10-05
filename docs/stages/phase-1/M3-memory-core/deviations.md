# Milestone M3: Deviations

## 1. Documented Deviations
1. **Explicit Sanitization in Global Validation Handler:**
   - *Observation:* Default Pydantic v2 `RequestValidationError.errors()` contains raw user `input` fields and a `ctx` mapping containing un-serializable raw `ValueError` exception objects when custom `@model_validator` or `@field_validator` triggers. Reflecting raw `input` risks echoing sensitive credentials/secrets when payloads fail validation, and raw `ValueError` instances break Starlette JSON serialization.
   - *Resolution:* In `backend/app/main.py`, the `RequestValidationError` handler deliberately constructs explicit sanitized error dictionaries. `loc`, `msg`, and `type` fields are preserved; unsafe raw `input` is completely omitted; and `ctx` keys excluding raw `error` objects are converted to strings. This prevents secret reflection and guarantees valid, serializable JSON responses across all validation failures.

2. **Embedding Provider Decoupling (TBD-004):**
   - *Observation:* Per product architecture, proprietary embedding services and concrete dimensions must not be hardcoded without formal governance.
   - *Resolution:* Default production provider (`UnavailableEmbeddingProvider`) raises `EmbeddingUnavailableError` (HTTP 503 `MEMORY_EMBEDDING_UNAVAILABLE`). Runtime dimension contracts are declared via `EmbeddingProvider.dimension` protocol property. Automated tests utilize `DeterministicTestEmbeddingProvider` generating deterministic unit-normalized vectors. Formally recorded as `TBD-004` in `TBD-REGISTRY.md`.

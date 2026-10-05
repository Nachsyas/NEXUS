# Milestone M3: Deviations

## 1. Documented Deviations
1. **JSON Encoding in Global Validation Handler:**
   - *Observation:* Pydantic v2 `RequestValidationError.errors()` includes a `ctx` dictionary containing raw `ValueError` exception objects when custom `@model_validator` or `@field_validator` raises. Starlette's `JSONResponse` failed to serialize raw `ValueError` instances directly with `json.dumps`.
   - *Resolution:* Wrapped `exc.errors()` with FastAPI's `jsonable_encoder(exc.errors())` in `validation_exception_handler` within `backend/app/main.py`. This ensures 100% compliant JSON responses for all validation errors across the entire application without altering API contract structure.

2. **Embedding Provider Decoupling (TBD-004):**
   - *Observation:* Per product boundary, proprietary embedding services must not be hardcoded without formal governance.
   - *Resolution:* Default production provider (`UnavailableEmbeddingProvider`) raises `EmbeddingUnavailableError` (HTTP 503 `MEMORY_EMBEDDING_UNAVAILABLE`). Automated tests utilize `DeterministicTestEmbeddingProvider` generating deterministic 1536-dimensional unit vectors. Formally recorded as `TBD-004` in `TBD-REGISTRY.md`.

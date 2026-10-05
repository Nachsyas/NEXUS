class MemoryError(Exception):
    """Base exception for Memory domain errors."""

    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class MemoryNotFoundError(MemoryError):
    def __init__(self, message: str = "Memory not found.") -> None:
        super().__init__(code="MEMORY_NOT_FOUND", message=message, status_code=404)


class MemorySecretRejectedError(MemoryError):
    def __init__(
        self, message: str = "Memory content rejected by NEVER_STORE secret safety policy."
    ) -> None:
        super().__init__(code="MEMORY_SECRET_REJECTED", message=message, status_code=400)


class MemoryInvalidStateError(MemoryError):
    def __init__(self, message: str = "Invalid memory state for this operation.") -> None:
        super().__init__(code="MEMORY_INVALID_STATE", message=message, status_code=409)


class MemoryScopeError(MemoryError):
    def __init__(self, message: str = "Invalid project scope for memory type.") -> None:
        super().__init__(code="MEMORY_INVALID_SCOPE", message=message, status_code=422)


class EmbeddingUnavailableError(MemoryError):
    def __init__(
        self,
        message: str = "Production embedding provider is not configured. (TBD-004)",
    ) -> None:
        super().__init__(code="MEMORY_EMBEDDING_UNAVAILABLE", message=message, status_code=503)


class EmbeddingValidationError(MemoryError):
    def __init__(self, message: str = "Invalid embedding vector generated.") -> None:
        super().__init__(code="MEMORY_EMBEDDING_INVALID", message=message, status_code=500)

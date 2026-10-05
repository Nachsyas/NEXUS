import hashlib
import math
from typing import Protocol

from app.domains.memories.exceptions import (
    EmbeddingUnavailableError,
    EmbeddingValidationError,
)


def validate_embedding_vector(
    vector: list[float] | None, expected_dim: int | None = None
) -> list[float]:
    """Validate embedding vector for non-emptiness, finiteness, and dimension consistency.

    Does NOT log or echo raw vector data.
    """
    if not vector:
        raise EmbeddingValidationError("Embedding vector is empty.")

    dim = len(vector)
    if expected_dim is not None and dim != expected_dim:
        raise EmbeddingValidationError(
            f"Embedding vector dimension mismatch: expected {expected_dim}, got {dim}."
        )

    for i, val in enumerate(vector):
        if not isinstance(val, (int, float)) or not math.isfinite(val):
            raise EmbeddingValidationError(
                f"Embedding vector contains non-finite or invalid numeric value at index {i}."
            )

    return vector


class EmbeddingProvider(Protocol):
    """Protocol for embedding generation providers."""

    @property
    def dimension(self) -> int:
        """Declared vector dimension produced by this provider."""
        ...

    async def embed(self, text: str) -> list[float]:
        """Generate vector embedding for a single text."""
        ...

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate vector embeddings for a list of texts."""
        ...


class UnavailableEmbeddingProvider:
    """Default production provider when no production embedding model/service is configured (TBD-004)."""

    @property
    def dimension(self) -> int:
        raise EmbeddingUnavailableError(
            "Production embedding provider is not configured. (TBD-004)"
        )

    async def embed(self, _text: str) -> list[float]:
        raise EmbeddingUnavailableError(
            "Production embedding provider is not configured. (TBD-004)"
        )

    async def embed_batch(self, _texts: list[str]) -> list[list[float]]:
        raise EmbeddingUnavailableError(
            "Production embedding provider is not configured. (TBD-004)"
        )


class DeterministicTestEmbeddingProvider:
    """Deterministic, unit-normalized embedding provider for test suite verification.

    NOTE: Used strictly for integration and unit testing. NOT presented as production semantic quality.
    """

    def __init__(self, dimension: int = 1536) -> None:
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def _generate_vector(self, text: str) -> list[float]:
        clean = text.strip().lower()
        seed = hashlib.sha512(clean.encode("utf-8")).digest()
        raw_values: list[float] = []
        for i in range(self._dimension):
            h = hashlib.sha256(seed + i.to_bytes(4, "big")).digest()
            val = int.from_bytes(h[:4], "big", signed=True) / (2**31 - 1)
            raw_values.append(val)
        norm = math.sqrt(sum(x * x for x in raw_values)) or 1.0
        vec = [x / norm for x in raw_values]
        return validate_embedding_vector(vec, expected_dim=self._dimension)

    async def embed(self, text: str) -> list[float]:
        return self._generate_vector(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._generate_vector(t) for t in texts]


# Module-level active provider registry
_active_provider: EmbeddingProvider = UnavailableEmbeddingProvider()


def get_embedding_provider() -> EmbeddingProvider:
    """Return currently configured embedding provider."""
    return _active_provider


def set_embedding_provider(provider: EmbeddingProvider) -> None:
    """Configure active embedding provider."""
    global _active_provider
    _active_provider = provider


def reset_embedding_provider() -> None:
    """Reset to default UnavailableEmbeddingProvider."""
    global _active_provider
    _active_provider = UnavailableEmbeddingProvider()

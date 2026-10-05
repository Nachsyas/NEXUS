import hashlib
import math
from typing import Protocol

from app.domains.memories.exceptions import EmbeddingUnavailableError


class EmbeddingProvider(Protocol):
    """Protocol for embedding generation providers."""

    async def embed(self, text: str) -> list[float]:
        """Generate vector embedding for a single text."""
        ...

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate vector embeddings for a list of texts."""
        ...


class UnavailableEmbeddingProvider:
    """Default production provider when no production embedding model/service is configured (TBD-030)."""

    async def embed(self, _text: str) -> list[float]:
        raise EmbeddingUnavailableError(
            "Production embedding provider is not configured. (TBD-030)"
        )

    async def embed_batch(self, _texts: list[str]) -> list[list[float]]:
        raise EmbeddingUnavailableError(
            "Production embedding provider is not configured. (TBD-030)"
        )


class DeterministicTestEmbeddingProvider:
    """Deterministic, unit-normalized 1536-dimensional embedding provider for test suite verification.

    NOTE: Used strictly for integration and unit testing. NOT presented as production semantic quality.
    """

    def __init__(self, dimension: int = 1536) -> None:
        self.dimension = dimension

    def _generate_vector(self, text: str) -> list[float]:
        clean = text.strip().lower()
        seed = hashlib.sha512(clean.encode("utf-8")).digest()
        raw_values: list[float] = []
        for i in range(self.dimension):
            h = hashlib.sha256(seed + i.to_bytes(4, "big")).digest()
            val = int.from_bytes(h[:4], "big", signed=True) / (2**31 - 1)
            raw_values.append(val)
        norm = math.sqrt(sum(x * x for x in raw_values)) or 1.0
        return [x / norm for x in raw_values]

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

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_request_id_generated(async_client: AsyncClient) -> None:
    """Verify X-Request-ID header is generated if not provided."""
    response = await async_client.get("/health")
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 10


@pytest.mark.asyncio
async def test_request_id_propagated(async_client: AsyncClient) -> None:
    """Verify incoming X-Request-ID header is preserved and echoed back."""
    custom_id = "custom-test-request-id-999"
    response = await async_client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.headers.get("X-Request-ID") == custom_id

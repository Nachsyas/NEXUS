from redis.asyncio import Redis, from_url

from app.core.config import settings
from app.core.logging import logger

redis_client: Redis | None = None


async def get_redis() -> Redis:
    """Get or initialize the global async Redis client."""
    global redis_client
    if redis_client is None:
        redis_client = from_url(
            settings.REDIS_URL,
            decode_responses=True,
            health_check_interval=30,
        )
    return redis_client


async def close_redis() -> None:
    """Close the global Redis client connection."""
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None


async def check_redis_health() -> bool:
    """Perform a lightweight Redis ping."""
    try:
        client = await get_redis()
        return bool(await client.ping())
    except Exception as exc:
        logger.warning("Redis health check failed", extra={"error": str(exc)})
        return False

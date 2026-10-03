from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.core.config import settings
from app.core.database import check_database_health
from app.core.redis import check_redis_health

router = APIRouter(tags=["Health"])


class ComponentStatus(BaseModel):
    database: Literal["connected", "disconnected", "unreachable"]
    redis: Literal["connected", "disconnected", "unreachable"]


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    service: str
    environment: str
    timestamp: str
    components: ComponentStatus


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Technical Health Check",
    description="Returns current service status and component connectivity without sensitive data.",
)
async def health_check() -> HealthResponse:
    db_ok = await check_database_health()
    redis_ok = await check_redis_health()

    components = ComponentStatus(
        database="connected" if db_ok else "unreachable",
        redis="connected" if redis_ok else "unreachable",
    )

    # In M0 foundation, overall status is healthy if service responds, degraded if dependencies are offline
    overall_status: Literal["healthy", "degraded", "unhealthy"] = (
        "healthy" if db_ok and redis_ok else "degraded"
    )

    return HealthResponse(
        status=overall_status,
        service=settings.PROJECT_NAME,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(UTC).isoformat(),
        components=components,
    )

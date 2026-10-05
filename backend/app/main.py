from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.health import router as health_router
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.logging import logger, setup_logging
from app.core.middleware import RequestIDMiddleware
from app.core.redis import close_redis
from app.domains.auth.security import AuthenticationError
from app.domains.memories.exceptions import MemoryError
from app.domains.projects.exceptions import ProjectError


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, Any]:
    """Application lifespan manager for startup and shutdown routines."""
    setup_logging(settings.LOG_LEVEL)
    logger.info("Initializing NEXUS Backend...", extra={"environment": settings.ENVIRONMENT})
    yield
    logger.info("Shutting down NEXUS Backend...")
    await close_redis()
    await engine.dispose()


def create_application() -> FastAPI:
    """Application factory for NEXUS FastAPI backend."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
        docs_url=f"{settings.API_V1_STR}/docs" if settings.DEBUG else None,
        redoc_url=f"{settings.API_V1_STR}/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Cross-Origin Resource Sharing
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request ID and tracing middleware
    app.add_middleware(RequestIDMiddleware)

    # Authentication & Authorization Exception Handler
    @app.exception_handler(AuthenticationError)
    async def auth_exception_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": None,
                },
            },
            headers={"X-Request-ID": request_id},
        )

    # Projects Domain Exception Handler
    @app.exception_handler(ProjectError)
    async def project_exception_handler(request: Request, exc: ProjectError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": None,
                },
            },
            headers={"X-Request-ID": request_id},
        )

    # Memories Domain Exception Handler
    @app.exception_handler(MemoryError)
    async def memory_exception_handler(request: Request, exc: MemoryError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": None,
                },
            },
            headers={"X-Request-ID": request_id},
        )

    # Pydantic Request Validation Error Handler
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request payload validation failed.",
                    "details": jsonable_encoder(exc.errors()),
                },
            },
            headers={"X-Request-ID": request_id},
        )

    # Global Exception Handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(
            f"Unhandled exception occurred: {exc}",
            extra={"request_id": request_id},
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected internal server error occurred.",
                    "details": None,
                },
            },
            headers={"X-Request-ID": request_id},
        )

    # Direct /health for orchestrators/containers
    app.include_router(health_router, prefix="", tags=["Health"])

    # API v1 prefix
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()

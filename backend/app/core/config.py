from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "NEXUS Core"
    ENVIRONMENT: Literal["development", "staging", "production", "test"] = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    API_V1_STR: str = "/api/v1"

    # Database Configuration (PostgreSQL 16 + pgvector)
    # Default host port 5433 avoids collision with local host PostgreSQL
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://nexus:nexus@localhost:5433/nexus_dev",
        description="Async PostgreSQL connection string for application runtime",
    )
    DATABASE_URL_SYNC: str = Field(
        default="postgresql+psycopg://nexus:nexus@localhost:5433/nexus_dev",
        description="Sync PostgreSQL connection string for Alembic migrations",
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: float = 30.0

    # Ephemeral / Presence Configuration (Redis 7)
    # Default host port 6380 avoids collision with local host Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6380/0",
        description="Redis connection string for caching, rate limiting, and presence",
    )


settings = Settings()

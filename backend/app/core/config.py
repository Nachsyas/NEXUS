from typing import Literal

from pydantic import Field, model_validator
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

    # Auth & Session Security Configuration (ADR-020 / TBD-028, TBD-029)
    # Canonical configuration owner for token formats and lifetimes
    JWT_SECRET_KEY: str = Field(
        default="nexus-dev-insecure-jwt-secret-key-change-in-production-min32chars",
        description="HMAC-SHA256 signing secret for session access tokens",
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="Algorithm for signing access tokens",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        description="Short-lived access token lifetime in minutes (canonical config)",
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=30,
        description="Long-lived rotating refresh token lifetime in days (canonical config)",
    )

    # Apple Sign-In Provider Configuration
    APPLE_CLIENT_ID: str = Field(
        default="com.nexus.client",
        description="Apple Services / Bundle ID (aud claim in Apple identity token)",
    )
    APPLE_TEAM_ID: str = Field(
        default="",
        description="Apple Developer Team ID",
    )
    APPLE_KEY_ID: str = Field(
        default="",
        description="Apple Sign-In Key ID",
    )

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        """Enforce strict production security invariants for cryptographic secrets."""
        if self.ENVIRONMENT == "production":
            if (
                "change-in-production" in self.JWT_SECRET_KEY
                or "nexus-dev-insecure" in self.JWT_SECRET_KEY
            ):
                raise ValueError(
                    "JWT_SECRET_KEY must not use development placeholder in production environment."
                )
            if len(self.JWT_SECRET_KEY) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY must have at least 32 characters (256-bit entropy baseline) in production."
                )
        return self


settings = Settings()

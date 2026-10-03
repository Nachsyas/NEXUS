from app.core.config import settings
from app.main import app


def test_app_instantiation() -> None:
    """Verify FastAPI application instance initializes properly."""
    assert app is not None
    assert app.title == settings.PROJECT_NAME


def test_settings_load() -> None:
    """Verify configuration settings load with expected defaults."""
    assert settings.PROJECT_NAME == "NEXUS Core"
    assert settings.API_V1_STR == "/api/v1"
    assert "postgresql" in settings.DATABASE_URL
    assert "redis" in settings.REDIS_URL

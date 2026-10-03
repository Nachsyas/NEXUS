import json
import logging

from app.core.logging import StructuredJSONFormatter, sanitize_data


def test_sanitize_sensitive_data() -> None:
    """Verify passwords, tokens, and secrets are masked."""
    raw = {
        "user_id": "123",
        "password": "super-secret-password",
        "api_key": "live_key_xyz",
        "nested": {
            "access_token": "bearer-token-val",
            "safe_field": "visible",
        },
    }
    sanitized = sanitize_data(raw)
    assert sanitized["user_id"] == "123"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["api_key"] == "[REDACTED]"
    assert sanitized["nested"]["access_token"] == "[REDACTED]"
    assert sanitized["nested"]["safe_field"] == "visible"


def test_structured_json_formatter() -> None:
    """Verify log record is formatted as valid JSON with required fields."""
    formatter = StructuredJSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.request_id = "test-req-123"
    formatted = formatter.format(record)
    parsed = json.loads(formatted)
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "Test message"
    assert parsed["request_id"] == "test-req-123"
    assert "timestamp" in parsed

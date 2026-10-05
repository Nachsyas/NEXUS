import logging
import re
from typing import Any

from app.domains.memories.exceptions import MemorySecretRejectedError

logger = logging.getLogger(__name__)

# High-confidence secret detection patterns (NEVER_STORE policy)
_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN\s+(?:[A-Z0-9_-]+\s+)?PRIVATE\s+KEY-----", re.IGNORECASE),
    re.compile(r"\beyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]+\b"),
    re.compile(r"\bBearer\s+[a-zA-Z0-9_\-\.]{20,}\b", re.IGNORECASE),
    re.compile(r"\bsk-[a-zA-Z0-9_\-]{20,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr|github_pat)_[a-zA-Z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"""(?i)\b(?:[a-z0-9_-]*_)?(?:api[_-]?key|secret[_-]?key|client[_-]?secret|auth[_-]?token|access[_-]?token|refresh[_-]?token)(?:\s+is)?\s*[:=]\s*['"]?[a-zA-Z0-9_\-\.]{16,}['"]?"""
    ),
    re.compile(
        r"""(?i)\b(?:[a-z0-9_-]*_)?(?:password|passwd|pwd)(?:\s+is)?\s*[:=]\s*['"]?[^\s'"]{6,}['"]?"""
    ),
    re.compile(
        r"""(?i)\b(?:otp(?:\s+code)?|one-time\s+password|verification\s+code)(?:\s+is)?\s*[:=]?\s*['"]?\d{4,8}['"]?"""
    ),
    re.compile(
        r"""(?i)\b(?:seed\s+phrase|recovery\s+phrase)\s*[:=]\s*['"]?[a-z]+(?:\s+[a-z]+){11,}['"]?"""
    ),
]

_SENSITIVE_KEY_PATTERN = re.compile(
    r"(?i)(?:password|passwd|pwd|secret_key|api_key|client_secret|auth_token|access_token|refresh_token)"
)


class MemorySafetyPolicy:
    """Enforces NEXUS NEVER_STORE policy by rejecting high-confidence credential/secret persistence."""

    @classmethod
    def scan_text(cls, text: str) -> bool:
        """Return True if text contains any forbidden secret pattern."""
        if not text:
            return False
        return any(pattern.search(text) for pattern in _SECRET_PATTERNS)

    @classmethod
    def scan_data(cls, data: Any) -> bool:
        """Recursively scan structured data for forbidden secrets."""
        if data is None:
            return False
        if isinstance(data, str):
            return cls.scan_text(data)
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(k, str):
                    if cls.scan_text(k) or cls.scan_text(f"{k}: {v}"):
                        return True
                    if _SENSITIVE_KEY_PATTERN.search(k) and v:
                        return True
                if cls.scan_data(v):
                    return True
            return False
        if isinstance(data, (list, tuple, set)):
            return any(cls.scan_data(item) for item in data)
        return False

    @classmethod
    def validate(
        cls,
        subject: str,
        predicate: str,
        value_text: str,
        value_json: dict[str, Any] | None = None,
    ) -> None:
        """Validate candidate memory fields.

        Raises MemorySecretRejectedError if any secret pattern is detected.
        Never logs or leaks the candidate secret value.
        """
        if (
            cls.scan_text(subject)
            or cls.scan_text(predicate)
            or cls.scan_text(value_text)
            or cls.scan_data(value_json)
        ):
            # Safe structured log event with zero secret content
            logger.warning("memory_rejected_by_safety_policy reason=secret_pattern_detected")
            raise MemorySecretRejectedError(
                "Memory content rejected by NEVER_STORE secret safety policy."
            )

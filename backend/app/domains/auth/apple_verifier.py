import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import httpx
import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from app.core.config import settings
from app.core.logging import logger
from app.domains.auth.security import InvalidCredentialsError


@dataclass(frozen=True)
class VerifiedExternalIdentity:
    """Verified identity claims extracted from an external identity provider."""

    provider: str
    provider_subject: str
    email: str | None = None
    full_name: str | None = None


class AppleIdentityVerifier(ABC):
    """Abstract provider boundary for verifying Apple identity credentials."""

    @abstractmethod
    async def verify_identity_token(
        self,
        identity_token: str,
        authorization_code: str | None = None,
    ) -> VerifiedExternalIdentity:
        """Verify an Apple identity token and return trusted identity claims."""
        pass


class ProductionAppleVerifier(AppleIdentityVerifier):
    """Production verifier that validates Apple identity tokens against Apple JWKS."""

    APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"
    APPLE_ISSUER = "https://appleid.apple.com"

    def __init__(self) -> None:
        self._cached_keys: list[dict[str, Any]] = []
        self._cache_expires_at: datetime.datetime | None = None

    async def _fetch_apple_public_keys(self) -> list[dict[str, Any]]:
        now = datetime.datetime.now(datetime.UTC)
        if self._cached_keys and self._cache_expires_at and now < self._cache_expires_at:
            return self._cached_keys

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.APPLE_JWKS_URL)
            if response.status_code != 200:
                logger.error(
                    "Failed to fetch Apple JWKS",
                    extra={"status_code": response.status_code},
                )
                raise InvalidCredentialsError(
                    "Unable to verify Apple identity with identity authority."
                )

            data = response.json()
            keys: list[dict[str, Any]] = data.get("keys", [])
            self._cached_keys = keys
            self._cache_expires_at = now + datetime.timedelta(hours=24)
            return keys

    async def verify_identity_token(
        self,
        identity_token: str,
        _authorization_code: str | None = None,
    ) -> VerifiedExternalIdentity:
        try:
            # 1. Inspect unverified header for key ID (kid)
            unverified_header = jwt.get_unverified_header(identity_token)
            kid = unverified_header.get("kid")
            if not kid:
                raise InvalidCredentialsError("Apple identity token header missing 'kid'.")

            # 2. Match with Apple JWKS public keys
            keys = await self._fetch_apple_public_keys()
            matching_key = next((k for k in keys if k.get("kid") == kid), None)
            if not matching_key:
                raise InvalidCredentialsError("Unknown Apple signing key identifier.")

            # 3. Construct RSA public key from JWKS
            raw_key = jwt.algorithms.RSAAlgorithm.from_jwk(matching_key)
            if not isinstance(raw_key, RSAPublicKey):
                raise InvalidCredentialsError("Apple signing key is not a valid RSA public key.")
            public_key = raw_key

            # 4. Cryptographically verify signature and standard claims
            payload = jwt.decode(
                identity_token,
                public_key,
                algorithms=["RS256"],
                audience=settings.APPLE_CLIENT_ID,
                issuer=self.APPLE_ISSUER,
            )

            subject = payload.get("sub")
            if not subject:
                raise InvalidCredentialsError("Apple identity token missing subject claim.")

            email = payload.get("email")
            return VerifiedExternalIdentity(
                provider="APPLE",
                provider_subject=subject,
                email=str(email) if email else None,
            )

        except jwt.ExpiredSignatureError as exc:
            raise InvalidCredentialsError("Apple identity token has expired.") from exc
        except jwt.InvalidTokenError as exc:
            raise InvalidCredentialsError(
                f"Apple identity token verification failed: {exc}"
            ) from exc
        except Exception as exc:
            if isinstance(exc, InvalidCredentialsError):
                raise
            logger.error("Unexpected error verifying Apple token", exc_info=True)
            raise InvalidCredentialsError("Failed to verify Apple identity credentials.") from exc


class MockAppleVerifier(AppleIdentityVerifier):
    """Test and development verifier for deterministic, offline testing."""

    def __init__(
        self,
        default_subject: str = "apple-sub-test-001",
        default_email: str | None = "user@test.apple.com",
    ) -> None:
        self.default_subject = default_subject
        self.default_email = default_email
        self.should_fail = False
        self.failure_reason = "Simulated Apple token verification failure."

    async def verify_identity_token(
        self,
        identity_token: str,
        _authorization_code: str | None = None,
    ) -> VerifiedExternalIdentity:
        if self.should_fail or identity_token == "invalid-apple-token":
            raise InvalidCredentialsError(self.failure_reason)

        # Allow format "mock-apple:<subject>:<email>" for flexible test cases
        if identity_token.startswith("mock-apple:"):
            parts = identity_token.split(":")
            sub = parts[1] if len(parts) > 1 and parts[1] else self.default_subject
            email = parts[2] if len(parts) > 2 and parts[2] else self.default_email
            return VerifiedExternalIdentity(
                provider="APPLE",
                provider_subject=sub,
                email=email,
            )

        return VerifiedExternalIdentity(
            provider="APPLE",
            provider_subject=self.default_subject,
            email=self.default_email,
        )


_active_verifier: AppleIdentityVerifier | None = None


def get_apple_verifier() -> AppleIdentityVerifier:
    """Return the active AppleIdentityVerifier instance."""
    global _active_verifier
    if _active_verifier is None:
        if settings.ENVIRONMENT in ("test", "development"):
            _active_verifier = MockAppleVerifier()
        else:
            _active_verifier = ProductionAppleVerifier()
    return _active_verifier


def set_apple_verifier(verifier: AppleIdentityVerifier) -> None:
    """Override the active verifier (primarily for unit/integration testing)."""
    global _active_verifier
    _active_verifier = verifier

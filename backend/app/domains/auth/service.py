import datetime
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.logging import logger
from app.domains.auth.apple_verifier import AppleIdentityVerifier, get_apple_verifier
from app.domains.auth.models import AuthIdentity, RotatedTokenHash, Session
from app.domains.auth.schemas import (
    AppleLoginRequest,
    RefreshTokenResponse,
    SessionResponse,
    TokenResponse,
)
from app.domains.auth.security import (
    ForbiddenAccessError,
    InvalidCredentialsError,
    RefreshTokenReusedError,
    TokenExpiredError,
    create_access_token,
    generate_opaque_token,
    hash_token,
)
from app.domains.users.models import User, UserPreference, generate_uuid7
from app.domains.users.schemas import UserResponse


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


class AuthService:
    """Service orchestrating authentication, token lifecycle, and session security."""

    @staticmethod
    async def login_with_apple(
        db: AsyncSession,
        request: AppleLoginRequest,
        client_metadata: dict[str, Any] | None = None,
        verifier: AppleIdentityVerifier | None = None,
    ) -> TokenResponse:
        if verifier is None:
            verifier = get_apple_verifier()

        # 1. Cryptographically verify identity token at provider boundary
        verified_identity = await verifier.verify_identity_token(
            request.identity_token,
            request.authorization_code,
        )

        # 2. Look up existing AuthIdentity
        stmt = (
            select(AuthIdentity)
            .options(selectinload(AuthIdentity.user))
            .where(
                AuthIdentity.provider == "APPLE",
                AuthIdentity.provider_subject == verified_identity.provider_subject,
            )
        )
        result = await db.execute(stmt)
        auth_identity = result.scalar_one_or_none()

        now = utc_now()

        if auth_identity:
            # Returning user
            user = auth_identity.user
            auth_identity.last_verified_at = now
            if verified_identity.email and not auth_identity.email:
                auth_identity.email = verified_identity.email
            if request.user_info and request.user_info.name and not user.display_name:
                user.display_name = request.user_info.name
            user.last_login_at = now
            user.updated_at = now
        else:
            # First-time user creation
            display_name = None
            if request.user_info and request.user_info.name:
                display_name = request.user_info.name
            elif verified_identity.full_name:
                display_name = verified_identity.full_name

            user = User(
                display_name=display_name,
                status="ACTIVE",
                created_at=now,
                updated_at=now,
                last_login_at=now,
            )
            db.add(user)
            await db.flush()

            email = verified_identity.email or (
                request.user_info.email if request.user_info else None
            )
            auth_identity = AuthIdentity(
                user_id=user.id,
                provider="APPLE",
                provider_subject=verified_identity.provider_subject,
                email=email,
                created_at=now,
                updated_at=now,
                last_verified_at=now,
            )
            db.add(auth_identity)

            user_preference = UserPreference(
                user_id=user.id,
                language="en",
                response_detail="CONCISE",
                interaction_style="DIRECT",
                proactivity_level="MEDIUM",
                notification_preferences={},
                voice_settings={},
                created_at=now,
                updated_at=now,
            )
            db.add(user_preference)

        # 3. Create active session
        raw_refresh_token = generate_opaque_token()
        refresh_hash = hash_token(raw_refresh_token)
        family_id = generate_uuid7()
        expires_at = now + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        session = Session(
            user_id=user.id,
            refresh_token_hash=refresh_hash,
            token_family_id=family_id,
            rotation_counter=0,
            created_at=now,
            last_used_at=now,
            expires_at=expires_at,
            client_metadata=client_metadata,
        )
        db.add(session)
        await db.flush()

        # 4. Generate access token
        access_token = create_access_token(user_id=user.id, session_id=session.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )

    @staticmethod
    async def refresh_session(
        db: AsyncSession,
        refresh_token: str,
    ) -> RefreshTokenResponse:
        incoming_hash = hash_token(refresh_token)
        now = utc_now()

        # Query session by current refresh_token_hash
        stmt = select(Session).where(Session.refresh_token_hash == incoming_hash)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()

        if session is None:
            # Check if this token was previously rotated (reuse detection)
            rotated_stmt = select(RotatedTokenHash).where(
                RotatedTokenHash.token_hash == incoming_hash
            )
            rotated_result = await db.execute(rotated_stmt)
            rotated = rotated_result.scalar_one_or_none()

            if rotated is not None:
                # REUSE DETECTED: Immediately revoke all sessions in token family
                family_stmt = select(Session).where(
                    Session.token_family_id == rotated.token_family_id
                )
                family_sessions = (await db.execute(family_stmt)).scalars().all()
                for s in family_sessions:
                    s.revoked_at = now
                    s.revocation_reason = "REUSE_DETECTED"
                # Persist the security revocation immediately before raising exception
                await db.commit()

                logger.warning(
                    "Refresh token reuse detected. Revoked token family.",
                    extra={"token_family_id": str(rotated.token_family_id)},
                )
                raise RefreshTokenReusedError(
                    "Refresh token reuse detected. All family sessions terminated."
                )

            raise InvalidCredentialsError("Invalid or unknown refresh token.")

        # Check revocation
        if session.revoked_at is not None:
            if session.revocation_reason == "REUSE_DETECTED":
                raise RefreshTokenReusedError(
                    "Session terminated due to prior token reuse detection."
                )
            raise InvalidCredentialsError("Session has been revoked.")

        # Check expiration
        if session.expires_at < now:
            raise TokenExpiredError("Refresh token has expired.")

        # Atomic Rotation
        # 1. Archive current token hash to rotated_token_hashes
        rotated_record = RotatedTokenHash(
            token_hash=session.refresh_token_hash,
            session_id=session.id,
            token_family_id=session.token_family_id,
            rotated_at=now,
        )
        db.add(rotated_record)

        # 2. Generate new refresh token
        new_refresh_token = generate_opaque_token()
        session.refresh_token_hash = hash_token(new_refresh_token)
        session.rotation_counter += 1
        session.last_used_at = now
        await db.flush()

        # 3. Issue new access token
        new_access_token = create_access_token(user_id=session.user_id, session_id=session.id)

        return RefreshTokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )

    @staticmethod
    async def logout(
        db: AsyncSession,
        user_id: uuid.UUID,
        session_id: uuid.UUID | None = None,
        refresh_token: str | None = None,
    ) -> None:
        now = utc_now()
        if session_id is not None:
            session = await db.get(Session, session_id)
            if session and session.user_id == user_id:
                session.revoked_at = now
                session.revocation_reason = "LOGOUT"
                await db.flush()
                return

        if refresh_token:
            token_hash = hash_token(refresh_token)
            stmt = select(Session).where(
                Session.refresh_token_hash == token_hash,
                Session.user_id == user_id,
            )
            session = (await db.execute(stmt)).scalar_one_or_none()
            if session:
                session.revoked_at = now
                session.revocation_reason = "LOGOUT"
                await db.flush()

    @staticmethod
    async def list_user_sessions(
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[SessionResponse]:
        now = utc_now()
        stmt = (
            select(Session)
            .where(
                Session.user_id == user_id,
                Session.revoked_at.is_(None),
                Session.expires_at > now,
            )
            .order_by(Session.last_used_at.desc())
        )
        sessions = (await db.execute(stmt)).scalars().all()

        results: list[SessionResponse] = []
        for s in sessions:
            metadata = s.client_metadata or {}
            results.append(
                SessionResponse(
                    id=s.id,
                    device_name=metadata.get("device_name"),
                    ip_address=metadata.get("ip_address"),
                    created_at=s.created_at,
                    last_active_at=s.last_used_at,
                )
            )
        return results

    @staticmethod
    async def revoke_user_session(
        db: AsyncSession,
        user_id: uuid.UUID,
        session_id: uuid.UUID,
    ) -> None:
        session = await db.get(Session, session_id)
        if not session:
            raise ForbiddenAccessError("Session not found.")
        if session.user_id != user_id:
            raise ForbiddenAccessError("You are not authorized to revoke another user's session.")

        session.revoked_at = utc_now()
        session.revocation_reason = "MANUAL_TERMINATION"
        await db.flush()

import datetime
import uuid

import jwt
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.config import Settings
from app.core.database import async_session_factory
from app.domains.auth.apple_verifier import MockAppleVerifier, set_apple_verifier
from app.domains.auth.models import Session
from app.domains.auth.security import create_access_token, hash_token
from app.domains.users.models import User, UserPreference


@pytest.fixture(autouse=True)
def setup_mock_verifier() -> None:
    """Ensure mock Apple verifier is active for all tests."""
    mock_verifier = MockAppleVerifier(
        default_subject="apple-sub-test-default",
        default_email="default@nexus.test",
    )
    set_apple_verifier(mock_verifier)


@pytest.mark.asyncio
async def test_first_apple_login_creates_user_and_preferences(async_client: AsyncClient) -> None:
    unique_sub = f"apple-sub-{uuid.uuid4()}"
    unique_email = f"user-{uuid.uuid4()}@nexus.test"

    response = await async_client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": f"mock-apple:{unique_sub}:{unique_email}",
            "user_info": {
                "name": "Nexus Explorer",
                "email": unique_email,
            },
        },
    )

    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    data = res_data["data"]
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["display_name"] == "Nexus Explorer"

    user_id = uuid.UUID(data["user"]["id"])

    # Verify database persistence & plaintext token absence
    async with async_session_factory() as db:
        user = await db.get(User, user_id)
        assert user is not None
        assert user.display_name == "Nexus Explorer"

        # Verify user preferences were created with defaults
        pref_stmt = select(UserPreference).where(UserPreference.user_id == user_id)
        pref = (await db.execute(pref_stmt)).scalar_one_or_none()
        assert pref is not None
        assert pref.language == "en"
        assert pref.response_detail == "CONCISE"

        # Verify session refresh_token_hash is stored, but NOT raw refresh token
        raw_refresh = data["refresh_token"]
        session_stmt = select(Session).where(Session.user_id == user_id)
        session = (await db.execute(session_stmt)).scalar_one_or_none()
        assert session is not None
        assert session.refresh_token_hash == hash_token(raw_refresh)
        assert session.refresh_token_hash != raw_refresh


@pytest.mark.asyncio
async def test_repeat_apple_login_resolves_same_user(async_client: AsyncClient) -> None:
    unique_sub = f"apple-sub-{uuid.uuid4()}"

    # First login
    resp1 = await async_client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": f"mock-apple:{unique_sub}:user1@nexus.test",
            "user_info": {"name": "Initial Name"},
        },
    )
    assert resp1.status_code == 200
    user_id_1 = resp1.json()["data"]["user"]["id"]

    # Repeat login with same Apple subject
    resp2 = await async_client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": f"mock-apple:{unique_sub}:user1@nexus.test",
        },
    )
    assert resp2.status_code == 200
    user_id_2 = resp2.json()["data"]["user"]["id"]

    # Must resolve to the exact same canonical user ID
    assert user_id_1 == user_id_2


@pytest.mark.asyncio
async def test_unverified_apple_token_rejected(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": "invalid-apple-token",
        },
    )
    assert response.status_code == 401
    res_data = response.json()
    assert res_data["success"] is False
    assert res_data["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_authenticated_profile_access(async_client: AsyncClient) -> None:
    # 1. Login
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:profile@test.com"},
    )
    access_token = login_resp.json()["data"]["access_token"]
    user_id = login_resp.json()["data"]["user"]["id"]

    # 2. Access /me without auth -> 401
    anon_resp = await async_client.get("/api/v1/me")
    assert anon_resp.status_code == 401

    # 3. Access /me with auth -> 200
    auth_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert auth_resp.status_code == 200
    assert auth_resp.json()["data"]["id"] == user_id


@pytest.mark.asyncio
async def test_profile_update(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:update@test.com"},
    )
    access_token = login_resp.json()["data"]["access_token"]

    update_resp = await async_client.patch(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"display_name": "Updated Agent Master"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["display_name"] == "Updated Agent Master"

    # Verify on subsequent GET /me
    get_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert get_resp.json()["data"]["display_name"] == "Updated Agent Master"


@pytest.mark.asyncio
async def test_user_preferences_flow(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:pref@test.com"},
    )
    access_token = login_resp.json()["data"]["access_token"]

    # GET preferences
    pref_resp = await async_client.get(
        "/api/v1/me/preferences",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert pref_resp.status_code == 200
    assert pref_resp.json()["data"]["response_detail"] == "CONCISE"

    # PATCH preferences
    patch_resp = await async_client.patch(
        "/api/v1/me/preferences",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "response_detail": "TECHNICAL",
            "interaction_style": "EXPLORATORY",
            "proactivity_level": "HIGH",
        },
    )
    assert patch_resp.status_code == 200
    pref_data = patch_resp.json()["data"]["preferences"]
    assert pref_data["response_detail"] == "TECHNICAL"
    assert pref_data["interaction_style"] == "EXPLORATORY"
    assert pref_data["proactivity_level"] == "HIGH"


@pytest.mark.asyncio
async def test_refresh_token_rotation_success(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:rotation@test.com"},
    )
    first_refresh = login_resp.json()["data"]["refresh_token"]

    # Rotate refresh token
    rotate_resp = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": first_refresh},
    )
    assert rotate_resp.status_code == 200
    new_data = rotate_resp.json()["data"]
    second_refresh = new_data["refresh_token"]
    second_access = new_data["access_token"]

    assert second_refresh != first_refresh
    assert "access_token" in new_data

    # Verify new access token works
    me_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {second_access}"},
    )
    assert me_resp.status_code == 200


@pytest.mark.asyncio
async def test_refresh_token_reuse_detection_revokes_family(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:reuse@test.com"},
    )
    initial_refresh = login_resp.json()["data"]["refresh_token"]

    # Legitimate first rotation
    rot_resp = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": initial_refresh},
    )
    assert rot_resp.status_code == 200
    new_access_token = rot_resp.json()["data"]["access_token"]

    # Attacker tries to replay initial_refresh (already rotated!)
    replay_resp = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": initial_refresh},
    )
    assert replay_resp.status_code == 401
    assert replay_resp.json()["error"]["code"] == "AUTH_REFRESH_TOKEN_REUSED"

    # Family is now revoked: even the new access token and new session must be dead
    me_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {new_access_token}"},
    )
    assert me_resp.status_code == 401


@pytest.mark.asyncio
async def test_session_listing_and_manual_revocation(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:sessions@test.com"},
    )
    access_token = login_resp.json()["data"]["access_token"]

    # List active sessions
    list_resp = await async_client.get(
        "/api/v1/auth/sessions",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert list_resp.status_code == 200
    sessions = list_resp.json()["data"]
    assert len(sessions) >= 1
    session_id = sessions[0]["id"]

    # Revoke that session
    del_resp = await async_client.delete(
        f"/api/v1/auth/sessions/{session_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert del_resp.status_code == 200
    assert del_resp.json()["data"]["message"] == "Session terminated"

    # Subsequent access using that session token is now rejected
    rejected_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert rejected_resp.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_current_session(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:logout@test.com"},
    )
    access_token = login_resp.json()["data"]["access_token"]

    logout_resp = await async_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert logout_resp.status_code == 200
    assert logout_resp.json()["data"]["message"] == "Session revoked"

    # Verify session is dead
    me_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_resp.status_code == 401


@pytest.mark.asyncio
async def test_revoked_session_cannot_refresh(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:rev-refresh@test.com"},
    )
    access_token = login_resp.json()["data"]["access_token"]
    refresh_token = login_resp.json()["data"]["refresh_token"]

    # Logout to revoke session
    await async_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Attempting to refresh a revoked session must fail
    refresh_resp = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_resp.status_code == 401
    assert refresh_resp.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_cross_user_isolation_multi_tenancy(async_client: AsyncClient) -> None:
    """Security Invariant: User A cannot read, modify, or terminate User B's resources."""
    # User A setup
    resp_a = await async_client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": f"mock-apple:sub-user-a-{uuid.uuid4()}:a@test.com",
            "user_info": {"name": "User Alpha"},
        },
    )
    token_a = resp_a.json()["data"]["access_token"]
    user_a_id = resp_a.json()["data"]["user"]["id"]

    # User B setup
    resp_b = await async_client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": f"mock-apple:sub-user-b-{uuid.uuid4()}:b@test.com",
            "user_info": {"name": "User Beta"},
        },
    )
    token_b = resp_b.json()["data"]["access_token"]
    user_b_id = resp_b.json()["data"]["user"]["id"]

    user_b_sessions = (
        await async_client.get(
            "/api/v1/auth/sessions",
            headers={"Authorization": f"Bearer {token_b}"},
        )
    ).json()["data"]
    session_b_id = user_b_sessions[0]["id"]

    # 1. User A cannot read User B profile (User A's /me returns User A)
    me_a = (
        await async_client.get("/api/v1/me", headers={"Authorization": f"Bearer {token_a}"})
    ).json()["data"]
    assert me_a["id"] == user_a_id
    assert me_a["id"] != user_b_id
    assert me_a["display_name"] == "User Alpha"

    # 2. User A cannot modify User B profile
    await async_client.patch(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {token_a}"},
        json={"display_name": "Alpha Modified"},
    )
    me_b = (
        await async_client.get("/api/v1/me", headers={"Authorization": f"Bearer {token_b}"})
    ).json()["data"]
    assert me_b["id"] == user_b_id
    assert me_b["display_name"] == "User Beta"  # Untouched

    # 3. User A cannot read User B preferences
    pref_a = (
        await async_client.get(
            "/api/v1/me/preferences", headers={"Authorization": f"Bearer {token_a}"}
        )
    ).json()["data"]
    assert pref_a["response_detail"] == "CONCISE"

    # 4. User A cannot modify User B preferences
    await async_client.patch(
        "/api/v1/me/preferences",
        headers={"Authorization": f"Bearer {token_a}"},
        json={"response_detail": "TECHNICAL"},
    )
    pref_a_updated = (
        await async_client.get(
            "/api/v1/me/preferences", headers={"Authorization": f"Bearer {token_a}"}
        )
    ).json()["data"]
    assert pref_a_updated["response_detail"] == "TECHNICAL"

    # User B's preferences remain untouched
    pref_b = (
        await async_client.get(
            "/api/v1/me/preferences", headers={"Authorization": f"Bearer {token_b}"}
        )
    ).json()["data"]
    assert pref_b["response_detail"] == "CONCISE"  # Untouched

    # 5. User A cannot list User B sessions
    sessions_a = (
        await async_client.get(
            "/api/v1/auth/sessions", headers={"Authorization": f"Bearer {token_a}"}
        )
    ).json()["data"]
    session_a_ids = [s["id"] for s in sessions_a]
    assert session_b_id not in session_a_ids

    # 6. User A cannot revoke User B's session -> must be rejected with 403 FORBIDDEN_ACCESS!
    attack_resp = await async_client.delete(
        f"/api/v1/auth/sessions/{session_b_id}",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert attack_resp.status_code == 403
    assert attack_resp.json()["error"]["code"] == "FORBIDDEN_ACCESS"

    # Verify User B's session remains active and untouched
    verify_b = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert verify_b.status_code == 200


@pytest.mark.asyncio
async def test_access_token_algorithm_safety_and_rejections(async_client: AsyncClient) -> None:
    """Verify algorithm confusion, invalid signature, expiration, and malformed token rejections."""
    # 1. Login to get valid context IDs
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:algtest@test.com"},
    )
    user_id = uuid.UUID(login_resp.json()["data"]["user"]["id"])
    session_id = uuid.UUID(
        (
            await async_client.get(
                "/api/v1/auth/sessions",
                headers={"Authorization": f"Bearer {login_resp.json()['data']['access_token']}"},
            )
        ).json()["data"][0]["id"]
    )

    # 2. Algorithm confusion test: "none" algorithm token
    none_payload = {
        "sub": str(user_id),
        "session_id": str(session_id),
        "exp": int(
            (datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)).timestamp()
        ),
    }
    none_token = jwt.encode(none_payload, key="", algorithm="none")
    none_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {none_token}"},
    )
    assert none_resp.status_code == 401
    assert none_resp.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"

    # 3. Algorithm mismatch: token signed with wrong key
    wrong_key_token = jwt.encode(
        none_payload, key="wrong-key-secret-32-bytes-long-padding", algorithm="HS256"
    )
    wrong_key_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {wrong_key_token}"},
    )
    assert wrong_key_resp.status_code == 401
    assert wrong_key_resp.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"

    # 4. Expired access token
    expired_token = create_access_token(
        user_id=user_id,
        session_id=session_id,
        expires_delta=datetime.timedelta(seconds=-10),
    )
    expired_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert expired_resp.status_code == 401
    assert expired_resp.json()["error"]["code"] == "AUTH_TOKEN_EXPIRED"

    # 5. Malformed non-JWT string
    malformed_resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": "Bearer not.a.valid.jwt"},
    )
    assert malformed_resp.status_code == 401
    assert malformed_resp.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"


def test_settings_production_security_validation() -> None:
    """Verify Settings rejects placeholder or short secrets in production environment."""
    # Placeholder in production -> rejected
    with pytest.raises(ValueError, match="development placeholder"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET_KEY="nexus-dev-insecure-jwt-secret-key-change-in-production-min32chars",
        )

    # Secret < 32 chars in production -> rejected
    with pytest.raises(ValueError, match="at least 32 characters"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET_KEY="too-short-secret",
        )

    # Valid secret in production -> accepted
    valid_settings = Settings(
        ENVIRONMENT="production",
        JWT_SECRET_KEY="a-very-secure-randomly-generated-production-secret-value-32",
    )
    assert valid_settings.JWT_SECRET_KEY.startswith("a-very-secure")


@pytest.mark.asyncio
async def test_tampered_access_token_rejected(async_client: AsyncClient) -> None:
    login_resp = await async_client.post(
        "/api/v1/auth/apple",
        json={"identity_token": f"mock-apple:sub-{uuid.uuid4()}:tamper@test.com"},
    )
    access_token = login_resp.json()["data"]["access_token"]
    tampered_token = access_token[:-4] + "abcd"

    resp = await async_client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {tampered_token}"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"

import asyncio
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.core.database import async_session_factory
from app.domains.auth.apple_verifier import MockAppleVerifier, set_apple_verifier
from app.domains.projects.models import Project
from app.domains.users.models import UserPreference


@pytest.fixture(autouse=True)
def setup_mock_verifier() -> None:
    mock_verifier = MockAppleVerifier(
        default_subject="apple-sub-test-default",
        default_email="default@nexus.test",
    )
    set_apple_verifier(mock_verifier)


async def create_test_user(
    client: AsyncClient, name: str = "Test User"
) -> tuple[dict[str, str], str]:
    sub = f"apple-sub-{uuid.uuid4()}"
    email = f"user-{uuid.uuid4()}@nexus.test"
    res = await client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": f"mock-apple:{sub}:{email}",
            "user_info": {"name": name, "email": email},
        },
    )
    assert res.status_code == 200
    data = res.json()["data"]
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers, data["user"]["id"]


@pytest.mark.asyncio
async def test_anonymous_access_rejected(async_client: AsyncClient) -> None:
    fake_id = uuid.uuid4()
    assert (await async_client.get("/api/v1/projects")).status_code == 401
    assert (await async_client.post("/api/v1/projects", json={"name": "P"})).status_code == 401
    assert (await async_client.get(f"/api/v1/projects/{fake_id}")).status_code == 401
    assert (
        await async_client.patch(f"/api/v1/projects/{fake_id}", json={"name": "P"})
    ).status_code == 401
    assert (await async_client.post(f"/api/v1/projects/{fake_id}/activate")).status_code == 401
    assert (await async_client.post(f"/api/v1/projects/{fake_id}/archive")).status_code == 401
    assert (await async_client.get(f"/api/v1/projects/{fake_id}/context")).status_code == 401


@pytest.mark.asyncio
async def test_project_creation_and_ownership(async_client: AsyncClient) -> None:
    headers, user_id_str = await create_test_user(async_client, "Project Creator")

    payload = {
        "name": "NEXUS Mobile App",
        "description": "Next-gen AI assistant iOS app",
        "status": "PLANNING",
        "priority": "HIGH",
        "summary": "SwiftUI + FastAPI backend companion",
        "progress": 25,
        "technologies": ["Swift", "SwiftUI", "FastAPI"],
    }

    res = await async_client.post("/api/v1/projects", json=payload, headers=headers)
    assert res.status_code == 201
    body = res.json()
    assert body["success"] is True
    data = body["data"]

    # Verify UUIDv7 and canonical fields
    assert uuid.UUID(data["id"])
    assert data["name"] == "NEXUS Mobile App"
    assert data["slug"] == "nexus-mobile-app"
    assert data["description"] == payload["description"]
    assert data["status"] == "PLANNING"
    assert data["priority"] == "HIGH"
    assert data["progress"] == 25
    assert data["is_active"] is False
    assert len(data["technologies"]) == 3
    tech_names = [t["name"] for t in data["technologies"]]
    assert "Swift" in tech_names
    assert "SwiftUI" in tech_names
    assert "FastAPI" in tech_names


@pytest.mark.asyncio
async def test_slug_generation_and_deterministic_collision(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Slug Tester")

    # First project: slug should be clean base slug
    res1 = await async_client.post(
        "/api/v1/projects",
        json={"name": "Project Apollo & Artemis!"},
        headers=headers,
    )
    assert res1.status_code == 201
    assert res1.json()["data"]["slug"] == "project-apollo-artemis"

    # Second project with identical normalized name by same user: slug becomes -2
    res2 = await async_client.post(
        "/api/v1/projects",
        json={"name": "Project Apollo   Artemis"},
        headers=headers,
    )
    assert res2.status_code == 201
    assert res2.json()["data"]["slug"] == "project-apollo-artemis-2"

    # Third project by same user: slug becomes -3
    res3 = await async_client.post(
        "/api/v1/projects",
        json={"name": "project apollo artemis"},
        headers=headers,
    )
    assert res3.status_code == 201
    assert res3.json()["data"]["slug"] == "project-apollo-artemis-3"

    # Different user can use the base slug without conflict
    headers2, _ = await create_test_user(async_client, "Another Slug User")
    res_other = await async_client.post(
        "/api/v1/projects",
        json={"name": "Project Apollo Artemis"},
        headers=headers2,
    )
    assert res_other.status_code == 201
    assert res_other.json()["data"]["slug"] == "project-apollo-artemis"


@pytest.mark.asyncio
async def test_concurrent_same_name_slug_creation(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Concurrent Slug User")

    # Concurrently create 3 projects with identical name for the same user
    tasks = [
        async_client.post("/api/v1/projects", json={"name": "Concurrent Project"}, headers=headers)
        for _ in range(3)
    ]
    responses = await asyncio.gather(*tasks)

    # None of the responses should be a 500 error
    for r in responses:
        assert r.status_code == 201, f"Expected 201, got {r.status_code}: {r.text}"

    slugs = [r.json()["data"]["slug"] for r in responses]
    assert len(slugs) == 3
    assert len(set(slugs)) == 3, f"Slugs must be unique, got: {slugs}"
    expected_slug_set = {"concurrent-project", "concurrent-project-2", "concurrent-project-3"}
    assert set(slugs) == expected_slug_set


@pytest.mark.asyncio
async def test_cross_user_isolation_and_idor(async_client: AsyncClient) -> None:
    headers_a, _ = await create_test_user(async_client, "Tenant A")
    headers_b, _ = await create_test_user(async_client, "Tenant B")

    # Tenant A creates project
    res_a = await async_client.post(
        "/api/v1/projects",
        json={"name": "Tenant A Secret Project"},
        headers=headers_a,
    )
    proj_a_id = res_a.json()["data"]["id"]

    # Tenant B tries to get Tenant A's project -> 404 (prevent IDOR)
    res_get = await async_client.get(f"/api/v1/projects/{proj_a_id}", headers=headers_b)
    assert res_get.status_code == 404
    assert res_get.json()["error"]["code"] == "PROJECT_NOT_FOUND"

    # Tenant B tries to update Tenant A's project -> 404
    res_patch = await async_client.patch(
        f"/api/v1/projects/{proj_a_id}",
        json={"name": "Hacked Project"},
        headers=headers_b,
    )
    assert res_patch.status_code == 404

    # Tenant B tries to activate Tenant A's project -> 404
    res_act = await async_client.post(f"/api/v1/projects/{proj_a_id}/activate", headers=headers_b)
    assert res_act.status_code == 404

    # Tenant B tries to archive Tenant A's project -> 404
    res_arc = await async_client.post(f"/api/v1/projects/{proj_a_id}/archive", headers=headers_b)
    assert res_arc.status_code == 404

    # Tenant B tries to get Tenant A's project context -> 404
    res_ctx = await async_client.get(f"/api/v1/projects/{proj_a_id}/context", headers=headers_b)
    assert res_ctx.status_code == 404


@pytest.mark.asyncio
async def test_project_activation_flow_and_invariant(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Active Tester")

    # Create two projects
    p1 = (
        await async_client.post("/api/v1/projects", json={"name": "Project 1"}, headers=headers)
    ).json()["data"]
    p2 = (
        await async_client.post("/api/v1/projects", json={"name": "Project 2"}, headers=headers)
    ).json()["data"]

    assert p1["is_active"] is False
    assert p2["is_active"] is False

    # Activate Project 1
    act1 = await async_client.post(f"/api/v1/projects/{p1['id']}/activate", headers=headers)
    assert act1.status_code == 200
    assert act1.json()["data"]["is_active"] is True

    # Activate Project 2 -> Project 1 must become inactive (single active focus invariant)
    act2 = await async_client.post(f"/api/v1/projects/{p2['id']}/activate", headers=headers)
    assert act2.status_code == 200
    assert act2.json()["data"]["is_active"] is True

    # Verify Project 1 is now inactive
    p1_refresh = (await async_client.get(f"/api/v1/projects/{p1['id']}", headers=headers)).json()[
        "data"
    ]
    assert p1_refresh["is_active"] is False

    # Activating already active project is idempotent
    act2_repeat = await async_client.post(f"/api/v1/projects/{p2['id']}/activate", headers=headers)
    assert act2_repeat.status_code == 200
    assert act2_repeat.json()["data"]["is_active"] is True


@pytest.mark.asyncio
async def test_concurrent_activation_safety(async_client: AsyncClient) -> None:
    headers, user_id_str = await create_test_user(async_client, "Race User")
    user_id = uuid.UUID(user_id_str)

    # Create 3 projects
    p1 = (
        await async_client.post("/api/v1/projects", json={"name": "Project One"}, headers=headers)
    ).json()["data"]
    p2 = (
        await async_client.post("/api/v1/projects", json={"name": "Project Two"}, headers=headers)
    ).json()["data"]
    p3 = (
        await async_client.post("/api/v1/projects", json={"name": "Project Three"}, headers=headers)
    ).json()["data"]

    # Fire concurrent activation requests for the same user
    tasks = [
        async_client.post(f"/api/v1/projects/{p1['id']}/activate", headers=headers),
        async_client.post(f"/api/v1/projects/{p2['id']}/activate", headers=headers),
        async_client.post(f"/api/v1/projects/{p3['id']}/activate", headers=headers),
    ]
    responses = await asyncio.gather(*tasks)

    # None of the responses should fail with 500
    for r in responses:
        assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"

    # Verify directly against database engine: COUNT(is_active = true) == 1
    async with async_session_factory() as session:
        count_stmt = select(func.count()).where(
            Project.user_id == user_id,
            Project.is_active.is_(True),
        )
        active_count = (await session.execute(count_stmt)).scalar_one()
        assert active_count == 1

    # Verify via API listing
    list_active = await async_client.get("/api/v1/projects?is_active=true", headers=headers)
    assert list_active.status_code == 200
    active_projects = list_active.json()["data"]
    assert len(active_projects) == 1
    assert active_projects[0]["id"] in [p1["id"], p2["id"], p3["id"]]


@pytest.mark.asyncio
async def test_project_archiving_flow(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Archive Tester")

    p = (
        await async_client.post("/api/v1/projects", json={"name": "To Archive"}, headers=headers)
    ).json()["data"]

    # Activate it first
    await async_client.post(f"/api/v1/projects/{p['id']}/activate", headers=headers)

    # Archive it
    arc_res = await async_client.post(f"/api/v1/projects/{p['id']}/archive", headers=headers)
    assert arc_res.status_code == 200
    arc_data = arc_res.json()["data"]
    assert arc_data["status"] == "ARCHIVED"
    assert arc_data["is_active"] is False
    assert arc_data["archived_at"] is not None

    # Archived project must not be returned in default list
    list_res = await async_client.get("/api/v1/projects", headers=headers)
    assert len(list_res.json()["data"]) == 0

    # Archived project returned when include_archived=true
    list_all = await async_client.get("/api/v1/projects?include_archived=true", headers=headers)
    assert len(list_all.json()["data"]) == 1

    # Cannot activate an archived project
    fail_act = await async_client.post(f"/api/v1/projects/{p['id']}/activate", headers=headers)
    assert fail_act.status_code == 400
    assert fail_act.json()["error"]["code"] == "PROJECT_INVALID_STATE"


@pytest.mark.asyncio
async def test_project_status_validation(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Validation User")

    # Invalid status in creation rejected with 422
    bad_res = await async_client.post(
        "/api/v1/projects",
        json={"name": "Bad Project", "status": "UNKNOWN_STATUS"},
        headers=headers,
    )
    assert bad_res.status_code == 422


@pytest.mark.asyncio
async def test_project_progress_validation(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Progress User")

    # Progress > 100 rejected with 422
    r_high = await async_client.post(
        "/api/v1/projects",
        json={"name": "Too High", "progress": 105},
        headers=headers,
    )
    assert r_high.status_code == 422

    # Progress < 0 rejected with 422
    r_low = await async_client.post(
        "/api/v1/projects",
        json={"name": "Too Low", "progress": -5},
        headers=headers,
    )
    assert r_low.status_code == 422


@pytest.mark.asyncio
async def test_project_technologies_deduplication_and_update(
    async_client: AsyncClient,
) -> None:
    headers, _ = await create_test_user(async_client, "Tech User")

    # Deduplicate case-insensitively on creation
    res = await async_client.post(
        "/api/v1/projects",
        json={
            "name": "Polyglot",
            "technologies": ["Python", "python", "PYTHON", "Postgres", "Redis"],
        },
        headers=headers,
    )
    assert res.status_code == 201
    techs = res.json()["data"]["technologies"]
    assert len(techs) == 3
    tech_names = [t["name"] for t in techs]
    assert "Python" in tech_names
    assert "Postgres" in tech_names
    assert "Redis" in tech_names

    p_id = res.json()["data"]["id"]

    # Patch technologies replacing list with deduplication
    patch_res = await async_client.patch(
        f"/api/v1/projects/{p_id}",
        json={"technologies": ["Swift", "swift", "FastAPI"]},
        headers=headers,
    )
    assert patch_res.status_code == 200
    new_techs = patch_res.json()["data"]["technologies"]
    assert len(new_techs) == 2
    new_tech_names = [t["name"] for t in new_techs]
    assert "Swift" in new_tech_names
    assert "FastAPI" in new_tech_names


@pytest.mark.asyncio
async def test_project_pagination_and_filtering(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Pagination User")

    # Create 5 projects
    for i in range(5):
        await async_client.post(
            "/api/v1/projects",
            json={"name": f"Project Batch {i}", "status": "PLANNING"},
            headers=headers,
        )

    # Page 1, limit 2
    r1 = await async_client.get("/api/v1/projects?page=1&limit=2", headers=headers)
    assert r1.status_code == 200
    b1 = r1.json()
    assert len(b1["data"]) == 2
    assert b1["meta"]["total"] == 5
    assert b1["meta"]["total_pages"] == 3
    assert b1["meta"]["page"] == 1
    assert b1["meta"]["limit"] == 2

    # Page 2, limit 2
    r2 = await async_client.get("/api/v1/projects?page=2&limit=2", headers=headers)
    assert r2.status_code == 200
    assert len(r2.json()["data"]) == 2

    # Page 3, limit 2
    r3 = await async_client.get("/api/v1/projects?page=3&limit=2", headers=headers)
    assert r3.status_code == 200
    assert len(r3.json()["data"]) == 1

    # Over max limit (>100) rejected with 422
    r_bad_limit = await async_client.get("/api/v1/projects?limit=101", headers=headers)
    assert r_bad_limit.status_code == 422


@pytest.mark.asyncio
async def test_project_context_metadata_endpoint(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Context User")

    create_res = await async_client.post(
        "/api/v1/projects",
        json={
            "name": "Core Intelligence Project",
            "summary": "Deterministic context foundation",
            "status": "ACTIVE",
            "priority": "HIGH",
            "progress": 50,
            "technologies": ["Python", "FastAPI"],
        },
        headers=headers,
    )
    proj_id = create_res.json()["data"]["id"]

    ctx_res = await async_client.get(f"/api/v1/projects/{proj_id}/context", headers=headers)
    assert ctx_res.status_code == 200
    data = ctx_res.json()["data"]

    assert data["project_id"] == proj_id
    assert data["name"] == "Core Intelligence Project"
    assert data["slug"] == "core-intelligence-project"
    assert data["summary"] == "Deterministic context foundation"
    assert data["status"] == "ACTIVE"
    assert data["priority"] == "HIGH"
    assert data["progress"] == 50
    assert data["is_active"] is False
    assert "Python" in data["active_technologies"]
    assert "FastAPI" in data["active_technologies"]

    # Invariant: deterministic M2 metadata without M3+ memory or knowledge placeholders
    assert "memory_count" not in data
    assert "knowledge_count" not in data
    assert "memories" not in data
    assert "knowledge" not in data
    assert "ai_summary" not in data


@pytest.mark.asyncio
async def test_default_project_ownership_validation(async_client: AsyncClient) -> None:
    headers_a, user_a_id_str = await create_test_user(async_client, "Owner A")
    headers_b, _ = await create_test_user(async_client, "Owner B")
    user_a_id = uuid.UUID(user_a_id_str)

    # User A creates Project A
    res_a = await async_client.post(
        "/api/v1/projects", json={"name": "Project of User A"}, headers=headers_a
    )
    proj_a_id = res_a.json()["data"]["id"]

    # User B creates Project B
    res_b = await async_client.post(
        "/api/v1/projects", json={"name": "Project of User B"}, headers=headers_b
    )
    proj_b_id = res_b.json()["data"]["id"]

    # 1. User A sets own Project A as default -> SUCCEEDS (200)
    set_own_res = await async_client.patch(
        "/api/v1/me/preferences",
        json={"default_project_id": proj_a_id},
        headers=headers_a,
    )
    assert set_own_res.status_code == 200
    assert set_own_res.json()["data"]["preferences"]["default_project_id"] == proj_a_id

    # Verify persistence in database
    async with async_session_factory() as session:
        pref = (
            await session.execute(select(UserPreference).where(UserPreference.user_id == user_a_id))
        ).scalar_one()
        assert pref.default_project_id == uuid.UUID(proj_a_id)

    # 2. User A attempts to set User B's Project B as default -> REJECTED (404 Not Found)
    set_other_res = await async_client.patch(
        "/api/v1/me/preferences",
        json={"default_project_id": proj_b_id},
        headers=headers_a,
    )
    assert set_other_res.status_code == 404
    assert set_other_res.json()["error"]["code"] == "PROJECT_NOT_FOUND"

    # Verify User A's default project in DB remained Project A (unchanged)
    async with async_session_factory() as session:
        pref = (
            await session.execute(select(UserPreference).where(UserPreference.user_id == user_a_id))
        ).scalar_one()
        assert pref.default_project_id == uuid.UUID(proj_a_id)

    # 3. User A attempts to set nonexistent project ID as default -> REJECTED (404 Not Found)
    fake_proj_id = str(uuid.uuid4())
    set_fake_res = await async_client.patch(
        "/api/v1/me/preferences",
        json={"default_project_id": fake_proj_id},
        headers=headers_a,
    )
    assert set_fake_res.status_code == 404
    assert set_fake_res.json()["error"]["code"] == "PROJECT_NOT_FOUND"

    # 4. User A clears default project by setting default_project_id to null -> SUCCEEDS (200)
    clear_res = await async_client.patch(
        "/api/v1/me/preferences",
        json={"default_project_id": None},
        headers=headers_a,
    )
    assert clear_res.status_code == 200
    assert clear_res.json()["data"]["preferences"]["default_project_id"] is None

    # Verify cleared in database
    async with async_session_factory() as session:
        pref = (
            await session.execute(select(UserPreference).where(UserPreference.user_id == user_a_id))
        ).scalar_one()
        assert pref.default_project_id is None

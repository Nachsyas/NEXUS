import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

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
    headers, user_id = await create_test_user(async_client, "Project Creator")

    payload = {
        "name": "  NEXUS Intelligence  ",
        "description": "Autonomous companion ecosystem",
        "status": "ACTIVE",
        "priority": "HIGH",
        "summary": "Core project setup",
        "progress": 35,
        "technologies": ["Swift", "FastAPI", "PostgreSQL"],
    }

    res = await async_client.post("/api/v1/projects", json=payload, headers=headers)
    assert res.status_code == 201
    body = res.json()
    assert body["success"] is True
    data = body["data"]

    assert data["name"] == "NEXUS Intelligence"
    assert data["slug"] == "nexus-intelligence"
    assert data["description"] == "Autonomous companion ecosystem"
    assert data["status"] == "ACTIVE"
    assert data["priority"] == "HIGH"
    assert data["progress"] == 35
    assert data["is_active"] is False
    assert data["archived_at"] is None
    assert len(data["technologies"]) == 3

    # Verify UUIDv7
    proj_uuid = uuid.UUID(data["id"])
    assert proj_uuid.version == 7


@pytest.mark.asyncio
async def test_slug_generation_and_deterministic_collision(async_client: AsyncClient) -> None:
    headers_1, _ = await create_test_user(async_client, "User One")
    headers_2, _ = await create_test_user(async_client, "User Two")

    # User 1 creates first project
    r1 = await async_client.post(
        "/api/v1/projects", json={"name": "Quantum Leap"}, headers=headers_1
    )
    assert r1.status_code == 201
    assert r1.json()["data"]["slug"] == "quantum-leap"

    # User 1 creates second project with same name -> collision handled deterministically
    r2 = await async_client.post(
        "/api/v1/projects", json={"name": "Quantum Leap"}, headers=headers_1
    )
    assert r2.status_code == 201
    assert r2.json()["data"]["slug"] == "quantum-leap-2"

    # User 1 creates third project with same name
    r3 = await async_client.post(
        "/api/v1/projects", json={"name": "Quantum Leap"}, headers=headers_1
    )
    assert r3.status_code == 201
    assert r3.json()["data"]["slug"] == "quantum-leap-3"

    # User 2 creates project with same name -> gets clean base slug (per-user namespace)
    r4 = await async_client.post(
        "/api/v1/projects", json={"name": "Quantum Leap"}, headers=headers_2
    )
    assert r4.status_code == 201
    assert r4.json()["data"]["slug"] == "quantum-leap"


@pytest.mark.asyncio
async def test_cross_user_isolation_and_idor(async_client: AsyncClient) -> None:
    headers_a, user_a_id = await create_test_user(async_client, "User A")
    headers_b, user_b_id = await create_test_user(async_client, "User B")

    # User A creates a project
    create_res = await async_client.post(
        "/api/v1/projects",
        json={"name": "Project Secret A", "technologies": ["Rust"]},
        headers=headers_a,
    )
    proj_a_id = create_res.json()["data"]["id"]

    # User B cannot read User A project (404 to avoid resource existence leaking)
    get_res = await async_client.get(f"/api/v1/projects/{proj_a_id}", headers=headers_b)
    assert get_res.status_code == 404
    assert get_res.json()["error"]["code"] == "PROJECT_NOT_FOUND"

    # User B cannot update User A project
    patch_res = await async_client.patch(
        f"/api/v1/projects/{proj_a_id}",
        json={"name": "Hacked Project"},
        headers=headers_b,
    )
    assert patch_res.status_code == 404

    # User B cannot activate User A project
    act_res = await async_client.post(f"/api/v1/projects/{proj_a_id}/activate", headers=headers_b)
    assert act_res.status_code == 404

    # User B cannot archive User A project
    arch_res = await async_client.post(f"/api/v1/projects/{proj_a_id}/archive", headers=headers_b)
    assert arch_res.status_code == 404

    # User B cannot get context of User A project
    ctx_res = await async_client.get(f"/api/v1/projects/{proj_a_id}/context", headers=headers_b)
    assert ctx_res.status_code == 404

    # User B cannot mass-assign user_id to User A
    spoof_res = await async_client.post(
        "/api/v1/projects",
        json={"name": "Spoofed Project", "user_id": user_a_id},
        headers=headers_b,
    )
    assert spoof_res.status_code == 201
    # Verify ownership in DB is assigned to User B, not User A
    spoofed_id = uuid.UUID(spoof_res.json()["data"]["id"])
    async with async_session_factory() as session:
        proj_in_db = (
            await session.execute(select(Project).where(Project.id == spoofed_id))
        ).scalar_one()
        assert str(proj_in_db.user_id) == user_b_id


@pytest.mark.asyncio
async def test_project_activation_flow_and_invariant(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Activation User")

    # Create 2 projects
    p1 = (await async_client.post("/api/v1/projects", json={"name": "P1"}, headers=headers)).json()[
        "data"
    ]
    p2 = (await async_client.post("/api/v1/projects", json={"name": "P2"}, headers=headers)).json()[
        "data"
    ]

    # Initially zero active
    assert p1["is_active"] is False
    assert p2["is_active"] is False

    # Activate P1
    act1 = await async_client.post(f"/api/v1/projects/{p1['id']}/activate", headers=headers)
    assert act1.status_code == 200
    assert act1.json()["data"]["is_active"] is True

    # Check P1 is active
    get_p1 = (await async_client.get(f"/api/v1/projects/{p1['id']}", headers=headers)).json()[
        "data"
    ]
    assert get_p1["is_active"] is True

    # Activate P2 -> atomically deactivates P1 and activates P2
    act2 = await async_client.post(f"/api/v1/projects/{p2['id']}/activate", headers=headers)
    assert act2.status_code == 200
    assert act2.json()["data"]["is_active"] is True

    # Verify P1 is now inactive and P2 is active
    get_p1 = (await async_client.get(f"/api/v1/projects/{p1['id']}", headers=headers)).json()[
        "data"
    ]
    get_p2 = (await async_client.get(f"/api/v1/projects/{p2['id']}", headers=headers)).json()[
        "data"
    ]
    assert get_p1["is_active"] is False
    assert get_p2["is_active"] is True

    # Re-activating P2 is idempotent
    act2_repeat = await async_client.post(f"/api/v1/projects/{p2['id']}/activate", headers=headers)
    assert act2_repeat.status_code == 200
    assert act2_repeat.json()["data"]["is_active"] is True

    # Database partial unique index enforcement:
    # Directly attempting to violate partial unique index raises IntegrityError
    async with async_session_factory() as session:
        proj_1_db = (
            await session.execute(select(Project).where(Project.id == uuid.UUID(p1["id"])))
        ).scalar_one()
        proj_1_db.is_active = True
        with pytest.raises(IntegrityError):
            await session.flush()
        await session.rollback()


@pytest.mark.asyncio
async def test_project_archiving_flow(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Archiving User")

    p = (
        await async_client.post("/api/v1/projects", json={"name": "To Archive"}, headers=headers)
    ).json()["data"]
    p_id = p["id"]

    # Activate it first
    await async_client.post(f"/api/v1/projects/{p_id}/activate", headers=headers)

    # Archive it
    arch_res = await async_client.post(f"/api/v1/projects/{p_id}/archive", headers=headers)
    assert arch_res.status_code == 200
    arch_data = arch_res.json()["data"]
    assert arch_data["status"] == "ARCHIVED"
    assert arch_data["is_active"] is False
    assert arch_data["archived_at"] is not None

    # Cannot activate an archived project
    act_res = await async_client.post(f"/api/v1/projects/{p_id}/activate", headers=headers)
    assert act_res.status_code == 400
    assert act_res.json()["error"]["code"] == "PROJECT_INVALID_STATE"

    # Default list excludes archived projects
    list_res = await async_client.get("/api/v1/projects", headers=headers)
    assert len(list_res.json()["data"]) == 0

    # List with include_archived=true includes it
    list_all = await async_client.get("/api/v1/projects?include_archived=true", headers=headers)
    assert len(list_all.json()["data"]) == 1


@pytest.mark.asyncio
async def test_project_status_validation(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Status Validator")

    # Valid statuses
    for valid_status in ["IDEA", "PLANNING", "ACTIVE", "PAUSED", "COMPLETED"]:
        r = await async_client.post(
            "/api/v1/projects",
            json={"name": f"Project {valid_status}", "status": valid_status},
            headers=headers,
        )
        assert r.status_code == 201
        assert r.json()["data"]["status"] == valid_status

    # Invalid status rejected with 422
    bad_res = await async_client.post(
        "/api/v1/projects",
        json={"name": "Bad Status", "status": "SUPER_ACTIVE"},
        headers=headers,
    )
    assert bad_res.status_code == 422


@pytest.mark.asyncio
async def test_project_progress_validation(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Progress Validator")

    # Bounds: 0 is valid
    r0 = await async_client.post(
        "/api/v1/projects", json={"name": "P0", "progress": 0}, headers=headers
    )
    assert r0.status_code == 201
    assert r0.json()["data"]["progress"] == 0

    # Bounds: 100 is valid
    r100 = await async_client.post(
        "/api/v1/projects", json={"name": "P100", "progress": 100}, headers=headers
    )
    assert r100.status_code == 201
    assert r100.json()["data"]["progress"] == 100

    # Negative rejected
    r_neg = await async_client.post(
        "/api/v1/projects", json={"name": "PNeg", "progress": -1}, headers=headers
    )
    assert r_neg.status_code == 422

    # > 100 rejected
    r_over = await async_client.post(
        "/api/v1/projects", json={"name": "POver", "progress": 101}, headers=headers
    )
    assert r_over.status_code == 422


@pytest.mark.asyncio
async def test_project_technologies_deduplication_and_update(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Tech User")

    # Creation with duplicate entries (case-insensitive deduplication)
    r = await async_client.post(
        "/api/v1/projects",
        json={
            "name": "FullStack Project",
            "technologies": ["FastAPI", "fastapi", "Swift", "SWIFT ", "PostgreSQL"],
        },
        headers=headers,
    )
    assert r.status_code == 201
    techs = [t["name"] for t in r.json()["data"]["technologies"]]
    assert len(techs) == 3
    assert "FastAPI" in techs
    assert "Swift" in techs
    assert "PostgreSQL" in techs

    proj_id = r.json()["data"]["id"]

    # Update technologies
    patch_res = await async_client.patch(
        f"/api/v1/projects/{proj_id}",
        json={"technologies": ["Python", "PyTorch"]},
        headers=headers,
    )
    assert patch_res.status_code == 200
    updated_techs = [t["name"] for t in patch_res.json()["data"]["technologies"]]
    assert len(updated_techs) == 2
    assert "Python" in updated_techs
    assert "PyTorch" in updated_techs


@pytest.mark.asyncio
async def test_project_pagination_and_filtering(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Pagination User")

    # Create 5 projects
    for i in range(5):
        await async_client.post(
            "/api/v1/projects",
            json={"name": f"Numbered Project {i + 1}"},
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
    # Invariant: deterministic M2 metadata without M3+ memory / AI
    assert data["memory_count"] == 0
    assert data["knowledge_count"] == 0
    assert "memories" not in data
    assert "ai_summary" not in data


@pytest.mark.asyncio
async def test_user_preference_default_project_fk(async_client: AsyncClient) -> None:
    headers, user_id_str = await create_test_user(async_client, "Default Pref User")
    user_id = uuid.UUID(user_id_str)

    # Create project
    proj_res = await async_client.post(
        "/api/v1/projects", json={"name": "Default Candidate"}, headers=headers
    )
    proj_id_str = proj_res.json()["data"]["id"]
    proj_id = uuid.UUID(proj_id_str)

    # Set default_project_id in preferences
    pref_res = await async_client.patch(
        "/api/v1/me/preferences",
        json={"default_project_id": proj_id_str},
        headers=headers,
    )
    assert pref_res.status_code == 200
    assert pref_res.json()["data"]["preferences"]["default_project_id"] == proj_id_str

    # Verify in DB and relationship loading
    async with async_session_factory() as session:
        pref = (
            await session.execute(select(UserPreference).where(UserPreference.user_id == user_id))
        ).scalar_one()
        assert pref.default_project_id == proj_id


@pytest.mark.asyncio
async def test_concurrent_activation_safety(async_client: AsyncClient) -> None:
    import asyncio

    headers, _ = await create_test_user(async_client, "Race User")

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

    # Fire concurrent activation requests
    tasks = [
        async_client.post(f"/api/v1/projects/{p1['id']}/activate", headers=headers),
        async_client.post(f"/api/v1/projects/{p2['id']}/activate", headers=headers),
        async_client.post(f"/api/v1/projects/{p3['id']}/activate", headers=headers),
    ]
    _ = await asyncio.gather(*tasks, return_exceptions=True)

    # Verify after all finish: exactly one project is active in the database
    list_active = await async_client.get("/api/v1/projects?is_active=true", headers=headers)
    assert list_active.status_code == 200
    active_projects = list_active.json()["data"]
    assert len(active_projects) == 1
    assert active_projects[0]["id"] in [p1["id"], p2["id"], p3["id"]]

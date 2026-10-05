import asyncio
import datetime
import time
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.core.database import async_session_factory
from app.domains.auth.apple_verifier import MockAppleVerifier, set_apple_verifier
from app.domains.memories.embedding import (
    DeterministicTestEmbeddingProvider,
    reset_embedding_provider,
    set_embedding_provider,
)
from app.domains.memories.models import (
    Memory,
    utc_now,
)


@pytest.fixture(autouse=True)
def setup_mock_verifier() -> None:
    mock_verifier = MockAppleVerifier(
        default_subject="apple-sub-test-default",
        default_email="default@nexus.test",
    )
    set_apple_verifier(mock_verifier)
    reset_embedding_provider()


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


async def create_test_project(
    client: AsyncClient, headers: dict[str, str], name: str = "Test Project"
) -> str:
    res = await client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": name, "description": "A test project for memory scoping."},
    )
    assert res.status_code == 201
    return str(res.json()["data"]["id"])


@pytest.mark.asyncio
async def test_anonymous_memory_access_rejected(async_client: AsyncClient) -> None:
    fake_id = uuid.uuid4()
    assert (await async_client.get("/api/v1/memories")).status_code == 401
    assert (
        await async_client.post(
            "/api/v1/memories",
            json={
                "memory_type": "PERSONAL_FACT",
                "subject": "User",
                "predicate": "name",
                "value_text": "Alex",
            },
        )
    ).status_code == 401
    assert (await async_client.get(f"/api/v1/memories/{fake_id}")).status_code == 401
    assert (
        await async_client.patch(f"/api/v1/memories/{fake_id}", json={"value_text": "Alex Updated"})
    ).status_code == 401
    assert (await async_client.post(f"/api/v1/memories/{fake_id}/forget")).status_code == 401
    assert (
        await async_client.post("/api/v1/memories/search", json={"query": "test"})
    ).status_code == 401


@pytest.mark.asyncio
async def test_memory_creation_and_attributes(async_client: AsyncClient) -> None:
    headers, user_id_str = await create_test_user(async_client, "Memory Creator")

    payload = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Preferred Name",
        "predicate": "is",
        "value_text": "Alex",
        "value_json": {"formal": "Alexander"},
        "importance": 0.8,
        "sensitivity": "LOW",
    }
    res = await async_client.post("/api/v1/memories", headers=headers, json=payload)
    assert res.status_code == 201
    data = res.json()["data"]

    assert data["memory_type"] == "PERSONAL_FACT"
    assert data["subject"] == "Preferred Name"
    assert data["predicate"] == "is"
    assert data["value_text"] == "Alex"
    assert data["value_json"] == {"formal": "Alexander"}
    assert data["status"] == "ACTIVE"
    assert data["importance"] == 0.8
    assert data["confidence"] == 1.0
    assert data["source_type"] == "USER_EXPLICIT"
    assert data["user_id"] == user_id_str
    assert data["project_id"] is None
    assert data["summary"] == "Preferred Name: is -> Alex"
    assert data["superseded_by"] is None

    # Check database persistence
    mem_uuid = uuid.UUID(data["id"])
    async with async_session_factory() as session:
        mem = (await session.execute(select(Memory).where(Memory.id == mem_uuid))).scalar_one()
        assert mem.subject == "Preferred Name"
        assert mem.value_text == "Alex"


@pytest.mark.asyncio
async def test_all_10_canonical_memory_types(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Taxonomy Tester")
    project_id = await create_test_project(async_client, headers, "Nexus Taxonomy Project")

    # 1. Global / Personal types
    global_types = [
        ("PERSONAL_FACT", "User timezone", "is", "Asia/Jakarta"),
        ("PREFERENCE", "Response style", "is", "Concise and direct"),
        ("INTEREST", "Architecture", "interested_in", "Distributed Systems"),
        ("SKILL", "Swift", "proficiency", "Advanced"),
        ("GOAL", "Ship NEXUS", "target_date", "2026-Q4"),
        ("BEHAVIOR_PATTERN", "Work hours", "usually_active", "Morning"),
    ]

    for mtype, sub, pred, val in global_types:
        res = await async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": mtype,
                "subject": sub,
                "predicate": pred,
                "value_text": val,
            },
        )
        assert res.status_code == 201, f"Failed for {mtype}: {res.text}"
        assert res.json()["data"]["memory_type"] == mtype

    # 2. Project-scoped types
    project_types = [
        ("PROJECT_FACT", "Database baseline", "uses", "PostgreSQL 16 with pgvector"),
        ("PROJECT_DECISION", "Embedding model", "decided", "Provider abstraction per ADR-011"),
        ("PROJECT_PROGRESS", "Milestone M2", "completed", "Projects and Tech stack foundation"),
        ("PROJECT_NEXT_ACTION", "Milestone M3", "implement", "Memory Core and Control Center"),
    ]

    for mtype, sub, pred, val in project_types:
        res = await async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": mtype,
                "project_id": project_id,
                "subject": sub,
                "predicate": pred,
                "value_text": val,
            },
        )
        assert res.status_code == 201, f"Failed for {mtype}: {res.text}"
        assert res.json()["data"]["memory_type"] == mtype

    # 3. Invalid / Invented types rejected
    for invalid in ["FACT", "NOTE", "DECISION", "CONTEXT", "OTHER"]:
        res = await async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": invalid,
                "subject": "Foo",
                "predicate": "bar",
                "value_text": "baz",
            },
        )
        assert res.status_code == 422


@pytest.mark.asyncio
async def test_project_memory_scope_invariants(async_client: AsyncClient) -> None:
    headers_a, _ = await create_test_user(async_client, "User A")
    headers_b, _ = await create_test_user(async_client, "User B")
    proj_a = await create_test_project(async_client, headers_a, "Project A")
    proj_b = await create_test_project(async_client, headers_b, "Project B")

    # Project type without project_id -> 422
    res = await async_client.post(
        "/api/v1/memories",
        headers=headers_a,
        json={
            "memory_type": "PROJECT_FACT",
            "subject": "Missing Project",
            "predicate": "is",
            "value_text": "Invalid",
        },
    )
    assert res.status_code == 422

    # Global type with project_id -> 422
    res = await async_client.post(
        "/api/v1/memories",
        headers=headers_a,
        json={
            "memory_type": "PERSONAL_FACT",
            "project_id": proj_a,
            "subject": "Personal Fact with Project",
            "predicate": "is",
            "value_text": "Invalid",
        },
    )
    assert res.status_code == 422

    # Non-existent project -> 404 safe
    fake_proj = str(uuid.uuid4())
    res = await async_client.post(
        "/api/v1/memories",
        headers=headers_a,
        json={
            "memory_type": "PROJECT_FACT",
            "project_id": fake_proj,
            "subject": "Fake Project",
            "predicate": "is",
            "value_text": "Data",
        },
    )
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "PROJECT_NOT_FOUND"

    # Cross-tenant project access -> 404 safe (User A cannot attach memory to User B's project)
    res = await async_client.post(
        "/api/v1/memories",
        headers=headers_a,
        json={
            "memory_type": "PROJECT_FACT",
            "project_id": proj_b,
            "subject": "Cross-tenant Project Fact",
            "predicate": "is",
            "value_text": "Attack data",
        },
    )
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "PROJECT_NOT_FOUND"


@pytest.mark.asyncio
async def test_never_store_secret_safety_policy(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Safety Tester")

    forbidden_inputs = [
        ("password = SuperSecretPass123!", "password assignment with equals"),
        ("password: MyAdminPassword999", "password assignment with colon"),
        ("sk-proj-1234567890abcdef1234567890abcdef", "OpenAI secret API key"),
        ("ghp_123456789012345678901234567890123456", "GitHub personal access token"),
        ("AKIAIOSFODNN7EXAMPLE", "AWS access key identifier"),
        ("-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...", "PEM private key header"),
        (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.c2VjcmV0",
            "Bearer JWT token",
        ),
        ("otp: 938402", "OTP credential assignment"),
        (
            "recovery phrase: witch collapse practice feed shame open despair creek road again ice least",
            "Seed phrase",
        ),
    ]

    for secret_text, desc in forbidden_inputs:
        res = await async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": "PERSONAL_FACT",
                "subject": "Secret Entry",
                "predicate": "has",
                "value_text": secret_text,
            },
        )
        assert res.status_code == 400, f"Expected 400 for {desc}, got {res.status_code}: {res.text}"
        err = res.json()["error"]
        assert err["code"] == "MEMORY_SECRET_REJECTED"
        # Zero secret leakage in response message or details
        assert secret_text not in err["message"]
        assert secret_text not in str(err.get("details"))

    # Also test nested secret in value_json
    res = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "PERSONAL_FACT",
            "subject": "Nested Secret",
            "predicate": "has",
            "value_text": "Benign outer text",
            "value_json": {"credential": "password = hidden123456"},
        },
    )
    assert res.status_code == 400
    assert res.json()["error"]["code"] == "MEMORY_SECRET_REJECTED"

    # Test benign discussion of secrets passes cleanly (no false positives)
    benign_discussions = [
        "I use a password manager for my accounts",
        "We need an API key rotation strategy for production",
        "Discussing two-factor authentication and OTP delivery via SMS",
        "The authentication architecture uses JWT sessions",
        "Private key cryptography is based on elliptic curves",
    ]

    for benign in benign_discussions:
        res = await async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": "PERSONAL_FACT",
                "subject": "Benign Discussion",
                "predicate": "notes",
                "value_text": benign,
            },
        )
        assert res.status_code == 201, f"False positive rejection on: {benign} ({res.text})"


@pytest.mark.asyncio
async def test_deterministic_deduplication(async_client: AsyncClient) -> None:
    headers, user_id_str = await create_test_user(async_client, "Dedup Tester")
    user_uuid = uuid.UUID(user_id_str)

    payload1 = {
        "memory_type": "PREFERENCE",
        "subject": "Code Indentation",
        "predicate": "preferred_spaces",
        "value_text": "4 spaces",
    }
    res1 = await async_client.post("/api/v1/memories", headers=headers, json=payload1)
    assert res1.status_code == 201
    mem1_id = res1.json()["data"]["id"]

    # Post identical fact with slight casing/whitespace difference in subject/predicate
    payload2 = {
        "memory_type": "PREFERENCE",
        "subject": "  code indentation  ",
        "predicate": "PREFERRED_SPACES",
        "value_text": "4 spaces",
    }
    res2 = await async_client.post("/api/v1/memories", headers=headers, json=payload2)
    assert res2.status_code == 201
    mem2_id = res2.json()["data"]["id"]

    # Must return identical memory ID (no duplicate created)
    assert mem1_id == mem2_id

    # Verify database has exactly 1 row for this user
    async with async_session_factory() as session:
        count = (
            await session.execute(
                select(func.count(Memory.id)).where(
                    Memory.user_id == user_uuid,
                    Memory.memory_type == "PREFERENCE",
                    Memory.status == "ACTIVE",
                )
            )
        ).scalar()
        assert count == 1


@pytest.mark.asyncio
async def test_conflict_and_supersede(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Supersede Tester")

    # Step 1: Initial fact
    res1 = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "PREFERENCE",
            "subject": "Theme",
            "predicate": "prefers",
            "value_text": "Dark Mode",
        },
    )
    assert res1.status_code == 201
    old_id = res1.json()["data"]["id"]

    # Step 2: Conflicting fact with same identity but different value
    res2 = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "PREFERENCE",
            "subject": "theme",
            "predicate": "prefers",
            "value_text": "Light Mode",
        },
    )
    assert res2.status_code == 201
    new_id = res2.json()["data"]["id"]
    assert new_id != old_id

    # Step 3: Check old memory is SUPERSEDED and linked to new
    res_old = await async_client.get(f"/api/v1/memories/{old_id}", headers=headers)
    assert res_old.status_code == 200
    old_data = res_old.json()["data"]
    assert old_data["status"] == "SUPERSEDED"
    assert old_data["superseded_by"] == new_id

    # Step 4: Check new memory is ACTIVE
    res_new = await async_client.get(f"/api/v1/memories/{new_id}", headers=headers)
    assert res_new.status_code == 200
    new_data = res_new.json()["data"]
    assert new_data["status"] == "ACTIVE"
    assert new_data["superseded_by"] is None

    # Step 5: Default listing only contains the ACTIVE memory
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    assert res_list.status_code == 200
    listed_ids = [item["id"] for item in res_list.json()["data"]]
    assert new_id in listed_ids
    assert old_id not in listed_ids


@pytest.mark.asyncio
async def test_concurrent_writes_and_supersede(async_client: AsyncClient) -> None:
    headers, user_id_str = await create_test_user(async_client, "Concurrency Tester")
    user_uuid = uuid.UUID(user_id_str)

    # 1. Concurrent identical writes -> deduplicated cleanly without crash
    async def post_same() -> int:
        res = await async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": "SKILL",
                "subject": "Python",
                "predicate": "level",
                "value_text": "Senior",
            },
        )
        return res.status_code

    statuses = await asyncio.gather(post_same(), post_same(), post_same())
    assert all(s == 201 for s in statuses)

    async with async_session_factory() as session:
        active_count = (
            await session.execute(
                select(func.count(Memory.id)).where(
                    Memory.user_id == user_uuid,
                    Memory.memory_type == "SKILL",
                    Memory.subject == "Python",
                    Memory.status == "ACTIVE",
                )
            )
        ).scalar()
        assert active_count == 1


@pytest.mark.asyncio
async def test_expiration_query_exclusion(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Expiration Tester")

    # Create memory expiring in the past
    past_time = (utc_now() - datetime.timedelta(hours=2)).isoformat()
    res = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "GOAL",
            "subject": "Sprint Target",
            "predicate": "finish_by",
            "value_text": "Completed yesterday",
            "expires_at": past_time,
        },
    )
    assert res.status_code == 201
    expired_id = res.json()["data"]["id"]

    # Excluded from default list
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    assert res_list.status_code == 200
    ids = [m["id"] for m in res_list.json()["data"]]
    assert expired_id not in ids

    # Direct fetch still possible for audit
    res_direct = await async_client.get(f"/api/v1/memories/{expired_id}", headers=headers)
    assert res_direct.status_code == 200


@pytest.mark.asyncio
async def test_forget_memory_semantics(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Forget Tester")

    res = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "PERSONAL_FACT",
            "subject": "Private Hobby",
            "predicate": "enjoys",
            "value_text": "Vintage Watch Collecting",
        },
    )
    assert res.status_code == 201
    mem_id = res.json()["data"]["id"]

    # Forget memory
    res_forget = await async_client.post(f"/api/v1/memories/{mem_id}/forget", headers=headers)
    assert res_forget.status_code == 200
    forget_data = res_forget.json()["data"]
    assert forget_data["id"] == mem_id
    assert forget_data["status"] == "FORGOTTEN"
    assert "forgotten_at" in forget_data

    # Idempotent: forget again succeeds
    res_forget_again = await async_client.post(f"/api/v1/memories/{mem_id}/forget", headers=headers)
    assert res_forget_again.status_code == 200
    assert res_forget_again.json()["data"]["status"] == "FORGOTTEN"

    # Excluded from active listing
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    assert res_list.status_code == 200
    ids = [m["id"] for m in res_list.json()["data"]]
    assert mem_id not in ids


@pytest.mark.asyncio
async def test_patch_memory_and_terminal_rejection(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Patch Tester")

    res = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "SKILL",
            "subject": "Rust",
            "predicate": "level",
            "value_text": "Intermediate",
            "importance": 0.5,
        },
    )
    assert res.status_code == 201
    mem_id = res.json()["data"]["id"]

    # Valid patch
    res_patch = await async_client.patch(
        f"/api/v1/memories/{mem_id}",
        headers=headers,
        json={"value_text": "Advanced", "importance": 0.9},
    )
    assert res_patch.status_code == 200
    patched = res_patch.json()["data"]
    assert patched["value_text"] == "Advanced"
    assert patched["importance"] == 0.9
    assert patched["summary"] == "Rust: level -> Advanced"

    # Patch with secret is rejected
    res_secret_patch = await async_client.patch(
        f"/api/v1/memories/{mem_id}",
        headers=headers,
        json={"value_text": "password: leaked_in_patch_123"},
    )
    assert res_secret_patch.status_code == 400
    assert res_secret_patch.json()["error"]["code"] == "MEMORY_SECRET_REJECTED"

    # Forget memory, then attempt patch -> 409
    await async_client.post(f"/api/v1/memories/{mem_id}/forget", headers=headers)
    res_terminal_patch = await async_client.patch(
        f"/api/v1/memories/{mem_id}",
        headers=headers,
        json={"value_text": "Should Fail"},
    )
    assert res_terminal_patch.status_code == 409
    assert res_terminal_patch.json()["error"]["code"] == "MEMORY_INVALID_STATE"


@pytest.mark.asyncio
async def test_multi_tenant_isolation_and_idor(async_client: AsyncClient) -> None:
    headers_a, _ = await create_test_user(async_client, "User Alpha")
    headers_b, _ = await create_test_user(async_client, "User Beta")

    # User A creates memory
    res_a = await async_client.post(
        "/api/v1/memories",
        headers=headers_a,
        json={
            "memory_type": "PERSONAL_FACT",
            "subject": "Alpha Fact",
            "predicate": "is",
            "value_text": "Confidential Alpha",
        },
    )
    assert res_a.status_code == 201
    mem_a_id = res_a.json()["data"]["id"]

    # User B attempts GET User A's memory -> 404
    assert (
        await async_client.get(f"/api/v1/memories/{mem_a_id}", headers=headers_b)
    ).status_code == 404

    # User B attempts PATCH User A's memory -> 404
    assert (
        await async_client.patch(
            f"/api/v1/memories/{mem_a_id}",
            headers=headers_b,
            json={"value_text": "Hacked"},
        )
    ).status_code == 404

    # User B attempts FORGET User A's memory -> 404
    assert (
        await async_client.post(f"/api/v1/memories/{mem_a_id}/forget", headers=headers_b)
    ).status_code == 404

    # User B's listing does not show User A's memory
    res_b_list = await async_client.get("/api/v1/memories", headers=headers_b)
    assert res_b_list.status_code == 200
    assert not any(m["id"] == mem_a_id for m in res_b_list.json()["data"])


@pytest.mark.asyncio
async def test_semantic_search_with_and_without_provider(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Vector Searcher")
    proj_id = await create_test_project(async_client, headers, "Search Test Project")

    # 1. Search when provider unavailable -> returns 503 MEMORY_EMBEDDING_UNAVAILABLE
    reset_embedding_provider()
    res_unavail = await async_client.post(
        "/api/v1/memories/search",
        headers=headers,
        json={"query": "test query"},
    )
    assert res_unavail.status_code == 503
    assert res_unavail.json()["error"]["code"] == "MEMORY_EMBEDDING_UNAVAILABLE"

    # 2. Configure DeterministicTestEmbeddingProvider
    set_embedding_provider(DeterministicTestEmbeddingProvider(dimension=1536))

    # Create distinct memories
    res_m1 = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "PROJECT_FACT",
            "project_id": proj_id,
            "subject": "Storage Engine",
            "predicate": "uses",
            "value_text": "PostgreSQL with pgvector for vector similarity retrieval",
        },
    )
    assert res_m1.status_code == 201
    m1_id = res_m1.json()["data"]["id"]

    res_m2 = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "PERSONAL_FACT",
            "subject": "Favorite Food",
            "predicate": "likes",
            "value_text": "Sushi and ramen",
        },
    )
    assert res_m2.status_code == 201

    # Search for vector storage
    res_search = await async_client.post(
        "/api/v1/memories/search",
        headers=headers,
        json={"query": "PostgreSQL with pgvector for vector similarity retrieval", "limit": 5},
    )
    assert res_search.status_code == 200
    hits = res_search.json()["data"]
    assert len(hits) >= 1
    # Top hit must be the exact text match
    assert hits[0]["id"] == m1_id
    assert hits[0]["similarity_score"] > 0.99

    # Project scoping: search within proj_id
    res_proj_search = await async_client.post(
        "/api/v1/memories/search",
        headers=headers,
        json={
            "query": "PostgreSQL with pgvector for vector similarity retrieval",
            "project_id": proj_id,
        },
    )
    assert res_proj_search.status_code == 200
    proj_hits = res_proj_search.json()["data"]
    assert all(h["project_id"] == proj_id for h in proj_hits)

    # Cross-tenant project search -> 404 safe
    fake_proj = str(uuid.uuid4())
    res_fake_proj = await async_client.post(
        "/api/v1/memories/search",
        headers=headers,
        json={"query": "query", "project_id": fake_proj},
    )
    assert res_fake_proj.status_code == 404


@pytest.mark.asyncio
async def test_memory_performance_and_latency(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Benchmarker")
    set_embedding_provider(DeterministicTestEmbeddingProvider(dimension=1536))

    payload = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Benchmark Fact",
        "predicate": "test_latency",
        "value_text": "Testing performance latency bounds",
    }

    # 1. Create latency
    t0 = time.perf_counter()
    res_create = await async_client.post("/api/v1/memories", headers=headers, json=payload)
    create_duration_ms = (time.perf_counter() - t0) * 1000
    assert res_create.status_code == 201
    mem_id = res_create.json()["data"]["id"]

    # 2. Dedup latency
    t0 = time.perf_counter()
    res_dedup = await async_client.post("/api/v1/memories", headers=headers, json=payload)
    dedup_duration_ms = (time.perf_counter() - t0) * 1000
    assert res_dedup.status_code == 201

    # 3. List latency
    t0 = time.perf_counter()
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    list_duration_ms = (time.perf_counter() - t0) * 1000
    assert res_list.status_code == 200

    # 4. Search latency
    t0 = time.perf_counter()
    res_search = await async_client.post(
        "/api/v1/memories/search",
        headers=headers,
        json={"query": "Testing performance latency bounds"},
    )
    search_duration_ms = (time.perf_counter() - t0) * 1000
    assert res_search.status_code == 200

    # 5. Forget latency
    t0 = time.perf_counter()
    res_forget = await async_client.post(f"/api/v1/memories/{mem_id}/forget", headers=headers)
    forget_duration_ms = (time.perf_counter() - t0) * 1000
    assert res_forget.status_code == 200

    print(
        f"\n[M3 Performance Benchmark]\n"
        f"  Create: {create_duration_ms:.2f}ms\n"
        f"  Dedup:  {dedup_duration_ms:.2f}ms\n"
        f"  List:   {list_duration_ms:.2f}ms\n"
        f"  Search: {search_duration_ms:.2f}ms\n"
        f"  Forget: {forget_duration_ms:.2f}ms\n"
    )

    # All operations should comfortably execute well under 200ms locally
    assert create_duration_ms < 200
    assert dedup_duration_ms < 200
    assert list_duration_ms < 200
    assert search_duration_ms < 200
    assert forget_duration_ms < 200

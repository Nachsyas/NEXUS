import asyncio
import time
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.database import async_session_factory
from app.domains.auth.apple_verifier import MockAppleVerifier, set_apple_verifier
from app.domains.memories.embedding import (
    DeterministicTestEmbeddingProvider,
    reset_embedding_provider,
    set_embedding_provider,
)
from app.domains.memories.models import Memory, MemoryStatus


@pytest.fixture(autouse=True)
def setup_mock_verifier() -> None:
    mock_verifier = MockAppleVerifier(
        default_subject="apple-sub-test-default",
        default_email="default@nexus.test",
    )
    set_apple_verifier(mock_verifier)


async def create_test_user(
    async_client: AsyncClient, name: str = "Memory Tester"
) -> tuple[dict[str, str], str]:
    sub = f"apple-sub-mem-{uuid.uuid4().hex[:8]}"
    email = f"user-{uuid.uuid4().hex[:8]}@example.com"
    res = await async_client.post(
        "/api/v1/auth/apple",
        json={
            "identity_token": f"mock-apple:{sub}:{email}",
            "user_info": {"name": name, "email": email},
        },
    )
    assert res.status_code == 200
    data = res.json()["data"]
    token = data["access_token"]
    user_id = data["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


async def create_test_project(
    async_client: AsyncClient, headers: dict[str, str], name: str = "Test Project"
) -> str:
    res = await async_client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": name, "description": "Memory test project"},
    )
    assert res.status_code == 201
    return str(res.json()["data"]["id"])


@pytest.mark.asyncio
async def test_anonymous_memory_access_rejected(async_client: AsyncClient) -> None:
    res = await async_client.get("/api/v1/memories")
    assert res.status_code == 401

    res_post = await async_client.post(
        "/api/v1/memories",
        json={
            "memory_type": "PERSONAL_FACT",
            "subject": "User",
            "predicate": "lives_in",
            "value_text": "Tokyo",
        },
    )
    assert res_post.status_code == 401


@pytest.mark.asyncio
async def test_memory_creation_and_attributes(async_client: AsyncClient) -> None:
    headers, user_id = await create_test_user(async_client)

    payload = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Favorite Beverage",
        "predicate": "prefers",
        "value_text": "Green tea without sugar",
        "value_json": {"temp": "hot", "frequency": "daily"},
        "importance": 0.8,
        "sensitivity": "LOW",
    }
    res = await async_client.post("/api/v1/memories", headers=headers, json=payload)
    assert res.status_code == 201
    data = res.json()["data"]

    assert data["memory_type"] == "PERSONAL_FACT"
    assert data["subject"] == "Favorite Beverage"
    assert data["predicate"] == "prefers"
    assert data["value_text"] == "Green tea without sugar"
    assert data["value_json"] == {"temp": "hot", "frequency": "daily"}
    assert data["importance"] == 0.8
    assert data["confidence"] == 1.0
    assert data["sensitivity"] == "LOW"
    assert data["source_type"] == "USER_EXPLICIT"
    assert data["status"] == "ACTIVE"
    assert data["project_id"] is None
    assert data["summary"] == "Favorite Beverage: prefers -> Green tea without sugar"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_all_10_canonical_memory_types(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client)
    proj_id = await create_test_project(async_client, headers, "Canonical Types Proj")

    canonical_types = [
        ("PERSONAL_FACT", None),
        ("PREFERENCE", None),
        ("INTEREST", None),
        ("SKILL", None),
        ("GOAL", None),
        ("BEHAVIOR_PATTERN", None),
        ("PROJECT_FACT", proj_id),
        ("PROJECT_DECISION", proj_id),
        ("PROJECT_PROGRESS", proj_id),
        ("PROJECT_NEXT_ACTION", proj_id),
    ]

    for m_type, p_id in canonical_types:
        payload = {
            "memory_type": m_type,
            "project_id": p_id,
            "subject": f"Subj for {m_type}",
            "predicate": "has_type",
            "value_text": f"Val for {m_type}",
        }
        res = await async_client.post("/api/v1/memories", headers=headers, json=payload)
        assert res.status_code == 201, f"Failed for canonical type: {m_type}, response: {res.text}"

    # Invalid / generic types MUST be rejected with 422
    for forbidden in ["FACT", "NOTE", "DECISION", "CONTEXT", "OTHER"]:
        res_bad = await async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": forbidden,
                "subject": "Bad",
                "predicate": "type",
                "value_text": "Invalid",
            },
        )
        assert res_bad.status_code == 422


@pytest.mark.asyncio
async def test_project_memory_scope_invariants(async_client: AsyncClient) -> None:
    headers_a, _ = await create_test_user(async_client, "Scope User A")
    headers_b, _ = await create_test_user(async_client, "Scope User B")
    proj_a = await create_test_project(async_client, headers_a, "Project A")

    # 1. Project type without project_id -> 422
    res_no_proj = await async_client.post(
        "/api/v1/memories",
        headers=headers_a,
        json={
            "memory_type": "PROJECT_FACT",
            "subject": "Scope Test",
            "predicate": "lacks",
            "value_text": "Missing project_id",
        },
    )
    assert res_no_proj.status_code == 422

    # 2. Personal type with project_id -> 422
    res_personal_with_proj = await async_client.post(
        "/api/v1/memories",
        headers=headers_a,
        json={
            "memory_type": "PERSONAL_FACT",
            "project_id": proj_a,
            "subject": "Scope Test",
            "predicate": "has_unneeded",
            "value_text": "Has project_id",
        },
    )
    assert res_personal_with_proj.status_code == 422

    # 3. Project type with another user's project_id -> 404 safe IDOR
    res_cross_tenant = await async_client.post(
        "/api/v1/memories",
        headers=headers_b,
        json={
            "memory_type": "PROJECT_DECISION",
            "project_id": proj_a,
            "subject": "Attack",
            "predicate": "attempt",
            "value_text": "Cross-tenant attach",
        },
    )
    assert res_cross_tenant.status_code == 404
    assert res_cross_tenant.json()["error"]["code"] == "PROJECT_NOT_FOUND"


@pytest.mark.asyncio
async def test_never_store_secret_safety_policy(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client)

    secret_payloads: list[dict[str, Any]] = [
        {"value_text": "My root password is: SuperSecretPassword123!"},
        {"value_text": "sk-proj-abc123456789012345678901234567890"},
        {"value_text": "ghp_1234567890abcdefghijklmnopqrstuvwxyz"},
        {"value_text": "AKIAIOSFODNN7EXAMPLE"},
        {"value_text": "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0..."},
        {
            "value_text": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.doNotStore"
        },
        {"value_text": "Here is the OTP code is 987654 for verification"},
        {
            "value_text": "Seed phrase: apple banana cherry dog elephant fox grape horse igloo jack kite lion"
        },
        {"value_text": "Benign text", "value_json": {"db_password": "nested_secret_val_123"}},
    ]

    for p in secret_payloads:
        body = {
            "memory_type": "PERSONAL_FACT",
            "subject": "Credentials",
            "predicate": "holds",
            **p,
        }
        res = await async_client.post("/api/v1/memories", headers=headers, json=body)
        assert res.status_code == 400, f"Payload should have been rejected: {p}"
        err = res.json()["error"]
        assert err["code"] == "MEMORY_SECRET_REJECTED"
        # Secret content must NEVER be echoed back in error response
        val_text = p.get("value_text")
        if isinstance(val_text, str):
            assert val_text not in res.text

    # Benign text about security concepts MUST pass without false positives
    benign_body = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Architecture Knowledge",
        "predicate": "notes",
        "value_text": "We discussed how passwords and API tokens should be stored using a dedicated secrets manager.",
        "sensitivity": "RESTRICTED",
    }
    res_benign = await async_client.post("/api/v1/memories", headers=headers, json=benign_body)
    assert res_benign.status_code == 201
    assert res_benign.json()["data"]["sensitivity"] == "RESTRICTED"


@pytest.mark.asyncio
async def test_pre_validation_secret_redaction(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client)

    fake_secret = "sk-fake-secret-that-must-never-be-echoed-back-12345"
    # Construct a request that fails Pydantic validation (invalid memory_type)
    # while carrying candidate secret strings
    bad_payload = {
        "memory_type": "INVALID_TYPE",
        "subject": fake_secret,
        "predicate": "test",
        "value_text": "some text",
    }
    res = await async_client.post("/api/v1/memories", headers=headers, json=bad_payload)
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"
    # Crucial security guarantee: raw inputs must NOT be reflected in 422 details
    assert fake_secret not in res.text


@pytest.mark.asyncio
async def test_deterministic_deduplication(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client)

    payload = {
        "memory_type": "PREFERENCE",
        "subject": "Editor Theme",
        "predicate": "uses",
        "value_text": "Tokyo Night",
    }

    res1 = await async_client.post("/api/v1/memories", headers=headers, json=payload)
    assert res1.status_code == 201
    mem1 = res1.json()["data"]

    # Submit same identity and value with differing whitespace and casing
    payload2 = {
        "memory_type": "PREFERENCE",
        "subject": "  editor theme  ",
        "predicate": "USES ",
        "value_text": "Tokyo Night",
    }
    res2 = await async_client.post("/api/v1/memories", headers=headers, json=payload2)
    assert res2.status_code == 201
    mem2 = res2.json()["data"]

    # Must be deduplicated to the exact same memory ID
    assert mem1["id"] == mem2["id"]


@pytest.mark.asyncio
async def test_conflict_and_supersede(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client)

    payload_old = {
        "memory_type": "PREFERENCE",
        "subject": "Primary Language",
        "predicate": "prefers",
        "value_text": "Python 3.11",
    }
    res_old = await async_client.post("/api/v1/memories", headers=headers, json=payload_old)
    assert res_old.status_code == 201
    old_id = res_old.json()["data"]["id"]

    # New value for same subject + predicate
    payload_new = {
        "memory_type": "PREFERENCE",
        "subject": "Primary Language",
        "predicate": "prefers",
        "value_text": "Python 3.12",
    }
    res_new = await async_client.post("/api/v1/memories", headers=headers, json=payload_new)
    assert res_new.status_code == 201
    new_id = res_new.json()["data"]["id"]
    assert new_id != old_id

    # Old memory must now be SUPERSEDED and reference new_id
    res_get_old = await async_client.get(f"/api/v1/memories/{old_id}", headers=headers)
    assert res_get_old.status_code == 200
    old_mem = res_get_old.json()["data"]
    assert old_mem["status"] == "SUPERSEDED"
    assert old_mem["superseded_by"] == new_id

    # Active listing shows only new memory
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    assert res_list.status_code == 200
    active_ids = [m["id"] for m in res_list.json()["data"]]
    assert new_id in active_ids
    assert old_id not in active_ids


@pytest.mark.asyncio
async def test_concurrent_identical_writes(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Concurrent User")

    payload = {
        "memory_type": "GOAL",
        "subject": "Nexus Phase 1",
        "predicate": "target",
        "value_text": "Complete all 14 milestones",
    }

    # Execute 5 concurrent posts
    tasks = [async_client.post("/api/v1/memories", headers=headers, json=payload) for _ in range(5)]
    responses = await asyncio.gather(*tasks)

    for r in responses:
        assert r.status_code == 201

    ids = {r.json()["data"]["id"] for r in responses}
    # Exactly one deduplicated memory row created
    assert len(ids) == 1


@pytest.mark.asyncio
async def test_concurrent_conflicting_writes(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Concurrent Conflict User")

    values = ["Novice Level", "Intermediate Level", "Expert Level"]

    # Execute concurrent posts with same identity but different values
    tasks = [
        async_client.post(
            "/api/v1/memories",
            headers=headers,
            json={
                "memory_type": "SKILL",
                "subject": "Rust Concurrency",
                "predicate": "proficiency",
                "value_text": val,
            },
        )
        for val in values
    ]
    responses = await asyncio.gather(*tasks)

    for r in responses:
        assert r.status_code == 201

    created_ids = [r.json()["data"]["id"] for r in responses]
    assert len(set(created_ids)) == 3

    # In database, exactly ONE row must remain ACTIVE, others SUPERSEDED
    async with async_session_factory() as session:
        stmt = select(Memory).where(Memory.id.in_([uuid.UUID(i) for i in created_ids]))
        rows = list((await session.execute(stmt)).scalars().all())
        active_rows = [r for r in rows if r.status == MemoryStatus.ACTIVE.value]
        superseded_rows = [r for r in rows if r.status == MemoryStatus.SUPERSEDED.value]

        assert len(active_rows) == 1, f"Expected exactly 1 ACTIVE row, got {len(active_rows)}"
        assert len(superseded_rows) == 2, f"Expected 2 SUPERSEDED rows, got {len(superseded_rows)}"
        for s in superseded_rows:
            assert s.superseded_by is not None


@pytest.mark.asyncio
async def test_expired_reassertion_and_status_coherence(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client, "Expired User")

    past_date = (datetime.now(UTC) - timedelta(hours=2)).isoformat()
    future_date = (datetime.now(UTC) + timedelta(days=7)).isoformat()

    # 1. Create a memory with past expiration
    payload_expired = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Temporary Location",
        "predicate": "staying_at",
        "value_text": "Airport Lounge",
        "expires_at": past_date,
    }
    res1 = await async_client.post("/api/v1/memories", headers=headers, json=payload_expired)
    assert res1.status_code == 201
    old_id = res1.json()["data"]["id"]

    # 2. Reassert the same fact with new future expiration
    payload_reassert = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Temporary Location",
        "predicate": "staying_at",
        "value_text": "Airport Lounge",
        "expires_at": future_date,
    }
    res2 = await async_client.post("/api/v1/memories", headers=headers, json=payload_reassert)
    assert res2.status_code == 201
    new_id = res2.json()["data"]["id"]

    # Reassertion of expired memory MUST create a new ACTIVE memory rather than returning expired row
    assert new_id != old_id

    # Old memory should now be recognized as EXPIRED
    res_get_old = await async_client.get(f"/api/v1/memories/{old_id}", headers=headers)
    assert res_get_old.status_code == 200
    assert res_get_old.json()["data"]["status"] == "EXPIRED"

    # Listing with status=EXPIRED must include old_id
    res_expired_list = await async_client.get("/api/v1/memories?status=EXPIRED", headers=headers)
    assert res_expired_list.status_code == 200
    expired_ids = [m["id"] for m in res_expired_list.json()["data"]]
    assert old_id in expired_ids
    assert new_id not in expired_ids


@pytest.mark.asyncio
async def test_typed_query_filters(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client)

    # Invalid status filter -> 422
    res_bad_status = await async_client.get(
        "/api/v1/memories?status=INVALID_STATUS", headers=headers
    )
    assert res_bad_status.status_code == 422

    # Invalid memory_type filter -> 422
    res_bad_type = await async_client.get("/api/v1/memories?memory_type=NOTE", headers=headers)
    assert res_bad_type.status_code == 422

    # Valid status filter -> 200
    res_ok = await async_client.get("/api/v1/memories?status=ACTIVE", headers=headers)
    assert res_ok.status_code == 200


@pytest.mark.asyncio
async def test_patch_nullable_semantics_and_stale_embedding_prevention(
    async_client: AsyncClient,
) -> None:
    headers, _ = await create_test_user(async_client)
    set_embedding_provider(DeterministicTestEmbeddingProvider(dimension=1536))

    # 1. Create memory with test provider configured
    future_date = (datetime.now(UTC) + timedelta(days=5)).isoformat()
    res = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "SKILL",
            "subject": "Swift Concurrency",
            "predicate": "level",
            "value_text": "Intermediate",
            "value_json": {"verified": True},
            "expires_at": future_date,
            "importance": 0.5,
        },
    )
    assert res.status_code == 201
    mem_id = res.json()["data"]["id"]

    # 2. Disable provider to simulate embedding unavailability during PATCH
    reset_embedding_provider()

    # 3. PATCH value_text while provider is unavailable
    res_patch = await async_client.patch(
        f"/api/v1/memories/{mem_id}",
        headers=headers,
        json={"value_text": "Advanced Expert"},
    )
    assert res_patch.status_code == 200
    patched = res_patch.json()["data"]
    assert patched["value_text"] == "Advanced Expert"
    assert patched["summary"] == "Swift Concurrency: level -> Advanced Expert"

    # Verify in DB: embedding must be NULL, NOT retaining the stale vector
    async with async_session_factory() as session:
        mem = await session.get(Memory, uuid.UUID(mem_id))
        assert mem is not None
        assert mem.embedding is None, "Embedding must be NULL to prevent stale vector retention"

    # 4. Null-clear semantics: PATCH with null value_json and expires_at
    res_clear = await async_client.patch(
        f"/api/v1/memories/{mem_id}",
        headers=headers,
        json={"value_json": None, "expires_at": None},
    )
    assert res_clear.status_code == 200
    cleared = res_clear.json()["data"]
    assert cleared["value_json"] is None
    assert cleared["expires_at"] is None

    # 5. Empty PATCH preserves existing values
    res_empty = await async_client.patch(f"/api/v1/memories/{mem_id}", headers=headers, json={})
    assert res_empty.status_code == 200


@pytest.mark.asyncio
async def test_forget_memory_semantics(async_client: AsyncClient) -> None:
    headers, _ = await create_test_user(async_client)

    res = await async_client.post(
        "/api/v1/memories",
        headers=headers,
        json={
            "memory_type": "PERSONAL_FACT",
            "subject": "Old Pet",
            "predicate": "name",
            "value_text": "Rex",
        },
    )
    assert res.status_code == 201
    mem_id = res.json()["data"]["id"]

    # Forget memory
    res_forget = await async_client.post(f"/api/v1/memories/{mem_id}/forget", headers=headers)
    assert res_forget.status_code == 200
    forget_data = res_forget.json()["data"]
    assert forget_data["status"] == "FORGOTTEN"
    assert "forgotten_at" in forget_data

    # Idempotent: repeating forget returns same response
    res_repeat = await async_client.post(f"/api/v1/memories/{mem_id}/forget", headers=headers)
    assert res_repeat.status_code == 200
    assert res_repeat.json()["data"]["status"] == "FORGOTTEN"

    # Excluded from active listings
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    assert res_list.status_code == 200
    assert not any(m["id"] == mem_id for m in res_list.json()["data"])


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
        f"\n[M3 Observed Local Baseline Benchmark]\n"
        f"  Create: {create_duration_ms:.2f}ms\n"
        f"  Dedup:  {dedup_duration_ms:.2f}ms\n"
        f"  List:   {list_duration_ms:.2f}ms\n"
        f"  Search: {search_duration_ms:.2f}ms\n"
        f"  Forget: {forget_duration_ms:.2f}ms\n"
    )

    # NON-PRODUCTION REGRESSION GUARD: Broad sanity check (< 2000ms) to prevent CI flakiness
    assert create_duration_ms < 2000
    assert dedup_duration_ms < 2000
    assert list_duration_ms < 2000
    assert search_duration_ms < 2000
    assert forget_duration_ms < 2000


@pytest.mark.asyncio
async def test_embedding_vector_validation_boundary() -> None:
    """Verify runtime validation boundary for vector emptiness, finiteness, and dimension."""
    from app.domains.memories.embedding import (
        DeterministicTestEmbeddingProvider,
        UnavailableEmbeddingProvider,
        validate_embedding_vector,
    )
    from app.domains.memories.exceptions import (
        EmbeddingUnavailableError,
        EmbeddingValidationError,
    )

    # 1. Empty and None vectors rejected
    with pytest.raises(EmbeddingValidationError, match="Embedding vector is empty"):
        validate_embedding_vector([])

    with pytest.raises(EmbeddingValidationError, match="Embedding vector is empty"):
        validate_embedding_vector(None)

    # 2. Non-finite values (NaN, +Inf, -Inf) rejected
    with pytest.raises(EmbeddingValidationError, match="non-finite or invalid numeric value"):
        validate_embedding_vector([1.0, float("nan"), 0.5])

    with pytest.raises(EmbeddingValidationError, match="non-finite or invalid numeric value"):
        validate_embedding_vector([1.0, float("inf"), 0.5])

    with pytest.raises(EmbeddingValidationError, match="non-finite or invalid numeric value"):
        validate_embedding_vector([1.0, float("-inf"), 0.5])

    # 3. Dimension mismatch rejected without leaking raw vector elements
    with pytest.raises(EmbeddingValidationError) as exc_info:
        validate_embedding_vector([0.1, 0.2, 0.3], expected_dim=4)
    assert "expected 4, got 3" in str(exc_info.value)
    assert "0.1" not in str(exc_info.value)

    # 4. Valid vector accepted
    valid_vec = [0.1, 0.2, 0.3, 0.4]
    result = validate_embedding_vector(valid_vec, expected_dim=4)
    assert result == valid_vec

    # 5. Provider protocol dimension property
    test_provider = DeterministicTestEmbeddingProvider(dimension=768)
    assert test_provider.dimension == 768

    unavailable_provider = UnavailableEmbeddingProvider()
    with pytest.raises(EmbeddingUnavailableError, match="TBD-004"):
        _ = unavailable_provider.dimension


@pytest.mark.asyncio
async def test_memory_payload_size_and_json_safety_bounds(async_client: AsyncClient) -> None:
    """Verify strict length bounds on value_text and serialized size/depth bounds on value_json."""
    headers, _ = await create_test_user(async_client, "PayloadBoundaryTester")

    # 1. value_text exactly 10,000 characters accepted
    payload_exact_max = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Max Payload",
        "predicate": "has_exact_max_chars",
        "value_text": "a" * 10000,
    }
    res_exact = await async_client.post("/api/v1/memories", headers=headers, json=payload_exact_max)
    assert res_exact.status_code == 201

    # 2. value_text 10,001 characters rejected with 422
    payload_over_max = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Over Max",
        "predicate": "has_over_max_chars",
        "value_text": "b" * 10001,
    }
    res_over = await async_client.post("/api/v1/memories", headers=headers, json=payload_over_max)
    assert res_over.status_code == 422
    # Ensure rejected long payload is not reflected in error response details
    assert "b" * 10001 not in res_over.text

    # 3. Oversized value_json (> 64KB) rejected with 422
    payload_oversized_json = {
        "memory_type": "PERSONAL_FACT",
        "subject": "JSON Bound",
        "predicate": "has_oversized_json",
        "value_text": "Valid text with oversized metadata",
        "value_json": {"data": "c" * 70000},
    }
    res_oversized = await async_client.post(
        "/api/v1/memories", headers=headers, json=payload_oversized_json
    )
    assert res_oversized.status_code == 422
    assert "c" * 70000 not in res_oversized.text

    # 4. Deeply nested value_json (> depth 5) rejected with 422
    payload_deep_json = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Depth Bound",
        "predicate": "has_deep_json",
        "value_text": "Valid text with deep nesting",
        "value_json": {"l1": {"l2": {"l3": {"l4": {"l5": {"l6": "too deep"}}}}}},
    }
    res_deep = await async_client.post("/api/v1/memories", headers=headers, json=payload_deep_json)
    assert res_deep.status_code == 422

    # 5. Ordinary well-structured value_json accepted
    payload_valid_json = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Valid JSON",
        "predicate": "has_normal_json",
        "value_text": "Valid text with normal metadata",
        "value_json": {"theme": "dark", "fontSize": 14, "tags": ["ui", "editor"]},
    }
    res_valid = await async_client.post(
        "/api/v1/memories", headers=headers, json=payload_valid_json
    )
    assert res_valid.status_code == 201
    assert res_valid.json()["data"]["value_json"]["theme"] == "dark"


@pytest.mark.asyncio
async def test_unicode_deterministic_identity(async_client: AsyncClient) -> None:
    """Verify canonically equivalent Unicode strings deduplicate to the same ACTIVE memory."""
    headers, _ = await create_test_user(async_client, "UnicodeTester")

    # Subject A: "Café" using precomposed character (U+00E9)
    subject_precomposed = "Café"
    # Subject B: "Café" using decomposed base letter 'e' + combining acute accent (U+0301)
    subject_decomposed = "Café"

    assert subject_precomposed != subject_decomposed  # Raw strings differ in code points

    # 1. Post precomposed memory
    payload_a = {
        "memory_type": "PERSONAL_FACT",
        "subject": subject_precomposed,
        "predicate": "drinks",
        "value_text": "Single Espresso",
    }
    res_a = await async_client.post("/api/v1/memories", headers=headers, json=payload_a)
    assert res_a.status_code == 201
    mem_id_a = res_a.json()["data"]["id"]

    # 2. Post decomposed memory with identical value -> MUST deduplicate to the same row
    payload_b = {
        "memory_type": "PERSONAL_FACT",
        "subject": subject_decomposed,
        "predicate": "drinks",
        "value_text": "Single Espresso",
    }
    res_b = await async_client.post("/api/v1/memories", headers=headers, json=payload_b)
    assert res_b.status_code == 201
    mem_id_b = res_b.json()["data"]["id"]
    assert mem_id_a == mem_id_b, (
        "Canonically equivalent Unicode subjects must resolve to the same memory"
    )

    # Verify query listing has exactly 1 ACTIVE memory
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    assert res_list.status_code == 200
    assert len(res_list.json()["data"]) == 1
    assert res_list.json()["meta"]["total"] == 1

    # 3. Post decomposed memory with conflicting value -> MUST supersede existing memory
    payload_conflict = {
        "memory_type": "PERSONAL_FACT",
        "subject": subject_decomposed,
        "predicate": "drinks",
        "value_text": "Double Espresso",
    }
    res_c = await async_client.post("/api/v1/memories", headers=headers, json=payload_conflict)
    assert res_c.status_code == 201
    mem_id_c = res_c.json()["data"]["id"]
    assert mem_id_c != mem_id_a

    # Check original memory is superseded
    res_old = await async_client.get(f"/api/v1/memories/{mem_id_a}", headers=headers)
    assert res_old.status_code == 200
    assert res_old.json()["data"]["status"] == "SUPERSEDED"
    assert res_old.json()["data"]["superseded_by"] == mem_id_c

    # 4. Post different Unicode subject ("Kaffee") -> MUST create separate distinct identity
    payload_diff = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Kaffee",
        "predicate": "drinks",
        "value_text": "Single Espresso",
    }
    res_d = await async_client.post("/api/v1/memories", headers=headers, json=payload_diff)
    assert res_d.status_code == 201
    mem_id_d = res_d.json()["data"]["id"]
    assert mem_id_d != mem_id_c


@pytest.mark.asyncio
async def test_mixed_dimension_safety_in_semantic_search(async_client: AsyncClient) -> None:
    """Verify semantic search safely filters out vectors of mismatched dimensions without database error."""
    headers, _ = await create_test_user(async_client, "DimensionSafetyTester")

    # 1. Seed a memory with 512-dimensional embedding
    set_embedding_provider(DeterministicTestEmbeddingProvider(dimension=512))
    payload_512 = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Dim512 Fact",
        "predicate": "stored_dim",
        "value_text": "Stored with 512 dimensions",
    }
    res_create = await async_client.post("/api/v1/memories", headers=headers, json=payload_512)
    assert res_create.status_code == 201

    # 2. Switch provider to 256-dimensional embedding
    set_embedding_provider(DeterministicTestEmbeddingProvider(dimension=256))

    # 3. Perform semantic search: query vector is 256-dim; stored memory is 512-dim.
    # PostgreSQL vector_dims filter MUST exclude 512-dim row so no <=> dimension mismatch error occurs.
    res_search = await async_client.post(
        "/api/v1/memories/search",
        headers=headers,
        json={"query": "Stored with 512 dimensions"},
    )
    assert res_search.status_code == 200
    hits = res_search.json()["data"]
    # 512-dim item was safely excluded, 0 hits returned without error
    assert len(hits) == 0

    # 4. Seed a new memory with the currently active 256-dim provider
    payload_256 = {
        "memory_type": "PERSONAL_FACT",
        "subject": "Dim256 Fact",
        "predicate": "stored_dim",
        "value_text": "Stored with matching 256 dimensions",
    }
    res_256 = await async_client.post("/api/v1/memories", headers=headers, json=payload_256)
    assert res_256.status_code == 201

    # 5. Search again: matching 256-dim memory is retrieved
    res_search_match = await async_client.post(
        "/api/v1/memories/search",
        headers=headers,
        json={"query": "Stored with matching 256 dimensions"},
    )
    assert res_search_match.status_code == 200
    hits_match = res_search_match.json()["data"]
    assert len(hits_match) == 1
    assert hits_match[0]["subject"] == "Dim256 Fact"

    # Reset to default provider
    reset_embedding_provider()


@pytest.mark.asyncio
async def test_unicode_normalization_expansion_safety(async_client: AsyncClient) -> None:
    """Verify that Unicode inputs whose NFKD normalization expands beyond 255 chars

    do not overflow database storage and preserve deterministic deduplication.
    """
    import unicodedata

    headers, _ = await create_test_user(async_client, "ExpansionTester")

    # Subject with composed accented characters: exactly 255 characters long.
    # Each 'é' (U+00E9) decomposes under NFKD into 'e' (U+0065) + combining acute accent (U+0301).
    # Raw length is 255 chars, but NFKD decomposed length is 510 chars!
    subject_composed = "é" * 255
    assert len(subject_composed) == 255

    subject_decomposed = unicodedata.normalize("NFKD", subject_composed)
    assert len(subject_decomposed) == 510  # Would overflow a VARCHAR(255) column

    # 1. Post composed memory (valid length <= 255)
    payload_a = {
        "memory_type": "PERSONAL_FACT",
        "subject": subject_composed,
        "predicate": "expanded_key",
        "value_text": "Accent expansion test value",
    }
    res_a = await async_client.post("/api/v1/memories", headers=headers, json=payload_a)
    assert res_a.status_code == 201, (
        f"Expected 201 Created but got {res_a.status_code}: {res_a.text}"
    )
    mem_id_a = res_a.json()["data"]["id"]

    # 2. Re-assert memory using identical value but composed vs decomposed forms within 255 raw chars:
    # A subject of 100 decomposed characters (100 'é' = 200 code points, within 255 raw length):
    subject_100_composed = "é" * 100
    subject_100_decomposed = unicodedata.normalize("NFKD", subject_100_composed)
    assert len(subject_100_composed) == 100
    assert len(subject_100_decomposed) == 200  # Valid raw input <= 255, decomposed = 200

    payload_100_comp = {
        "memory_type": "PERSONAL_FACT",
        "subject": subject_100_composed,
        "predicate": "key_100",
        "value_text": "Decomposed equivalence test",
    }
    res_100_a = await async_client.post("/api/v1/memories", headers=headers, json=payload_100_comp)
    assert res_100_a.status_code == 201
    id_100_a = res_100_a.json()["data"]["id"]

    payload_100_decomp = {
        "memory_type": "PERSONAL_FACT",
        "subject": subject_100_decomposed,
        "predicate": "key_100",
        "value_text": "Decomposed equivalence test",
    }
    res_100_b = await async_client.post(
        "/api/v1/memories", headers=headers, json=payload_100_decomp
    )
    assert res_100_b.status_code == 201
    id_100_b = res_100_b.json()["data"]["id"]
    assert id_100_a == id_100_b, "Composed and decomposed forms must resolve to the same memory ID"

    # 3. Re-posting the 255-char composed memory deduplicates cleanly
    res_repost = await async_client.post("/api/v1/memories", headers=headers, json=payload_a)
    assert res_repost.status_code == 201
    assert res_repost.json()["data"]["id"] == mem_id_a

    # 4. Verify listing has exactly 2 active memories (the 255-char one and the 100-char one)
    res_list = await async_client.get("/api/v1/memories", headers=headers)
    assert res_list.status_code == 200
    assert res_list.json()["meta"]["total"] == 2

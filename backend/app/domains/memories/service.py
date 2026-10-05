import logging
import unicodedata
import uuid

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.memories.embedding import get_embedding_provider
from app.domains.memories.exceptions import (
    EmbeddingUnavailableError,
    MemoryInvalidStateError,
    MemoryNotFoundError,
)
from app.domains.memories.models import (
    Memory,
    MemorySourceType,
    MemoryStatus,
    utc_now,
)
from app.domains.memories.safety import MemorySafetyPolicy
from app.domains.memories.schemas import MemoryCreate, MemorySearchHit, MemoryUpdate
from app.domains.projects.exceptions import ProjectNotFoundError
from app.domains.projects.models import Project
from app.domains.users.models import User

logger = logging.getLogger(__name__)


def normalize_key(text: str) -> str:
    """Normalize subject or predicate for deterministic identity matching."""
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.strip().lower()


def derive_summary(subject: str, predicate: str, value_text: str, max_chars: int = 500) -> str:
    """Derive deterministic structured summary without LLM dependency."""
    raw = f"{subject.strip()}: {predicate.strip()} -> {value_text.strip()}"
    if len(raw) <= max_chars:
        return raw
    return raw[: max_chars - 3] + "..."


class MemoryService:
    """Service managing Memory lifecycle, deterministic deduplication, superseding, safety, and search."""

    @staticmethod
    async def create_memory(
        db: AsyncSession,
        user_id: uuid.UUID,
        data: MemoryCreate,
    ) -> Memory:
        """Create a new memory or return existing on duplicate, superseding old on conflict."""
        # 1. Enforce NEVER_STORE secret safety policy before any persistence
        MemorySafetyPolicy.validate(
            subject=data.subject,
            predicate=data.predicate,
            value_text=data.value_text,
            value_json=data.value_json,
        )

        # 2. Enforce Project ownership invariants if project_id is supplied
        if data.project_id is not None:
            stmt = select(Project.id).where(
                Project.id == data.project_id,
                Project.user_id == user_id,
            )
            project_exists = (await db.execute(stmt)).scalar_one_or_none()
            if not project_exists:
                raise ProjectNotFoundError("Project not found.")

        # 3. Acquire user row lock to serialize concurrent memory writes for this user
        await db.execute(select(User.id).where(User.id == user_id).with_for_update())

        norm_subject = normalize_key(data.subject)
        norm_predicate = normalize_key(data.predicate)
        norm_value = data.value_text.strip()

        # 4. Check for existing ACTIVE memory with identical deterministic identity
        lookup_stmt = select(Memory).where(
            Memory.user_id == user_id,
            Memory.project_id == data.project_id,
            Memory.memory_type == data.memory_type.value,
            func.lower(func.trim(Memory.subject)) == norm_subject,
            func.lower(func.trim(Memory.predicate)) == norm_predicate,
            Memory.status == MemoryStatus.ACTIVE.value,
        )
        existing = (await db.execute(lookup_stmt)).scalars().first()

        now = utc_now()

        # 5. Handle Exact Deduplication: same identity + same normalized value
        if existing is not None:
            existing_val = existing.value_text.strip()
            if existing_val == norm_value and existing.value_json == data.value_json:
                logger.info(
                    "memory_deduplicated",
                    extra={"memory_id": str(existing.id), "user_id": str(user_id)},
                )
                return existing

        # 6. Generate summary & attempt embedding generation
        summary = derive_summary(data.subject, data.predicate, data.value_text)
        embedding_vector: list[float] | None = None
        try:
            provider = get_embedding_provider()
            embedding_vector = await provider.embed(data.value_text)
        except EmbeddingUnavailableError:
            embedding_vector = None

        new_memory = Memory(
            user_id=user_id,
            project_id=data.project_id,
            memory_type=data.memory_type.value,
            subject=data.subject.strip(),
            predicate=data.predicate.strip(),
            value_text=data.value_text.strip(),
            value_json=data.value_json,
            summary=summary,
            embedding=embedding_vector,
            importance=data.importance,
            confidence=1.0,  # USER_EXPLICIT manual creation baseline
            sensitivity=data.sensitivity.value,
            source_type=MemorySourceType.USER_EXPLICIT.value,
            status=MemoryStatus.ACTIVE.value,
            expires_at=data.expires_at,
            created_at=now,
            updated_at=now,
        )

        db.add(new_memory)
        await db.flush()

        # 7. Handle Conflict / Supersede: old ACTIVE becomes SUPERSEDED by new memory
        if existing is not None:
            existing.status = MemoryStatus.SUPERSEDED.value
            existing.superseded_by = new_memory.id
            existing.updated_at = now
            await db.flush()
            logger.info(
                "memory_superseded",
                extra={
                    "old_id": str(existing.id),
                    "new_id": str(new_memory.id),
                    "user_id": str(user_id),
                },
            )
        else:
            logger.info(
                "memory_created",
                extra={"memory_id": str(new_memory.id), "user_id": str(user_id)},
            )

        return new_memory

    @staticmethod
    async def get_memory(
        db: AsyncSession,
        user_id: uuid.UUID,
        memory_id: uuid.UUID,
    ) -> Memory:
        """Fetch memory with strict user-tenant scoping."""
        stmt = select(Memory).where(Memory.id == memory_id, Memory.user_id == user_id)
        memory = (await db.execute(stmt)).scalar_one_or_none()
        if not memory:
            raise MemoryNotFoundError("Memory not found.")
        return memory

    @staticmethod
    async def list_memories(
        db: AsyncSession,
        user_id: uuid.UUID,
        status: str | None = None,
        project_id: uuid.UUID | None = None,
        memory_type: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Memory], int]:
        """List caller-owned memories with bounded pagination and safe expiration filtering."""
        bounded_limit = max(1, min(limit, 100))
        offset = max(0, (page - 1) * bounded_limit)
        now = utc_now()

        conditions = [Memory.user_id == user_id]

        if status is not None:
            conditions.append(Memory.status == status)
            if status == MemoryStatus.ACTIVE.value:
                # Exclude expired memories even if lazy normalization has not executed
                conditions.append(or_(Memory.expires_at.is_(None), Memory.expires_at > now))
        else:
            # Default behavior: prioritize currently usable ACTIVE, non-expired memories
            conditions.append(Memory.status == MemoryStatus.ACTIVE.value)
            conditions.append(or_(Memory.expires_at.is_(None), Memory.expires_at > now))

        if project_id is not None:
            conditions.append(Memory.project_id == project_id)

        if memory_type is not None:
            conditions.append(Memory.memory_type == memory_type)

        count_stmt = select(func.count(Memory.id)).where(and_(*conditions))
        total = (await db.execute(count_stmt)).scalar() or 0

        query = (
            select(Memory)
            .where(and_(*conditions))
            .order_by(Memory.updated_at.desc(), Memory.created_at.desc())
            .offset(offset)
            .limit(bounded_limit)
        )
        items = list((await db.execute(query)).scalars().all())
        return items, total

    @staticmethod
    async def update_memory(
        db: AsyncSession,
        user_id: uuid.UUID,
        memory_id: uuid.UUID,
        data: MemoryUpdate,
    ) -> Memory:
        """Update mutable fields of an active memory."""
        await db.execute(select(User.id).where(User.id == user_id).with_for_update())

        memory = await MemoryService.get_memory(db, user_id, memory_id)

        # Reject mutation on terminal lifecycle states
        if memory.status in (
            MemoryStatus.FORGOTTEN.value,
            MemoryStatus.SUPERSEDED.value,
            MemoryStatus.EXPIRED.value,
        ):
            raise MemoryInvalidStateError(
                f"Cannot update memory with terminal status '{memory.status}'."
            )

        now = utc_now()
        if memory.expires_at and memory.expires_at <= now:
            raise MemoryInvalidStateError("Cannot update expired memory.")

        # Safety policy scan on updated values
        target_val = data.value_text if data.value_text is not None else memory.value_text
        target_json = data.value_json if data.value_json is not None else memory.value_json
        MemorySafetyPolicy.validate(
            subject=memory.subject,
            predicate=memory.predicate,
            value_text=target_val,
            value_json=target_json,
        )

        if data.value_text is not None:
            memory.value_text = data.value_text.strip()
            memory.summary = derive_summary(memory.subject, memory.predicate, memory.value_text)
            try:
                provider = get_embedding_provider()
                memory.embedding = await provider.embed(memory.value_text)
            except EmbeddingUnavailableError:
                pass

        if data.value_json is not None:
            memory.value_json = data.value_json

        if data.importance is not None:
            memory.importance = data.importance

        if data.sensitivity is not None:
            memory.sensitivity = data.sensitivity.value

        if data.expires_at is not None:
            memory.expires_at = data.expires_at

        memory.updated_at = now
        await db.flush()
        return memory

    @staticmethod
    async def forget_memory(
        db: AsyncSession,
        user_id: uuid.UUID,
        memory_id: uuid.UUID,
    ) -> Memory:
        """Mark memory as FORGOTTEN (idempotent, excluded from retrieval)."""
        await db.execute(select(User.id).where(User.id == user_id).with_for_update())

        memory = await MemoryService.get_memory(db, user_id, memory_id)

        if memory.status == MemoryStatus.FORGOTTEN.value:
            return memory

        now = utc_now()
        memory.status = MemoryStatus.FORGOTTEN.value
        memory.updated_at = now
        await db.flush()

        logger.info(
            "memory_forgotten",
            extra={"memory_id": str(memory.id), "user_id": str(user_id)},
        )
        return memory

    @staticmethod
    async def search_memories(
        db: AsyncSession,
        user_id: uuid.UUID,
        query: str,
        project_id: uuid.UUID | None = None,
        limit: int = 10,
    ) -> list[MemorySearchHit]:
        """Perform semantic search using pgvector cosine similarity scan."""
        # 1. Require embedding provider to generate query vector
        provider = get_embedding_provider()
        query_vector = await provider.embed(query)

        # 2. Verify project ownership if project scope is supplied
        if project_id is not None:
            stmt = select(Project.id).where(
                Project.id == project_id,
                Project.user_id == user_id,
            )
            project_exists = (await db.execute(stmt)).scalar_one_or_none()
            if not project_exists:
                raise ProjectNotFoundError("Project not found.")

        now = utc_now()
        bounded_limit = max(1, min(limit, 50))

        # 3. Exact vector similarity query with strict security predicates
        cosine_distance = Memory.embedding.cosine_distance(query_vector).label("distance")

        conditions = [
            Memory.user_id == user_id,
            Memory.status == MemoryStatus.ACTIVE.value,
            Memory.embedding.is_not(None),
            or_(Memory.expires_at.is_(None), Memory.expires_at > now),
        ]

        if project_id is not None:
            conditions.append(Memory.project_id == project_id)

        search_stmt = (
            select(Memory, cosine_distance)
            .where(and_(*conditions))
            .order_by("distance")
            .limit(bounded_limit)
        )

        rows = (await db.execute(search_stmt)).all()

        hits: list[MemorySearchHit] = []
        for mem, dist in rows:
            # Cosine distance to similarity: similarity = 1.0 - distance
            similarity = max(0.0, min(1.0, 1.0 - float(dist)))
            hits.append(
                MemorySearchHit(
                    id=mem.id,
                    memory_type=mem.memory_type,
                    subject=mem.subject,
                    predicate=mem.predicate,
                    value_text=mem.value_text,
                    summary=mem.summary,
                    project_id=mem.project_id,
                    similarity_score=similarity,
                    created_at=mem.created_at,
                )
            )

        return hits

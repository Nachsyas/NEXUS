# Milestone M2: Deviations & Decisions

## 1. Deviations from Planned Scope
- **None:** The implementation strictly adhered to the approved Milestone M2 plan and scope boundaries.
- **Zero M3+ Scope Creep:** No memory entities, vector embeddings, goal trees, or LLM-dependent functions were introduced. The `/context` endpoint returns deterministic metadata foundation only.

## 2. Technical Adjustments During Implementation
- **SQLAlchemy Attribute Naming:** The database column for technology metadata is named `metadata`. In SQLAlchemy declarative models, `metadata` is a reserved attribute on `Base`. This was resolved cleanly by declaring the model property as `tech_metadata = mapped_column("metadata", JSONB, ...)` and utilizing Pydantic serialization alias `Field(default_factory=dict, alias="tech_metadata")` with `populate_by_name=True`.
- **Async Relationship Loading:** Direct serialization of lazily-loaded relationships in async FastAPI routes triggers SQLAlchemy's `MissingGreenlet` error. This was resolved by declaring `Project.technologies` with `lazy="selectin"` and adding an explicit `selectinload` fetch in `ProjectService` mutation methods before returning entities.

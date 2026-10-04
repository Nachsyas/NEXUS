# ADR-016: uv as Python Package and Environment Manager

**Status:** ACCEPTED  
**Date:** 2026-10-04 (Ratified)  
**Deciders:** User Formal Ratification  
**Resolves:** TBD-013  

> [!NOTE]
> Formally approved and ratified by the User on 2026-10-04. `uv` is the approved Phase 1 Python package/environment management baseline. Any future replacement must follow standard ADR governance and require empirical evidence.

## Context
NEXUS backend requires a fast, reliable, reproducible Python package and environment management tool for Phase 1 local development and CI/CD pipelines.

## Problem
Which Python package and environment manager should NEXUS use for backend development?

## Decision
Adopt **uv** (Astral) as the official Python package and virtual environment manager for NEXUS.
- Standard pyproject.toml configuration.
- Reproducible dependency resolution via `uv.lock`.
- Native Apple Silicon (ARM64) support with ultra-fast execution.

## Alternatives Considered
- *Poetry:* Mature and widely adopted, but slower dependency resolution and higher virtualenv management overhead.
- *pip-tools:* Minimalist, but lacks unified environment management, script execution, and project workspace features.

## Consequences
- Extremely fast environment setup, installs, and dependency locking in local development and CI.
- Requires `uv` installed in developer environments (native Homebrew / standalone installer).

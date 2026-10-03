# ADR-016: uv as Python Package and Environment Manager

**Status:** PROPOSED BY M0 IMPLEMENTATION  
**Date:** 2026-10-03  
**Deciders:** Proposed by M0 Implementation; Pending Formal User Approval  
**Resolves:** TBD-013 (Proposed)  

> [!NOTE]
> This decision represents the working implementation baseline established during Milestone M0. In accordance with NEXUS governance, it is classified as **PROPOSED BY M0 IMPLEMENTATION** pending explicit formal user acceptance.

## Context
NEXUS backend requires a fast, reliable, reproducible Python package and environment management tool for Phase 1 local development and CI/CD pipelines.

## Problem
Which Python package and environment manager should NEXUS use for backend development?

## Proposed Decision
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

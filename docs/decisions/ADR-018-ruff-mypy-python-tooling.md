# ADR-018: Ruff and Mypy for Python Formatting, Linting, and Type-Checking

**Status:** ACCEPTED  
**Date:** 2026-10-03  
**Deciders:** User & Core Engineering Team  
**Resolves:** TBD-015  

## Context
NEXUS backend requires rigorous code quality standards, strict static typing, and automated formatting to ensure maintainability, security, and developer velocity.

## Problem
Which Python linter, formatter, and type-checking suite should be established in NEXUS local development and CI pipelines?

## Decision
Adopt **Ruff** for code formatting and linting, and **Mypy** for strict static type checking.
- Ruff replaces Black, Flake8, isort, and pydocstyle in a single, ultra-fast Rust-based binary.
- Mypy provides deep static type validation across all modules with strict typing enabled.
- Single unified configuration in `pyproject.toml`.

## Alternatives Considered
- *Black + Flake8 + isort + Mypy:* Fragmented multi-tool chain, significantly slower execution in local pre-commit and CI workflows.

## Consequences
- Sub-second linting and formatting feedback loop during local development.
- Strict typing enforced on all backend code before merging.

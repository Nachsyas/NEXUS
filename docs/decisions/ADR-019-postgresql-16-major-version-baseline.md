# ADR-019: PostgreSQL 16 Major Version Baseline with pgvector

**Status:** ACCEPTED  
**Date:** 2026-10-04 (Ratified)  
**Deciders:** User Formal Ratification  
**Resolves:** TBD-026  

> [!NOTE]
> Formally approved and ratified by the User on 2026-10-04. PostgreSQL 16 with compatible pgvector is the approved Phase 1 development/database baseline. This does NOT lock production hosting provider, future PostgreSQL major upgrades, pgvector index strategy, or future database scaling architecture; those remain governed independently.

## Context
NEXUS requires a stable, high-performance relational database with vector search capability (pgvector) for local development, testing, and Phase 1 staging environments.

## Problem
What PostgreSQL major version baseline should be adopted for NEXUS container environments and local development?

## Decision
Adopt **PostgreSQL 16** with official **pgvector** extension support (`pgvector/pgvector:pg16` Docker image) as the baseline database engine for Phase 1.
- Proven operational stability and broad extension compatibility.
- Native Apple Silicon ARM64 container images available.
- Supported by all major managed PostgreSQL cloud providers (AWS RDS/Aurora, GCP Cloud SQL, Supabase, Neon) ensuring future portability without cloud lock-in.

## Alternatives Considered
- *PostgreSQL 17:* Newer release, but some managed service providers have delayed pgvector extension packaging.
- *PostgreSQL 15:* Older release lacking key query optimization improvements present in v16.

## Consequences
- Predictable, standardized database environment for all developers and CI pipelines.
- Upgrades to newer PostgreSQL major versions can follow standard migration paths in later phases.

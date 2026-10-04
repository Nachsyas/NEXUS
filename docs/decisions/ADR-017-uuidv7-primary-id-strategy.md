# ADR-017: UUIDv7 Primary Identifier Strategy

**Status:** ACCEPTED  
**Date:** 2026-10-04 (Ratified)  
**Deciders:** User Formal Ratification  
**Resolves:** TBD-014  

> [!NOTE]
> Formally approved and ratified by the User on 2026-10-04. UUIDv7 (RFC 9562) is the approved primary identifier strategy for NEXUS durable entities unless a specific entity has a documented technical reason to use another identifier. Any exception must be explicit and reviewed.

## Context
NEXUS entities (users, devices, memories, actions, audit logs, sessions, etc.) require unique primary keys that scale well in PostgreSQL, support distributed generation without coordination, and prevent index fragmentation.

## Problem
What is the primary ID generation strategy for NEXUS database entities?

## Decision
Adopt **UUIDv7** (RFC 9562) as the default primary identifier strategy across NEXUS relational database tables.
- Time-ordered 128-bit identifiers with millisecond-precision Unix timestamps in high bits.
- Stored natively in PostgreSQL `UUID` columns (16 bytes).
- Preserves B-tree index insertion locality, preventing page splits and fragmentation typical of random UUIDv4.
- Generatable in client, agent, or backend without database round-trips.

## Alternatives Considered
- *UUIDv4:* Random 128-bit UUIDs cause severe B-tree index fragmentation and random page I/O at scale.
- *ULID:* 128-bit sortable, but non-standard text representation (Crockford Base32) requires conversion for native UUID column storage.
- *Snowflake:* 64-bit integer, but requires central coordination or node ID management.

## Consequences
- High-efficiency indexing and natural chronological sorting for all entity primary keys.
- Requires standard UUIDv7 generator utility in Python and Swift.

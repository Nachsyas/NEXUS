# ADR-003: PostgreSQL as Primary Relational Database

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Sistem membutuhkan penyimpanan data relasional yang andal, mendukung transaksi ACID, integritas referensial, serta kemampuan ekstensi modern.

## Decision
Menetapkan **PostgreSQL** sebagai primary source of truth database (baseline versi major ditentukan via TBD-026 sebelum finalisasi lingkungan M0).

## Consequences
- Seluruh mutasi data penting memiliki jaminan integritas ACID.
- Migrasi skema dikelola melalui Alembic.

# ADR-004: pgvector as Phase 1 Vector Store Baseline

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Fitur Knowledge Vault, Personal Memory, dan Research Radar membutuhkan pencarian semantik berbasis kemiripan vektor embedding.

## Decision
Menggunakan ekstensi **pgvector** langsung di dalam database PostgreSQL untuk Phase 1.

## Alternatives
- *Pinecone / Qdrant Dedicated:* Ditolak untuk Phase 1 guna menghindari penambahan infrastruktur eksternal dan menjaga query tetap berada dalam satu transaksi database lokal.

## Consequences
- Menghemat biaya dan menyederhanakan arsitektur database tanpa komponen vector DB eksternal terpisah.
- Strategi indeks spesifik pgvector dan target performa latensi dievaluasi secara terukur via TBD-025 sebelum benchmark skala produksi pertama.

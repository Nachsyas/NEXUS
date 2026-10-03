# ADR-001: Modular Monolith Architecture for Phase 1 Backend

**Status:** ACCEPTED  
**Date:** 2026-10-03  
**Deciders:** Core Engineering Team  

## Context
NEXUS membutuhkan fondasi backend yang cepat diiterasi, mudah diuji, dan memiliki konsistensi data yang ketat selama Phase 1, sembari mendukung batas domain yang bersih untuk potensi pemisahan di masa depan.

## Problem
Apakah backend Phase 1 harus dibangun menggunakan arsitektur microservices atau modular monolith?

## Decision
Mengadopsi pola **Modular Monolith** berbasis FastAPI di dalam satu codebase backend (`backend/app`). Seluruh domain (auth, memory, context, actions, devices, dll.) diorganisir dalam paket-paket independen dengan isolasi data yang ketat.

## Alternatives
- *Microservices:* Ditolak karena menambah overhead jaringan, kompleksitas deployment lokal, dan latensi antar-service yang belum dibutuhkan pada Phase 1.

## Consequences
- Pengembangan dan deployment lokal menjadi sangat sederhana.
- Batas domain wajib dijaga ketat melalui code review dan linter agar tidak terjadi coupling liar.

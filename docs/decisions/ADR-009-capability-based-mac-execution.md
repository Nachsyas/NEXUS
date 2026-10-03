# ADR-009: Capability-Based Execution on Mac Agent

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Eksekusi remote pada komputer pengguna memiliki risiko keamanan tertinggi jika tidak dibatasi dengan ketat.

## Decision
Mac Agent hanya mengeksekusi aksi yang terdaftar secara eksplisit dalam katalog kemampuan (*CapabilityRegistry*). Setiap capability memiliki skema payload dan validasi input yang ketat.

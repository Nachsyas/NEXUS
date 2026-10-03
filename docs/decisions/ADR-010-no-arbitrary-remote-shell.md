# ADR-010: Strict Prohibition of Arbitrary Remote Shell

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Memberikan kemampuan eksekusi terminal shell sembarangan via AI membuka celah eksploitasi fatal terhadap workstation pengguna.

## Decision
Melarang keras (*strictly forbid*) capability terminal/shell arbitrer (misal `EXECUTE_SHELL`) pada Phase 1. Setiap aksi harus berupa capability spesifik terisolasi.

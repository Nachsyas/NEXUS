# ADR-015: Deterministic Permission and Risk Engine Outside LLM

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Model bahasa (LLM) probabilistik tidak dapat dijadikan benteng otorisasi keamanan karena rentan terhadap jailbreak dan manipulasi instruksi.

## Decision
Penegakan izin (DENY / ASK / ALLOW) dan klasifikasi risiko aksi dijalankan oleh mesin evaluasi kode deterministik di luar LLM pada backend dan Mac Agent.

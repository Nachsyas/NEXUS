# ADR-011: Model-Agnostic AI Provider Architecture

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Teknologi model AI berkembang sangat cepat. Mengikat domain logika ke satu vendor SDK tertentu menciptakan vendor lock-in yang berbahaya.

## Decision
Menerapkan pola **Model Router** dan adapter antarmuka abstrak. Domain service berkomunikasi hanya dengan antarmuka generic `AIService`.

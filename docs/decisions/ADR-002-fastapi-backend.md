# ADR-002: FastAPI Framework for Backend Core

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Backend NEXUS membutuhkan asynchronous I/O berkinerja tinggi untuk melayani WebSocket realtime, streaming LLM, serta ekosistem AI Python yang kaya.

## Problem
Memilih framework web Python modern yang efisien dan memiliki dukungan typing kuat.

## Decision
Menggunakan **FastAPI** dengan validasi skema tipe data berbasis Pydantic dan ASGI async/await.

## Alternatives
- *Django:* Terlalu berat dan kurang fleksibel untuk streaming WebSocket dan integrasi AI granular.
- *Go / Gin:* Sangat cepat namun ekosistem manipulasi dokumen, ekstraksi AI, dan data science jauh lebih matang di Python.

## Consequences
- Validasi data otomatis dan dokumentasi OpenAPI interaktif tersedia out-of-the-box.
- Perlu disiplin ketat dalam memisahkan logic komputasi berat ke background worker agar event loop tidak terblokir.

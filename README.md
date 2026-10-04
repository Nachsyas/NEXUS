# NEXUS

> **A Personal AI Companion that remembers, understands, connects, and acts.**

## 1. Ringkasan Proyek
NEXUS bukan sekadar aplikasi yang disematkan AI; NEXUS adalah ekosistem companion personal dengan arsitektur multi-endpoint:
- **iOS Client**: Antarmuka interaksi personal utama (Voice, Text, Context Transparency, Memory Control Center, Sign in with Apple) berlokasi di `apps/ios/NEXUS.xcodeproj`.
- **Mac Agent**: Secure execution node lokal untuk menjalankan safe actions terverifikasi berlokasi di `apps/mac-agent/`.
- **Backend Core**: Modular monolith berbasis FastAPI, PostgreSQL 16 (pgvector), dan Redis sebagai intelligence & orchestration layer berlokasi di `backend/`.

## 2. Status Repositori
- **Canonical Remote:** `https://github.com/Nachsyas/NEXUS.git` (Branch: `main`)
- **Repository Visibility:** PUBLIC (Intentionally public repository)
- **Phase saat ini:** Phase 1 (Core Personal Intelligence System)
- **Status Milestone:**
  - **M0 Foundation:** CLOSED & RATIFIED (Baseline arsitektur, environment uv, DB PostgreSQL 16 + pgvector, Redis, CI pipeline, target scaffolding).
  - **M1 Account & Identity:** CLOSED & RATIFIED (ADR-020 ACCEPTED, model domain User/AuthIdentity, Sign in with Apple, token rotation & reuse detection, isolasi multi-tenant).
  - **M2 Projects:** NEXT MILESTONE (Menunggu otorisasi pengguna).
- **Lisensi:** Lihat [`LICENSE-STATUS.md`](LICENSE-STATUS.md) (Status: TBD — Aksesibilitas publik tidak memberikan hak lisensi open source atau redistribusi).

## 3. Navigasi Dokumentasi
Bagi developer atau AI coding agent baru, urutan membaca adalah:
1. [`AGENTS.md`](AGENTS.md)
2. [`docs/README.md`](docs/README.md)
3. [`docs/context/HANDOFF.md`](docs/context/HANDOFF.md)
4. [`docs/context/PROJECT-STATE.md`](docs/context/PROJECT-STATE.md)
5. [`docs/GLOSSARY.md`](docs/GLOSSARY.md)

Seluruh spesifikasi teknis dan SOP tata kelola tersimpan di direktori `docs/`.

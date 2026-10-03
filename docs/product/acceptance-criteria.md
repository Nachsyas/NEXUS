# Phase 1 Acceptance Criteria — Master Matrix

**Status:** LOCKED  
**Version:** 1.1  

---

Setiap milestone Phase 1 wajib memenuhi kriteria penerimaan berikut sebelum dapat dinyatakan COMPLETE:

| Milestone | Nama | Acceptance Criteria Inti |
|---|---|---|
| **M0** | Foundation | Skeleton backend FastAPI berjalan, PostgreSQL + pgvector terhubung, Redis terhubung, migrasi Alembic berfungsi, unit test runner bekerja, skeleton iOS & Mac Agent launch, CI baseline. |
| **M1** | Account & Identity | Sign in with Apple terverifikasi, entitas `users` terpisah dari `auth_identities`, access token + rotating refresh token di Keychain, endpoint logout & revoke session bekerja, tes isolasi cross-user lulus. |
| **M2** | Projects | CRUD project, aktivasi & arsip, konsistensi status active project, project technologies terdata, isolasi kepemilikan antar user teruji. |
| **M3** | Memory Core | Klasifikasi memory type, dedup & conflict resolution, supersession, forget semantics (`/forget`), pemfilteran secret terbukti lulus uji, isolasi lintas project & user. |
| **M4** | AI Conversation | Percakapan streaming teks, Model Router modular tanpa coupling SDK vendor ke domain, Private Session terbukti tidak menyimpan memori, error handling graceful. |
| **M5** | Context Engine | Context Package terbukti bounded token budget, prioritas memori eksplisit di atas inferensi, data usang/terlupakan tidak bocor, leakage antar project 0%. |
| **M6** | Device Pairing | Pairing code jangka pendek sekali pakai, private key Mac tidak pernah keluar dari Keychain lokal, public key terdaftar di backend, koneksi ulang terotentikasi, proteksi replay. |
| **M7** | Device Intelligence | Mac Agent mengirim telemetry (baterai, storage, thermal, agent state), presence runtime (ONLINE/OFFLINE/STALE) akurat dan terpisah dari trust state (PAIRED/REVOKED). |
| **M8** | Remote Safe Actions | 8 safe capabilities terimplementasi, allowlist ketat, verifikasi eksekusi, penolakan arbitrary shell 100%, idempotency key aktif, audit trail tercatat. |
| **M9** | Permission & Audit | Kebijakan DENY/ASK/ALLOW ditegakkan di luar LLM, prompt aksi HIGH risk mewajibkan konfirmasi, kill switch mematikan remote actions seketika. |
| **M10** | Knowledge Vault | Upload dokumen asinkron via worker, chunking & pgvector indexing, semantic search dengan sitasi metadata valid, resistensi prompt injection teruji. |
| **M11** | Research Radar | Ingesti feed AI/tech, deduplikasi URL/konten, scoring relevansi personal, feed sementara dapat disimpan permanen ke Knowledge Vault. |
| **M12** | Voice + Action Button | Tap-to-talk voice interaktif, UI visualisasi listening yang jelas, integrasi App Intents / Shortcuts iOS, audio mentah tidak disimpan permanen. |
| **M13** | UX Polish | Antarmuka iOS responsif, loading, empty, stale, dan error state manusiawi tanpa raw stack trace, konsumsi penyimpanan lokal terkendali (~1-2 GB target). |
| **M14** | Beta Reliability | Uji ketahanan jaringan (Mac sleep/wake, hotspot transition, WSS auto-reconnect, token refresh failure recovery), AI regression suite lulus, zero blocking security findings. |

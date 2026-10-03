# Consistency Matrix — Governance Corrective Review (Pre-M0)

**Status:** RE-EVALUATED & FACTUALLY VERIFIED  
**Date:** 2026-10-03  

| Pasangan Dokumen / Aspek | Kriteria Konsistensi | Hasil | Catatan Faktual |
|---|---|---|---|
| **Product Vision ↔ Product Brief** | Visi companion personal dan positioning konsisten | PASS | Positioning companion personal terjaga utuh tanpa reduksi chatbot. |
| **Product Brief ↔ Phase 1 Spec** | Ruang lingkup Phase 1 selaras tanpa non-goals | PASS | Non-goals terlindungi; SSE dihapus (WSS baseline); Ed25519 dialihkan ke TBD-020. |
| **Phase Spec ↔ Roadmap** | Penahapan Phase 0 s/d Phase 5 identik | PASS | Hirarki penahapan roadmap terjaga konsisten. |
| **Roadmap ↔ Milestones** | Rincian M0 s/d M14 mencakup target Phase 1 | PASS | 15 milestone terdaftar lengkap dengan dependensi terarah. |
| **Milestones ↔ Acceptance Criteria** | Setiap milestone memiliki kriteria kelulusan jelas | PASS | Matriks acceptance criteria lengkap dan terdefinisi. |
| **Architecture ↔ ADRs** | Semua keputusan teknologi didukung ADR tanpa unapproved lock | PASS | ADR-001 s/d ADR-015 konsisten; asumsi PostgreSQL 16+, Pydantic V2, dan HNSW/<80ms dibersihkan. |
| **Architecture ↔ Repo Structure** | Struktur folder mematuhi spesifikasi repo | PASS (Pre-M0 Note) | Direktori target tata kelola (`apps/ios/`, `apps/mac-agent/`, `backend/`, `docs/`) telah ada. Scaffold bawaan awal (`Untitled Project.xcodeproj`, `MyApp/`) tetap berada di root dan akan dimigrasikan/direname to `apps/ios/` pada M0 Foundation. |
| **Database Architecture ↔ Data Contract** | Skema konseptual mencakup seluruh entitas, UTC timestamps, dan isolasi user | PASS | 19 entitas konseptual di 9 domain terdokumentasi lengkap dengan pemisahan semantik mutlak (ADR-012), isolasi user-scoped, dan pencegahan duplikasi provider email di core users. |
| **Memory Architecture ↔ Database Contract** | Taksonomi tipe memori (10 tipe), sensitivitas (4 level + NEVER_STORE), dan 6 tipe sumber konsisten | PASS | 10 tipe kanonikal (`PERSONAL_FACT` s/d `BEHAVIOR_PATTERN`), sensitivitas (`LOW` s/d `RESTRICTED` + `NEVER_STORE`), dan 6 sumber (`CONVERSATION` s/d `BEHAVIORAL_INFERENCE`) 100% identik di `memory-architecture.md` dan `database-architecture.md`. |
| **Memory Architecture ↔ API Contract** | Endpoint memori mendukung taksonomi kanonikal dan semantik forget | PASS | `POST /memories` mendukung 10 tipe kanonikal; filter status mencakup 5 status kanonikal; forget beralih ke `FORGOTTEN`. |
| **Knowledge Architecture ↔ Database Contract** | Status sumber daya, deduplikasi hash, penyimpanan objek, dan chunk provenance | PASS | Status sumber daya `PENDING`, `PROCESSING`, `READY`, `FAILED`, `DELETED` konsisten; `content_hash`, `object_key`, serta `page` dan `section` pada chunks terdefinisi eksplisit. |
| **Research Architecture ↔ Database Contract** | Metadata komprehensif, deduplikasi konten, dan state keterlibatan pengguna | PASS | `research_items` mencakup metadata lengkap, hash deduplikasi, dan embedding; `user_research_state` mencakup status resmi `UNSEEN`, `SEEN`, `SAVED`, `DISMISSED`. |
| **Device Architecture ↔ Database Contract** | Entitas identitas fisik, kapabilitas safe, dan log audit sesi tanpa secret plaintext | PASS | `devices` menyimpan hardware identity permanen; `device_capabilities` memuat primitive aman tanpa arbitrary shell; `device_sessions` menyimpan log audit tanpa credential plaintext. |
| **Security ↔ Permissions ↔ Actions** | Penegakan izin deterministik di luar LLM dan mitigasi ancaman | PASS | Tingkat DENY/ASK/ALLOW dan 4 scope terkunci; matriks default per-capability dipindahkan ke TBD-023; arbitrary shell mutlak DENY. Siklus hidup aksi selaras 11 status resmi. |
| **API ↔ Feature Specification** | Endpoint REST dan WebSocket selaras dengan kapabilitas approved baseline | PASS | Kontrak API v1 Phase 1 terdokumentasi lengkap di 13 domain (60 endpoint REST terdokumentasi, termasuk 1 convenience endpoint) dengan semantik request lengkap dan penanganan private session. |
| **AGENTS ↔ Development Workflow** | Otorisasi mandiri, kegagalan mandiri, dan batasan keputusan pengguna selaras | PASS | `AGENTS.md` (Bagian 5) dan `SOP 01` (Bagian 2 & 3) selaras penuh menetapkan Standing Autonomous Execution Policy, Failure Recovery protocol, User Decision Boundary, dan Platform Security Controls. |
| **Stage Template ↔ SOP-12** | Gerbang penyelesaian stage selaras dengan kriteria penutupan | PASS | SOP-12 memuat 22 kriteria completion gate faktual; folder stage template memuat 12 berkas fisik total (1 README orientasi + 11 artefak bukti). |
| **Skills ↔ Required Documentation** | 20 agent skills merujuk pada SOP dan doc kanonikal | PASS | Seluruh SKILL.md terverifikasi; skill `stage-close` disinkronkan penuh dengan 22 butir kriteria SOP-12. |
| **HANDOFF ↔ Actual Repo State** | Handover mencerminkan ketiadaan production code dan status scaffold riil | PASS | HANDOFF mencatat secara jujur ketiadaan kode produksi NEXUS (0 lines written), keberadaan scaffold default Xcode starter di root, dan 0 tautan aktif Markdown `file:///`. |

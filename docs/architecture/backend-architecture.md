# Backend Architecture — Modular Monolith

**Status:** LOCKED  
**Version:** 1.2  
**Decision Reference:** ADR-001, ADR-002, ADR-003, ADR-004, ADR-005  

---

## 1. Struktur Modul Backend
```text
backend/
├── app/
│   ├── main.py                # Inisialisasi FastAPI & Middleware
│   ├── core/                  # Konfigurasi, Database Engine, Redis, Security
│   ├── domains/               # Domain-driven modules
│   │   ├── auth/
│   │   ├── users/
│   │   ├── projects/
│   │   ├── memory/
│   │   ├── context/
│   │   ├── conversations/
│   │   ├── knowledge/
│   │   ├── research/
│   │   ├── devices/
│   │   ├── actions/
│   │   ├── permissions/
│   │   ├── audit/
│   │   ├── ai/
│   │   └── realtime/
│   └── shared/                # Kernel abstrak (Base Models, Value Objects)
├── workers/                   # Background jobs (Celery / ARQ / TBD-005)
├── migrations/                # Skrip Alembic
└── tests/                     # Unit, Integration, & Contract Tests
```

## 2. Pola Penanganan Request
- Setiap request divalidasi menggunakan skema Pydantic.
- Otentikasi menyematkan konteks pengguna (`current_user_id`) pada setiap panggilan.
- Setiap operasi mutasi data yang relevan memicu penulisan event audit ke database.
- Request yang membutuhkan operasi berat (seperti pembuatan embedding dokumen atau ringkasan riset) didelegasikan ke queue background worker.

## 3. Implementation Baselines vs Locked Architecture
Perbedaan antara batasan arsitektur terkunci (*locked architectural constraints*) dan baseline implementasi (*implementation baselines*):
- **Locked Architectural Constraints:** Keputusan struktural yang mengikat dan hanya dapat diubah melalui ADR baru berstatus ACCEPTED (misal: Pola Modular Monolith [ADR-001], Larangan Shell Arbitrer [ADR-010], Pemisahan Semantik Data [ADR-012], Penggunaan PostgreSQL [ADR-003]).
- **Implementation Baselines:** Detail implementasi runtime M0 (seperti Redis 7, SQLAlchemy async engine, driver `asyncpg`/`psycopg`, pemetaan port host lokal `5433` dan `6380`, atau versi patch pustaka tertentu) berstatus sebagai *implementation baselines*, bukan batasan arsitektur yang dibuat kaku secara artifisial. Detail ini dapat disesuaikan, ditingkatkan (*upgraded*), atau dikonfigurasi ulang sesuai evolusi kebutuhan teknis tanpa perlu mengubah arsitektur inti.

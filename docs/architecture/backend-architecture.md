# Backend Architecture — Modular Monolith

**Status:** LOCKED  
**Version:** 1.1  
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

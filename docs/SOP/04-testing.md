# SOP 04 — Testing Strategy & Execution

**Status:** CANONICAL SOP  
**Version:** 1.1  

## 1. Piramida Pengujian
- **Unit Tests:** Menguji fungsionalitas murni fungsi, domain rules, skema, dan utility.
- **Integration Tests:** Menguji kolaborasi antar domain, koneksi DB PostgreSQL, operasi Redis, dan background jobs.
- **Contract Tests:** Menguji kecocokan skema data antara Backend ↔ iOS dan Backend ↔ Mac Agent.
- **Security & AI Evals:** Menguji pencegahan kebocoran data multi-tenant, resistensi prompt injection, dan isolasi proyek.

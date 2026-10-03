# KNOWN ISSUES — Global Repository Register

Daftar utang teknis, temuan audit tata kelola, dan batasan repositori yang tercatat secara resmi:

---

## 1. Active Issues
*None.* Currently 0 active blockers or known defects.

---

## 2. Resolved Issues in Milestone M0 (2026-10-03)
| Issue ID | Deskripsi Masalah | Komponen Terdampak | Status | Tindakan Resolusi |
|---|---|---|---|---|
| **ISSUE-001** | Scaffold bawaan default Xcode (`Untitled Project.xcodeproj` & `MyApp/`) berada di root repositori. | Repository Structure / iOS | RESOLVED | Dimigrasikan dan dikonfigurasi ulang ke `apps/ios/NEXUS.xcodeproj`, folder starter lama dihapus dengan aman. |
| **ISSUE-002** | Keputusan teknologi tooling lokal (TBD-013, TBD-014, TBD-015, TBD-026). | Local Development | RESOLVED | Diresolusikan via persetujuan eksplisit pengguna dan diratifikasi dalam ADR-016 hingga ADR-019. |
| **ISSUE-003** | Port host default 5432 dan 6379 bertabrakan dengan kontainer lokal yang sudah ada. | Local Infrastructure | RESOLVED | Dikonfigurasi ulang port host ke 5433 (PostgreSQL) dan 6380 (Redis) melalui environment variable tanpa mengganggu layanan pengguna. |
| **ISSUE-004** | Dependensi `greenlet` diperlukan oleh SQLAlchemy asyncio mode. | Backend Tooling | RESOLVED | Ditambahkan ke `backend/pyproject.toml` dan disinkronkan via `uv`. |

---

## 3. Resolved Governance Audit Findings (Pre-M0)
| Audit Item | Temuan Awal | Status Resolusi | Tindakan Perbaikan |
|---|---|---|---|
| **AUDIT-001** | Tautan Markdown menggunakan skema mesin absolut `file:///` | RESOLVED | Seluruh tautan diubah menjadi tautan relatif portabel. |
| **AUDIT-002** | Klaim "0 production files" tanpa kualifikasi scaffold awal | RESOLVED | Dikoreksi faktual pada fase bootstrap; dituntaskan di M0. |
| **AUDIT-003** | Klaim struktur repositori mengabaikan posisi Xcode scaffold di root | RESOLVED | Dimigrasikan ke `apps/ios/` pada M0. |
| **AUDIT-004** | Kontrak API v1 tidak lengkap | RESOLVED | Diperluas penuh ke 60 endpoint terdokumentasi sesuai baseline. |
| **AUDIT-005** | Skema database kurang memuat kontrak data konseptual | RESOLVED | Diperluas mendokumentasikan 19 entitas konseptual di 9 domain. |
| **AUDIT-006** | Asumsi teknis unapproved terkunci | RESOLVED | Dipindahkan ke TBD Registry dan diselesaikan secara resmi saat diperlukan. |
| **AUDIT-007** | Target numerik budget performa dibuat sebelum pengukuran riil | RESOLVED | Dialihkan ke prinsip Measurement-First (baseline diukur di M0). |
| **AUDIT-008** | Matriks izin per-capability ditetapkan sebagai locked default | RESOLVED | Dipindahkan ke status PROPOSED / TBD-023. |
| **AUDIT-009** | Workflow CI mengasumsikan Python 3.11 dan backend runner prematur | RESOLVED | Disesuaikan dengan `uv` dan verifikasi multi-tooling resmi pada M0. |
| **AUDIT-010** | SOP-12 dan skill stage-close tidak mencakup 22 butir completion gate | RESOLVED | SOP-12 diperluas penuh mencakup seluruh 22 butir kriteria gate. |
| **AUDIT-011** | Berkas `bootstrap_report.md` dirujuk namun tidak eksis secara fisik | RESOLVED | Berkas laporan faktual nyata dibuat dan diverifikasi. |

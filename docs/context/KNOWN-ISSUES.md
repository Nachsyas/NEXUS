# KNOWN ISSUES — Global Repository Register

Daftar utang teknis, temuan audit tata kelola, dan batasan repositori yang tercatat secara resmi:

---

## 1. Active Pre-M0 Architectural / Repository Items
| Issue ID | Deskripsi Masalah | Komponen Terdampak | Status | Rencana Resolusi |
|---|---|---|---|---|
| **ISSUE-001** | Scaffold bawaan default Xcode (`Untitled Project.xcodeproj` & `MyApp/`) masih berada di root repositori dan belum dimigrasikan ke `apps/ios/`. | Repository Structure | PENDING M0 | Migrasi dan penamaan ulang ke `apps/ios/NEXUS.xcodeproj` dijadwalkan secara resmi pada Milestone M0 Foundation setelah persetujuan tata kelola. |
| **ISSUE-002** | Keputusan teknologi tooling lokal (Python env manager, linter, DB version) masih berstatus TBD (TBD-013, TBD-015, TBD-026). | Local Development | OPEN (TBD) | Diselesaikan bersama pengguna pada sesi kick-off Milestone M0. |

---

## 2. Resolved Governance Audit Findings (Final Corrective Pass 2026-10-03)
| Audit Item | Temuan Awal | Status Resolusi | Tindakan Perbaikan |
|---|---|---|---|
| **AUDIT-001** | Tautan Markdown menggunakan skema mesin absolut `file:///Users/user/...` | RESOLVED | Seluruh tautan diubah menjadi tautan relatif portabel; diverifikasi 0 active Markdown repository links using file:/// remain. |
| **AUDIT-002** | Klaim "0 production files" tanpa kualifikasi scaffold awal | RESOLVED | Dikoreksi faktual: Scaffold awal Xcode starter tercatat jelas belum dimigrasikan; tidak ada kode produksi NEXUS baru yang ditulis. |
| **AUDIT-003** | Klaim struktur repositori mengabaikan posisi Xcode scaffold di root | RESOLVED | Consistency matrix dan Project State dikoreksi mencerminkan scaffold di root menunggu M0. |
| **AUDIT-004** | Kontrak API v1 tidak lengkap | RESOLVED | Diperluas penuh ke 60 endpoint terdokumentasi sesuai baseline approved di 13 domain (59 core + 1 convenience endpoint). |
| **AUDIT-005** | Skema database kurang memuat kontrak data konseptual | RESOLVED | Diperluas mendokumentasikan 19 entitas konseptual di 9 domain beserta semantik mutlak ADR-012 dan UTC timestamps. |
| **AUDIT-006** | Asumsi teknis unapproved terkunci (PostgreSQL 16+, Pydantic V2, Ed25519, Secure Enclave, TTL 5m, Heartbeat 30s/60s, SSE, HNSW/<80ms) | RESOLVED | Seluruh asumsi unapproved dibersihkan dari teks locked dan dipindahkan ke TBD Registry (TBD-020 s/d TBD-026). |
| **AUDIT-007** | Target numerik budget performa dibuat sebelum pengukuran riil | RESOLVED | Dialihkan ke prinsip Measurement-First (Baseline: NOT MEASURED, Target: TBD AFTER BASELINE), mempertahankan approved iOS storage guideline. |
| **AUDIT-008** | Matriks izin per-capability ditetapkan sebagai locked default | RESOLVED | Dipindahkan ke status PROPOSED / TBD-023; arbitrary shell tetap locked DENY. |
| **AUDIT-009** | Workflow CI mengasumsikan Python 3.11 dan backend runner prematur | RESOLVED | Dikonversi menjadi workflow validasi tata kelola murni tanpa asumsi runtime/tooling backend; validasi link diubah untuk memeriksa sintaks tautan Markdown absolut. |
| **AUDIT-010** | SOP-12 dan skill stage-close tidak mencakup 22 butir completion gate | RESOLVED | SOP-12 dan skill `stage-close` diperluas penuh mencakup seluruh 22 butir kriteria gate (12 berkas stage total: 1 README + 11 bukti). |
| **AUDIT-011** | Berkas `bootstrap_report.md` dirujuk namun tidak eksis secara fisik | RESOLVED | Berkas laporan faktual nyata dibuat di `bootstrap_report.md` dan `docs/validation/GOVERNANCE-BOOTSTRAP-REPORT.md`. |

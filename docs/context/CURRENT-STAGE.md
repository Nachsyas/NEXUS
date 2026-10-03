# CURRENT STAGE: Governance Corrective Review / Pre-M0

**Current Stage:** Governance Corrective Review / Pre-M0  
**Phase:** Phase 0 (Governance Bootstrap)  
**Production NEXUS Implementation:** NOT STARTED  
**Pre-existing Xcode Scaffold:** PRESENT (`Untitled Project.xcodeproj` & `MyApp/` di root; belum dimigrasikan ke `apps/ios/`)  
**M0 Status:** BLOCKED UNTIL GOVERNANCE CORRECTIVE PASS IS VERIFIED  

---

## 1. Sasaran Tahap Korektif (Corrective Objectives)
Melakukan perbaikan komprehensif terhadap dokumen tata kelola berdasarkan hasil audit eksternal, memastikan tidak ada klaim kelulusan yang prematur, membersihkan asumsi sepihak yang belum disetujui, dan melengkapi kontrak data serta API sesuai baseline resmi.

## 2. Kriteria Penerimaan Evaluasi Korektif (Acceptance Checklist)
- [x] **Internal Links Portability:** Seluruh tautan absolut `file:///` dan path mesin lokal telah dihapus dan diganti dengan tautan relatif repositori. 0 active Markdown repository links using file:/// remain.
- [x] **Production Code Factual Claim:** Pernyataan "0 production files" telah dikoreksi dengan penjelasan jujur mengenai scaffold bawaan awal Xcode yang belum dimigrasi.
- [x] **Repository Structure Claim:** Struktur repositori mencatat bahwa scaffold Xcode awal masih berada di root dan akan dimigrasikan/direname pada M0 Foundation.
- [x] **API Contract Completeness:** Kontrak REST API v1 didokumentasikan lengkap mencakup 60 endpoint yang disetujui di 13 domain (59 core + 1 convenience endpoint).
- [x] **Database Conceptual Contract:** Kontrak data konseptual mencakup 19 entitas di 9 domain dengan pemisahan semantik mutlak (ADR-012) dan UTC timestamps.
- [x] **Removal of Unapproved Decisions:** Asumsi PostgreSQL 16+, Pydantic V2, Ed25519 locked, TTL 5 menit, Heartbeat 30s/60s, SSE, HNSW/<80ms telah dibersihkan dari teks locked.
- [x] **TBD Expansion:** TBD-020 hingga TBD-026 ditambahkan secara resmi ke `docs/architecture/TBD-REGISTRY.md`.
- [x] **Measurement-First Performance:** Budget performa diperbaiki ke prinsip Measurement-First (Baseline: NOT MEASURED, Target: TBD AFTER BASELINE), mempertahankan approved iOS storage guideline.
- [x] **Permission Policy Demoted:** Matriks izin per-capability dialihkan ke PROPOSED / TBD-023; arbitrary shell tetap mutlak DENY.
- [x] **CI Configuration Corrected:** CI workflow disesuaikan menjadi validasi tata kelola murni tanpa pemilihan runtime/tooling Python prematur.
- [x] **Stage Completion Gate Alignment:** SOP-12 dan skill `stage-close` diperluas penuh memuat seluruh 22 butir kriteria completion gate faktual (12 berkas stage total: 1 README orientasi + 11 artefak bukti).
- [x] **Consistency Matrix Re-evaluated:** `docs/validation/CONSISTENCY-MATRIX.md` mencerminkan evaluasi faktual riil.
- [x] **Real Verification Report:** Laporan verifikasi faktual nyata tersedia di repositori (`bootstrap_report.md` dan `docs/validation/GOVERNANCE-BOOTSTRAP-REPORT.md`).

## 3. Kondisi Pemblokir (Blockers)
Pengerjaan Milestone M0 (Foundation) **DIBLOKIR** sampai pengguna meninjau dan memberikan persetujuan formal terhadap laporan tata kelola korektif ini.

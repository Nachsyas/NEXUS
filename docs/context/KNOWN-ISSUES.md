# KNOWN ISSUES — Global Repository Register

Daftar utang teknis, temuan audit tata kelola, dan batasan repositori yang tercatat secara resmi:

---

## 1. Active Issues
*None.* Currently 0 active blockers or known defects.

---

## 2. Operational Caveats & Status Notes (Milestone M1)
| Caveat ID | Deskripsi | Komponen Terdampak | Status | Catatan Operasional |
|---|---|---|---|---|
| **CAVEAT-001** | Live Apple Sign-In E2E Verification | iOS & Auth Backend | DOCUMENTED / PENDING LIVE TEST | Kode verifikasi produksi (`ProductionAppleVerifier`) dan UI (`AuthView`) lengkap. Test otomatis 100% lulus via `MockAppleVerifier`. Live E2E dengan server Apple berstatus `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED` hingga akun Apple Developer riil diprovisi. |

---

## 3. Resolved Issues in Milestone M1 (2026-10-04)
| Issue ID | Deskripsi Masalah | Komponen Terdampak | Status | Tindakan Resolusi |
|---|---|---|---|---|
| **ISSUE-005** | Token Reuse Detection DB Rollback: FastAPI rollback pada unhandled domain error membatalkan revokasi family. | Backend Auth Service | RESOLVED | Menambahkan `await db.commit()` eksplisit sebelum melempar `RefreshTokenReusedError` sehingga revokasi tersimpan permanen di PostgreSQL. |
| **ISSUE-006** | Swift 6 Approachable Concurrency Actor Isolation pada DTO Codable. | iOS Data Models | RESOLVED | DTO model dan helper network/keychain ditandai `nonisolated` agar kompatibel lintas thread background URLSession. |
| **ISSUE-007** | Ratifikasi Formal ADR-020 (Session Token Format & Rotation). | Architecture Governance | RESOLVED | Diratifikasi secara formal oleh pengguna sebagai ACCEPTED; TBD-028 dan TBD-029 berstatus RESOLVED. |

---

## 4. Resolved Issues in Milestone M0 (2026-10-03)
| Issue ID | Deskripsi Masalah | Komponen Terdampak | Status | Tindakan Resolusi |
|---|---|---|---|---|
| **ISSUE-001** | Scaffold bawaan default Xcode (`Untitled Project.xcodeproj` & `MyApp/`) berada di root repositori. | Repository Structure / iOS | RESOLVED | Dimigrasikan dan dikonfigurasi ulang ke `apps/ios/NEXUS.xcodeproj`, folder starter lama dihapus dengan aman. |
| **ISSUE-002** | Keputusan teknologi tooling lokal (TBD-013, TBD-014, TBD-015, TBD-026). | Local Development | RESOLVED | Diresolusikan via persetujuan eksplisit pengguna dan diratifikasi dalam ADR-016 hingga ADR-019. |
| **ISSUE-003** | Port host default 5432 dan 6379 bertabrakan dengan kontainer lokal yang sudah ada. | Local Infrastructure | RESOLVED | Dikonfigurasi ulang port host ke 5433 (PostgreSQL) dan 6380 (Redis) melalui environment variable tanpa mengganggu layanan pengguna. |
| **ISSUE-004** | Dependensi `greenlet` diperlukan oleh SQLAlchemy asyncio mode. | Backend Tooling | RESOLVED | Ditambahkan ke `backend/pyproject.toml` dan disinkronkan via `uv`. |

---

## 5. Resolved Governance Audit Findings (Pre-M0)
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

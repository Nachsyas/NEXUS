# SOP 12 — Stage Completion Gate & Verification

**Status:** CANONICAL SOP — MANDATORY GATE  
**Version:** 1.3  

---

## 1. Prinsip Utama Stage Completion Gate
Penyelesaian stage atau milestone pada ekosistem NEXUS menganut prinsip bukti faktual (*evidence-based governance*). Tidak ada stage yang boleh dinyatakan selesai (`COMPLETE`) hanya berdasarkan asumsi, klaim lisan, atau kode yang belum tervalidasi.

Jika satu saja kriteria kritis belum terpenuhi, atau pengujian belum dijalankan secara empiris, status wajib ditetapkan sebagai:
```text
STATUS = PARTIAL (atau FAILED bila terjadi pelanggaran arsitektur/keamanan fatal)
```
Dilarang keras menandai `STATUS = COMPLETE` jika terdapat kriteria yang belum terbukti secara faktual.

---

## 2. Persyaratan Lengkap Stage Completion Gate (22 Kriteria)
Sebelum stage atau milestone ditutup, seluruh aspek berikut wajib dievaluasi dan didokumentasikan di folder stage terkait (`docs/stages/<STAGE_ID>/`):

### 2.1 Kriteria Fungsional & Implementasi
1. **Acceptance Criteria Verification:** Setiap butir kriteria penerimaan pada `plan.md` / `acceptance-criteria.md` telah terpenuhi dan dibuktikan dengan hasil tes nyata.
2. **Actual Implementation Completion:** Fitur dalam ruang lingkup stage telah terimplementasi secara nyata tanpa menyisakan placeholder kosong atau bypass sementara.

### 2.2 Verifikasi Kualitas & Pengujian
3. **Required Tests Executed:** Seluruh suite pengujian otomatis (unit, integrasi, dan kontrak antarmuka) telah dieksekusi secara aktual.
4. **Required Tests Passing:** 100% tes yang dieksekusi berhasil lulus tanpa *flaky tests* yang diabaikan.
5. **AI Evaluation (bila relevan):** Kasus uji AI Eval (retrieval accuracy, intent classification, injection resistance) dieksekusi dan memenuhi ambang kualitas.

### 2.3 Review Arsitektur & Keamanan
6. **Architecture Review:** Dokumen `architecture-review.md` terisi lengkap; memverifikasi kepatuhan terhadap batas domain, tidak ada cyclic dependencies, dan tidak ada cross-domain repository shortcut.
7. **Security Review:** Dokumen `security-review.md` terisi lengkap; memverifikasi mitigasi IDOR, perlakuan data eksternal sebagai DATA, perlindungan kredensial, dan larangan mutlak *arbitrary shell*.
8. **Performance Evaluation:** Dokumen `performance-results.md` terisi angka baseline empiris terukur (sesuai kaidah Measurement-First ADR-014).
9. **Observability Consideration:** Memastikan setiap alur kritis membawa `request_id` / `action_id`, structured logging, dan telemetri yang memadai.

### 2.4 Berkas Bukti Nyata (Stage Artifacts)
Terdapat 12 berkas stage yang diwajibkan total (1 berkas orientasi/README + 11 artefak bukti/penyelesaian) di mana seluruh 11 artefak bukti wajib terisi secara faktual:
10. `plan.md`: Rencana kerja dan acceptance criteria awal.
11. `implementation-log.md`: Catatan kronologis langkah implementasi teknis.
12. `files-changed.md`: Daftar lengkap berkas yang dibuat, dimodifikasi, atau dihapus.
13. `commands-run.md`: Daftar perintah aktual yang dijalankan selama proses pengerjaan dan pengujian.
14. `test-results.md`: Output log eksekusi pengujian faktual dan rasio kelulusan.
15. `security-review.md`: Penilaian risiko keamanan terstruktur.
16. `architecture-review.md`: Kuesioner evaluasi kepatuhan arsitektur.
17. `performance-results.md`: Hasil benchmark performa empiris.
18. `deviations.md`: Catatan penyimpangan rencana awal beserta justifikasi teknisnya.
19. `known-issues.md`: Catatan kendala atau batasan yang teridentifikasi selama stage.
20. `completion-report.md`: Laporan penutupan formal yang merangkum hasil verifikasi seluruh gate.  
*(Catatan: `README.md` pada folder stage berfungsi sebagai berkas orientasi stage pendukung 11 artefak bukti di atas, menggenapi 12 berkas fisik di `docs/stages/_template/`).*

### 2.5 Sinkronisasi Status Repositori & Kontinuitas
21. **Context Documents Synchronized:**
    - `docs/context/PROJECT-STATE.md` diperbarui mencerminkan milestone/stage yang selesai.
    - `docs/context/CURRENT-STAGE.md` diperbarui dengan target stage berikutnya.
    - `docs/context/NEXT-ACTIONS.md` diperbarui dengan instruksi langkah pertama yang jelas.
    - `docs/context/HANDOFF.md` diperbarui agar agent atau developer baru dapat melanjutkan pekerjaan tanpa kehilangan konteks.
22. **Known Git State:** Status commit, branch, dan status kebersihan tree git tercatat faktual.

---

## 3. Matriks Keputusan Kelulusan Gate
- **`COMPLETE`**: Seluruh butir 1 s/d 22 terpenuhi 100%, seluruh tes lulus, zero blocking review issues.
- **`PARTIAL`**: Terdapat butir atau tes yang belum selesai/teruji, namun tidak ada pelanggaran keamanan arsitektur kritis. Stage tidak boleh dianggap selesai untuk membuka tahap berikutnya yang bergantung padanya.
- **`FAILED`**: Ditemukan pelanggaran Invarian Keamanan (misal: celah shell arbitrer, kebocoran secret, pelanggaran batas domain) atau kegagalan tes fundamental. Implementasi wajib ditolak dan diperbaiki.

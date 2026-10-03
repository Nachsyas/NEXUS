# Skill: stage-close

## 1. Description
Melakukan validasi gerbang penyelesaian panggung (*Stage Completion Gate*) dan serah terima konteks repositori secara ketat dan berbasis bukti faktual.

## 2. When Used
Saat seluruh pekerjaan implementasi sebuah stage atau milestone telah selesai dan hendak ditutup secara formal.

## 3. Prerequisites
- Seluruh kode implementasi telah ditulis dan lolos pemeriksaan lokal.
- Seluruh acceptance criteria stage telah dievaluasi.
- 12 berkas fisik stage (1 README orientasi + 11 artefak bukti) di `docs/stages/<STAGE_ID>/` telah disiapkan.

## 4. Required Docs
- `docs/SOP/12-stage-completion.md` (Mandatory Completion Gate - 22 Kriteria)
- `docs/stages/<STAGE_ID>/` (12 berkas stage)
- `docs/context/PROJECT-STATE.md`
- `docs/context/CURRENT-STAGE.md`
- `docs/context/NEXT-ACTIONS.md`
- `docs/context/KNOWN-ISSUES.md`
- `docs/context/HANDOFF.md`

## 5. Workflow (Stage Completion Verification Gate — 22 Criteria)
Agent wajib mengeksekusi dan memverifikasi seluruh butir pemeriksaan secara sekuensial:

1. **Acceptance Criteria Verification:** Cocokkan setiap butir di `plan.md` / `acceptance-criteria.md` dengan implementasi riil.
2. **Implementation Completion:** Pastikan tidak ada kode dummy atau mock sementara yang tertinggal di jalur produksi.
3. **Execute Required Tests:** Jalankan test suite aktual dan catat output ke `test-results.md`. Seluruh tes wajib berstatus PASS (100%).
4. **AI Evaluation (bila relevan):** Jalankan kasus uji eval di `docs/ai/eval-cases/` dan catat metrik akurasi / ketahanan.
5. **Architecture Review:** Lengkapi kuesioner `architecture-review.md` (pastikan zero domain violations, zero cross-domain repo shortcuts).
6. **Security Review:** Lengkapi `security-review.md` (evaluasi IDOR, least privilege, zero arbitrary shell, secret filtering).
7. **Performance Evaluation:** Catat angka empiris terukur ke `performance-results.md` (baseline/observed, dilarang merekayasa angka).
8. **Observability Verification:** Pastikan korelasi ID (`request_id`, `action_id`) dan structured logging diterapkan.
9. **Record Evidence Artifacts (11 Artefak Bukti + 1 README Orientasi):**
   - Catat berkas yang disentuh di `files-changed.md`.
   - Catat perintah yang dijalankan di `commands-run.md`.
   - Catat narasi teknis di `implementation-log.md`.
   - Catat deviasi di `deviations.md` dan kendala terbuka di `known-issues.md`.
10. **Formulate Completion Report:**
    - Buat `completion-report.md` di folder stage.
    - Tetapkan status secara jujur: `COMPLETE` jika 100% kriteria lulus; `PARTIAL` jika ada butir yang belum teruji/selesai; `FAILED` jika ada pelanggaran kritis.
11. **Synchronize Repository Context:**
    - Perbarui `docs/context/PROJECT-STATE.md`.
    - Perbarui `docs/context/CURRENT-STAGE.md`.
    - Perbarui `docs/context/NEXT-ACTIONS.md`.
    - Perbarui `docs/context/KNOWN-ISSUES.md`.
    - Perbarui `docs/context/HANDOFF.md` dengan instruksi serah terima transparan.
12. **Record Git State:** Catat status kebersihan git working tree dan commit terakhir.

## 6. Validation
Verifikasi kontinuitas operasional: AI agent baru atau pengembang eksternal harus dapat memahami status proyek terkini dan langsung melanjutkan pekerjaan hanya dengan membaca `HANDOFF.md` dan dokumen konteks.

## 7. Docs Update
Folder stage (`docs/stages/<STAGE_ID>/`) dan seluruh berkas di `docs/context/` diperbarui serentak secara konsisten.

## 8. Stop Conditions
- Dilarang menandai stage sebagai `COMPLETE` bila ada acceptance criteria yang belum terbukti secara faktual (wajib berstatus `PARTIAL`).
- Hentikan proses dan laporkan status `FAILED` jika ditemukan pelanggaran Invarian Keamanan atau Invarian Arsitektur.

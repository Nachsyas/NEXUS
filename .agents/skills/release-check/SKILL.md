# Skill: release-check

## 1. Description
Pemeriksaan menyeluruh sebelum rilis versi atau integrasi besar.

## 2. When Used
Sebelum rilis milestone penting atau penggabungan branch utama.

## 3. Prerequisites
Seluruh test suite dan validasi stage telah lengkap.

## 4. Required Docs
- `docs/SOP/12-stage-completion.md`
- `docs/context/PROJECT-STATE.md`

## 5. Workflow
1. Jalankan linter, formatter, dan type checker.
2. Jalankan seluruh unit, integration, dan AI evaluation tests.
3. Scan repositori terhadap potensi secret atau credential yang tertinggal.
4. Periksa kecocokan skema migrasi database dengan model domain.
5. Verifikasi kepatuhan lisensi dan catatan rilis.

## 6. Validation
Zero blocking issues, zero lint errors, zero test failures.

## 7. Docs Update
Catat versi dan ringkasan rilis pada `PROJECT-STATE.md`.

## 8. Stop Conditions
Batalkan rilis jika ditemukan potensi kebocoran secret atau regresi keamanan.

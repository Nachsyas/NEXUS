# Skill: debug-issue

## 1. Description
Mengisolasi akar masalah (*root cause*) dan menerapkan perbaikan terarah.

## 2. When Used
Saat terjadi kegagalan test, unhandled error, atau kejanggalan perilaku sistem.

## 3. Prerequisites
Laporan kegagalan atau log error tersedia.

## 4. Required Docs
- `docs/SOP/09-debugging.md`

## 5. Workflow
1. Reproduksi masalah dalam lingkungan pengujian terkontrol.
2. Telusuri stack trace dan log korelasi untuk menemukan layer yang bertanggung jawab.
3. Tulis regression test yang gagal membuktikan adanya bug tersebut.
4. Terapkan perbaikan pada layer yang bersangkutan.
5. Jalankan kembali test suite untuk memastikan regresi teratasi.

## 6. Validation
Regression test yang sebelumnya gagal kini berhasil lulus.

## 7. Docs Update
Catat temuan pada implementation log atau `docs/context/KNOWN-ISSUES.md`.

## 8. Stop Conditions
Berhenti jika mencoba menyelesaikan bug dengan mematikan validasi keamanan.

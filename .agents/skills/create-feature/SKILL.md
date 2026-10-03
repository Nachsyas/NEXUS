# Skill: create-feature

## 1. Description
Mengembangkan fungsionalitas baru dengan menjaga batasan domain dan kualitas kode.

## 2. When Used
Saat mengimplementasikan fitur yang telah disetujui dalam spesifikasi fase aktif.

## 3. Prerequisites
Feature tercakup dalam milestone aktif dan memiliki acceptance criteria yang jelas.

## 4. Required Docs
- `docs/product/phase-1-specification.md`
- `docs/architecture/domain-boundaries.md`
- SOP yang relevan

## 5. Workflow
1. Konfirmasi kepatuhan fitur terhadap batasan fase aktif.
2. Tentukan domain yang memiliki tanggung jawab (*domain ownership*).
3. Buat irisan perubahan terkecil yang fungsional.
4. Tulis unit test dan integration test.
5. Verifikasi bahwa tidak ada cross-domain repository shortcut.

## 6. Validation
Jalankan test suite dan verifikasi kelulusan 100%.

## 7. Docs Update
Update stage implementation-log dan files-changed.

## 8. Stop Conditions
Berhenti jika fitur membutuhkan perubahan arsitektur besar tanpa ADR.

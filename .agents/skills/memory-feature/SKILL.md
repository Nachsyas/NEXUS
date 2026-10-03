# Skill: memory-feature

## 1. Description
Mengimplementasikan penyimpanan fakta personal/proyek dengan filter sensitivitas.

## 2. When Used
Saat membangun atau memodifikasi alur Memory Core.

## 3. Prerequisites
Sistem pemfilteran secret dan klasifikasi memori telah siap.

## 4. Required Docs
- `docs/architecture/memory-architecture.md`
- `docs/security/security-architecture.md`

## 5. Workflow
1. Terapkan validasi `worth_storing` pada input informasi.
2. Jalankan filter sensitivitas untuk menolak password/token/OTP.
3. Periksa potensi konflik dan lakukan superseding bila fakta diperbarui.
4. Terapkan handler `/forget` untuk menandai status `FORGOTTEN`.
5. Uji isolasi antar user dan antar proyek.

## 6. Validation
Jalankan test evaluasi memori di `docs/ai/eval-cases/memory-retrieval.md`.

## 7. Docs Update
Update implementation-log pada milestone M3.

## 8. Stop Conditions
Berhenti jika ada secret yang lolos tersimpan ke database memori.

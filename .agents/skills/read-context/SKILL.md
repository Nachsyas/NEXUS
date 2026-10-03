# Skill: read-context

## 1. Description
Mengorientasikan diri pada status proyek, tata kelola, dan batasan arsitektur sebelum mengeksekusi tugas.

## 2. When Used
Pada awal setiap sesi kerja baru atau saat berpindah tugas.

## 3. Prerequisites
Repositori telah di-clone dan memiliki struktur direktori docs/.

## 4. Required Docs
- `AGENTS.md`
- `docs/context/PROJECT-STATE.md`
- `docs/context/CURRENT-STAGE.md`
- `docs/context/HANDOFF.md`
- Dokumen kanonikal terkait tugas

## 5. Workflow
1. Baca `AGENTS.md` untuk memahami aturan mutlak.
2. Baca `PROJECT-STATE.md` untuk mengetahui fase dan milestone aktif.
3. Baca `CURRENT-STAGE.md` untuk mengetahui sasaran spesifik tahap ini.
4. Baca `HANDOFF.md` untuk instruksi spesifik task berikutnya.
5. Periksa repositori aktual untuk mendeteksi drift antara kode dan dokumen.

## 6. Validation
Konfirmasi pemahaman status sebelum mengusulkan aksi implementasi.

## 7. Docs Update
Tidak ada pembaruan dokumen pada fase membaca.

## 8. Stop Conditions
Berhenti jika status repositori bertentangan secara fatal dengan isi `HANDOFF.md` dan diskusikan dengan pengguna.

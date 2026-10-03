# SOP 01 — Development Workflow & Autonomous Execution Policy

**Status:** CANONICAL SOP  
**Version:** 1.2  

---

## 1. Alur Kerja Rekayasa Standar
1. **Memahami Konteks:** Baca `AGENTS.md`, `PROJECT-STATE.md`, `CURRENT-STAGE.md`, dan `HANDOFF.md`.
2. **Spesifikasi & Batasan:** Pastikan fitur yang dikerjakan tercakup dalam scope fase/milestone aktif.
3. **Desain Perubahan Terkecil:** Buat irisan perubahan yang koheren, teruji, dan tidak merusak batas domain.
4. **Implementasi Bertahap:** Tulis kode sesuai standar arsitektur modular monolith, sertakan penanganan kegagalan (*fail-closed*).
5. **Pengujian & Validasi:** Jalankan unit test, integrasi, dan periksa kepatuhan keamanan serta konsistensi kontrak data.
6. **Pencatatan Bukti:** Catat perubahan pada berkas dokumentasi stage terkait (implementation log, files changed, dsb).

---

## 2. Kebijakan Otonomi Pelaksanaan Mandiri (Standing Autonomous Execution Policy)

### 2.1 Otorisasi Mandiri Penuh di Bawah Tugas/Milestone yang Disetujui
Saat pengguna menginstruksikan atau memulai sebuah tugas/milestone (misalnya kickoff Milestone M0):
- Instruksi tersebut menjadi mandat otorisasi penuh (*standing authorization*) untuk melaksanakan seluruh rangkaian siklus rekayasa tanpa meminta konfirmasi berulang (*zero micro-confirmations*).
- **Prinsip Operasional Agen:**
  ```text
  DO THE WORK.
  VALIDATE IT.
  FIX PROBLEMS.
  CONTINUE.
  DOCUMENT IT.
  COMPLETE THE ASSIGNMENT.
  ```
- **Dilarang keras meminta izin mikro** seperti:
  - *"Bolehkah saya mengedit berkas ini?"*
  - *"Bolehkah saya membuat folder/skrip ini?"*
  - *"Bolehkah saya menjalankan pengetesan?"*
  - *"Bolehkah saya memperbaiki bug ini?"*
  - *"Bolehkah saya memperbarui dokumen serah terima?"*  
  selama tindakan tersebut merupakan konsekuensi logis dari penyelesaian milestone yang disetujui.

### 2.2 Lingkup Kewenangan Mandiri Agen
Dalam batas ruang lingkup yang disetujui, agen berwenang penuh untuk:
- Menginspeksi pohon repositori, berkas kode, dan dependensi.
- Membuat, mengedit, memindahkan, atau merefaktor berkas proyek sesuai arsitektur kanonikal.
- Menjalankan build, runner tes otomatis, linter, formatter, dan type checker.
- Mengeksekusi perintah pengembangan lokal (migrasi database, inisialisasi lingkungan).
- Menginspeksi status Git, diff, dan branch.
- Memperbaiki kegagalan atau regresi yang terdeteksi.
- Memperbarui 12 berkas stage, dokumen konsistensi, dan berkas sinkronisasi konteks (`docs/context/*`).

### 2.3 Protokol Pemulihan Kegagalan Mandiri (Autonomous Failure Recovery)
Setiap kali terjadi kendala teknis (tes gagal, linter error, validasi tidak lulus):
```text
REPRODUCE → INVESTIGATE → FIX → RE-RUN → VERIFY → CONTINUE
```
Agen tidak boleh menghentikan proses kerja hanya karena menemui kegagalan pada suatu sub-langkah. Lakukan investigasi mandiri, perbaiki akar penyebab, uji ulang hingga lulus, dan lanjutkan penugasan.

---

## 3. Batas Keputusan Pengguna (User Decision Boundary)
Agen dilarang berasumsi atau mengambil keputusan sepihak yang secara eksklusif merupakan hak prerogatif pengguna. Agen WAJIB berhenti dan meminta keputusan pengguna HANYA untuk:
1. Item TBD belum terselesaikan yang dibutuhkan oleh pekerjaan saat ini.
2. Perubahan pada arsitektur atau keputusan yang telah berstatus `LOCKED`.
3. Perluasan ruang lingkup (*scope creep / scope expansion*) ke luar batas milestone aktif.
4. Penambahan kapabilitas eksekusi baru yang berpotensi destruktif.
5. Penggantian dependensi/teknologi fondasi dalam stack baseline.
6. Keputusan terkait lisensi perangkat lunak pihak ketiga.
7. Aksi destruktif permanen di luar ruang lingkup yang disetujui.
8. Persetujuan rilis produksi formal.
9. Ambiguitas keamanan yang tidak dapat diselesaikan melalui prinsip fail-closed.

*Prinsip Kelanjutan Non-Blocking:* Jika suatu komponen terbentur batas keputusan pengguna, lanjutkan pengerjaan bagian lain dalam milestone yang tidak bergantung padanya; jangan memblokir seluruh proses secara tidak perlu.

---

## 4. Perlindungan Keamanan Platform (Platform Security Controls)
Kebijakan otonomi ini tidak pernah memberi hak untuk membypass perlindungan keamanan platform:
- Prompt izin sistem operasi macOS (TCC / accessibility / disk access).
- Otentikasi dan kredensial pengguna.
- Penandatanganan sertifikat Xcode (*code signing*).
- Kebijakan keamanan repositori GitHub dan cloud provider.
- Dialog keamanan dan mekanisme sandbox platform Antigravity.
Keamanan dan integritas sistem selalu diutamakan di atas kenyamanan otonomi.

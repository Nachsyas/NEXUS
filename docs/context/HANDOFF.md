# CONTINUATION HANDOFF — READ FIRST

**Target:** Pengembang atau AI Agent Baru  
**Current State:** Governance Corrective Review / Pre-M0 (Phase 0 in Corrective Pass; M0 Foundation Not Started).  

---

## 1. What Was Just Completed
Fondasi tata kelola NEXUS telah melalui evaluasi korektif menyeluruh:
- Struktur direktori kanonikal target tata kelola telah lengkap (`apps/ios/`, `apps/mac-agent/`, `backend/`, `docs/`, dsb).
- Status scaffold Xcode awal: Scaffold bawaan awal (`Untitled Project.xcodeproj` & `MyApp/`) masih berada di root repositori dan belum dipindahkan/di-rename. Migrasi ke struktur kanonikal `apps/ios/` akan dilakukan pada Milestone M0 Foundation setelah persetujuan tata kelola.
- Tidak ada implementasi produksi NEXUS yang dibuat selama Governance Bootstrap (`0 lines of production code written`).
- Tautan repositori telah dibersihkan menjadi tautan Markdown relatif portabel (0 active Markdown repository links using file:/// remain).
- Kontrak API v1 diperluas lengkap sesuai baseline yang disetujui di 13 domain (60 endpoint terdokumentasi, termasuk 1 convenience endpoint).
- Kontrak data database konseptual diperluas lengkap mencakup 19 entitas konseptual di 9 domain dengan pemisahan semantik mutlak (ADR-012), isolasi user-scoped, UTC timestamps, taksonomi memori 10 tipe kanonikal, sensitivitas (LOW s/d RESTRICTED + NEVER_STORE), dan 6 sumber bukti.
- Asumsi-asumsi teknis yang belum disetujui telah dibersihkan dari status LOCKED dan dipindahkan ke TBD Registry (TBD-020 s/d TBD-026).
- Budget performa dialihkan ke prinsip *Measurement-First* (Baseline = NOT MEASURED, Target = TBD AFTER BASELINE).
- Matriks default permission dipindahkan ke status PROPOSED / TBD-023 dengan tetap mempertahankan tingkat DENY/ASK/ALLOW dan larangan mutlak arbitrary shell.
- Gate SOP-12 dan skill `stage-close` diperkuat penuh mencakup 22 butir kriteria completion gate faktual (12 berkas stage total: 1 README orientasi + 11 artefak bukti).
- Standing Autonomous Execution Policy dan User Decision Boundary dikunci secara kanonikal di `AGENTS.md` dan `docs/SOP/01-development-workflow.md`.

## 2. Aturan Otonomi Milestone (Standing Autonomous Execution Rule)
**PENTING UNTUK AGENT BERIKUTNYA:**
Begitu pengguna secara eksplisit memberikan instruksi untuk memulai Milestone M0:
- Milestone M0 memiliki **otorisasi eksekusi penuh (*standing execution authorization*)**.
- Antigravity wajib melangkah secara otonom melewati seluruh sub-tahap normal M0 (inspeksi, scaffold refactor, migrasi Xcode, setup backend modular monolith, konfigurasi linter/formatter, eksekusi test, dokumentasi stage) **tanpa meminta konfirmasi mikro (*zero micro-confirmations*)**.
- **Kondisi Berhenti (*Stop Conditions*) HANYA berlaku untuk:**
  1. Keputusan pengguna yang benar-benar belum terselesaikan (*genuine unresolved user decision*, misal: pilihan tooling TBD-013/TBD-015/TBD-026);
  2. Dialog izin sistem operasi / platform eksternal yang tidak dapat dihindari (macOS / Xcode / Keychain / TCC);
  3. Ambiguitas keamanan kritis yang tidak dapat diselesaikan via least-privilege;
  4. Penyelesaian atau kegagalan formal seluruh Milestone M0.

## 3. What Is Being Worked On
Menunggu review dan persetujuan formal pengguna atas dokumen tata kelola akhir ini. Belum ada kode implementasi produksi NEXUS yang ditulis. Scaffold Xcode bawaan awal tetap utuh di root repositori.

## 4. DO NOT CHANGE
- Dilarang mengubah arsitektur backend menjadi microservices (ADR-001).
- Dilarang menambahkan kemampuan terminal shell arbitrer ke Mac Agent (ADR-010).
- Dilarang mengubah status item TBD tanpa persetujuan eksplisit pengguna.
- Dilarang menulis kode implementasi produksi NEXUS atau memindahkan/me-rename scaffold Xcode sebelum persetujuan tata kelola dan dibukanya M0.

## 5. Next Exact Task
Menunggu instruksi eksplisit pengguna untuk melangkah ke **Milestone M0: Foundation**. Begitu instruksi diberikan, laksanakan Milestone M0 secara otonom sesuai *Standing Autonomous Execution Policy*.

## 6. Required Reading Before Starting
1. [`AGENTS.md`](../../AGENTS.md)
2. [Documentation Hub](../README.md)
3. [`PROJECT-STATE.md`](PROJECT-STATE.md)

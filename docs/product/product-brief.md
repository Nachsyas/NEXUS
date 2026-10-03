# Product Brief — NEXUS

**Status:** LOCKED  
**Version:** 1.1  

---

## 1. Ringkasan Eksekutif
NEXUS menghadirkan pendamping AI personal yang mengintegrasikan percakapan natural (teks dan suara), personal memory, pemahaman proyek, integrasi vault pengetahuan, kurasi riset radar, serta remote action aman ke komputer Mac pengguna dari iPhone.

## 2. Masalah yang Diselesaikan
- AI chat generik saat ini bersifat stateless, mudah lupa konteks penting, dan terisolasi dari lingkungan kerja nyata pengguna.
- Asisten personal yang ada tidak memiliki pemahaman mendalam tentang proyek engineering pengguna dan tidak dapat mengeksekusi aksi nyata di workstation secara aman.
- Alat remote control yang ada terlalu berbahaya (unrestricted shell) atau terlalu kaku, tanpa audit trail dan mitigasi injeksi prompt.

## 3. Solusi NEXUS
- **Context Engine Terkurasi:** Menggabungkan memori personal, memori proyek, knowledge vault, dan telemetry ke dalam paket konteks berbatas anggaran token (*bounded token budget*).
- **Capability-Based Mac Agent:** Membuka aplikasi, memeriksa status git, memantau service tanpa memberikan akses remote shell bebas.
- **Memory Control Center:** Memberikan antarmuka eksplisit untuk melihat, mengedit, dan melupakan memori.

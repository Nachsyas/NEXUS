# SOP 06 — Security Review Protocol

**Status:** CANONICAL SOP  
**Version:** 1.1  

## Protokol Penilaian Keamanan:
1. Evaluasi dampak aset yang disentuh (Data Pengguna, Sesi Auth, Eksekusi Perangkat).
2. Periksa apakah aksi baru mematuhi prinsip Least Privilege.
3. Pastikan tidak ada cara bagi pengguna untuk mengeksekusi shell arbitrer pada Mac Agent.
4. Verifikasi bahwa semua input dari luar (web capture, dokumen unggahan) disanitasi sebagai DATA.
5. Klasifikasi tingkat risiko: BLOCKING, HIGH, MEDIUM, LOW, INFO.

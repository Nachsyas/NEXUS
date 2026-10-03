# ADR-012: Semantic Separation of Core Data Concepts

**Status:** ACCEPTED  
**Date:** 2026-10-03  

## Context
Pencampuran konsep data (misal menganggap semua pesan chat sebagai memori, atau menganggap hasil web search sebagai knowledge terpercaya) mengaburkan arsitektur dan melemahkan keamanan.

## Decision
Menegakkan pemisahan semantik secara tegas:
- **Memory:** Menyimpan arti (*meaning*), fakta personal/proyek yang lolos kurasi.
- **Knowledge:** Menyimpan dokumen sumber terstruktur milik pengguna (*source documents*).
- **Conversation:** Menyimpan riwayat interaksi sementara (*interaction logs*).
- **Research:** Menyimpan kecerdasan eksternal yang belum diverifikasi pengguna (*external intelligence*).
- **Action:** Menyimpan jejak instruksi eksekusi perangkat (*device execution*).

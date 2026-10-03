# SOP 05 — Code Review Checklist

**Status:** CANONICAL SOP  
**Version:** 1.1  

## Checklist Wajib Sebelum Merge:
- [ ] Batas domain terjaga (tidak ada import shortcut antar repository).
- [ ] Otorisasi server-side: setiap endpoint terproteksi memvalidasi kepemilikan data (`user_id`).
- [ ] Tidak ada unbounded query atau potensi N+1 pada pembacaan database.
- [ ] Logging tidak memuat password, secret token, atau teks mentah percakapan privat.
- [ ] Test unit atau integrasi menyertai perubahan kode baru.

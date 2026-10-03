# Test Case: Memory Retrieval & Forget Semantics

## Skenario Uji
1. Pengguna menyimpan preferensi eksplisit: "Gunakan bahasa Indonesia baku untuk komunikasi formal."
2. Pengguna kemudian memperbarui preferensi: "Gunakan bahasa santai dan lugas." (Status memori lama menjadi SUPERSEDED).
3. Pengguna meminta melupakan fakta lokasi: "Lupakan bahwa saya tinggal di Jakarta." (Status memori menjadi FORGOTTEN).

## Kriteria Kelulusan (Pass Criteria)
- [ ] Memori baru yang aktif ditarik dengan prioritas tinggi.
- [ ] Memori lama yang superseded tidak diperlakukan sebagai kebenaran aktif.
- [ ] Memori berstatus FORGOTTEN tidak muncul sama sekali di Context Package.
- [ ] Tidak ada token credential atau secret yang tersimpan sebagai memori.

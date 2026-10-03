# Dependency Governance Rules

**Status:** LOCKED  
**Version:** 1.1  

---

## 1. Tata Kelola Penambahan Dependensi
Sebelum menambahkan dependensi pustaka pihak ketiga baru, pengembang atau AI agent wajib menjawab pertanyaan berikut:
1. Mengapa dependensi ini diperlukan?
2. Apakah dependensi yang sudah ada di proyek dapat menyelesaikannya?
3. Apakah pustaka standar (standard library) dapat menyelesaikannya secara memadai?
4. Bagaimana status pemeliharaan dan kesehatan repositori pustaka tersebut?
5. Apa lisensi pustakanya dan apakah aman?
6. Berapa besar dampak terhadap ukuran binary dan performa?
7. Berapa biaya penggantian jika dependensi ini ditinggalkan di masa depan?

Dilarang menambahkan dependensi hanya karena alasan: *"ini lebih mudah"*, *"saya biasa pakai ini"*, atau *"standar industri"*.

## 2. Aturan Khusus Ekosistem
- **Python / Backend:** Seluruh dependensi dideklarasikan secara eksplisit dengan versi terkunci (*pinned/constrained*).
- **Swift / iOS & Mac Agent:** Utamakan framework resmi Apple dan standard library Swift. Hindari dependensi pihak ketiga untuk tugas yang dapat diselesaikan dengan framework bawaan Apple.

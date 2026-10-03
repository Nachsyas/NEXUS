# Knowledge Vault Architecture — Secure RAG

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-004, ADR-012  

---

## 1. Alur Pipeline Knowledge
```text
Upload Dokumen (PDF, MD, TXT, Code)
              ↓
  Validasi Ukuran, Tipe & Hash Dedup
              ↓
   Simpan ke Object Storage (S3-Compatible)
              ↓
   Kirim Job ke Asynchronous Worker Queue
              ↓
    Parser & Sanitizer Dokumen
              ↓
  Chunking (dengan metadata halaman/bagian)
              ↓
    Pembuatan Vektor Embedding
              ↓
   Penyimpanan ke pgvector (PostgreSQL)
              ↓
      Status Update: READY
```

## 2. Penanganan Keamanan & Konten Tak Terpercaya
- Dokumen yang diunggah diperlakukan sebagai **DATA**, bukan instruksi sistem yang dapat dieksekusi.
- Sistem resisten terhadap injeksi prompt di dalam dokumen (instruksi dalam dokumen tidak boleh mengubah aturan sistem NEXUS).
- Setiap chunk wajib memiliki metadata: `knowledge_item_id`, `chunk_index`, `page`, `section`, dan `user_id`.

# Security Architecture & Invariants — NEXUS

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-009, ADR-010, ADR-015  

---

## 1. Lima Belas Invarian Keamanan Non-Negotiable
1. **AI Tidak Pernah Bypass Permission Engine:** Keputusan eksekusi diatur oleh kebijakan kode deterministik, bukan oleh output LLM.
2. **LLM Tidak Pernah Mendapatkan Akses Eksekusi OS Langsung:** Tidak ada endpoint evaluasi bash/shell sembarangan yang terhubung ke AI.
3. **Mac Agent Tidak Menerima Perintah Shell Arbitrer:** Seluruh aksi wajib berupa *Capability* terstruktur yang terdaftar secara legal.
4. **Private Key Perangkat Tidak Pernah Meninggalkan Perangkat:** Kunci privat disimpan secara eksklusif di Keychain perangkat lokal.
5. **Perangkat yang Direvoke Dilarang Keras Terhubung Kembali:** Status pencabutan bersifat definitif di server.
6. **Konten Eksternal Tidak Boleh Mengubah Kebijakan Keamanan:** Data riset dan dokumen yang diunggah adalah DATA, bukan instruksi yang berwenang.
7. **Aksi Berisiko Tinggi (HIGH/CRITICAL) Mewajibkan Konfirmasi Eksplisit:** Tidak ada eksekusi diam-diam tanpa persetujuan pengguna.
8. **Seluruh Aksi Bermakna Wajib Memiliki Jejak Audit:** Log audit bersifat *append-only* dan mencatat korelasi lengkap.
9. **Isolasi Mutlak Lintas Pengguna (Multi-Tenancy):** Pengguna A dilarang membaca atau memanipulasi data Pengguna B.
10. **Secret Tidak Boleh Disimpan di General Memory:** Password, token, private key, OTP, dan kredensial disaring sebelum memori disimpan.
11. **Otorisasi Objek Berada di Server-Side:** Klien tidak berhak menentukan izin secara sepihak.
12. **Ambiguitas Keamanan Selalu Gagal Tertutup (*Fail Closed*):** Jika validasi ragu atau data korup, akses ditolak secara default.
13. **Aksi yang Kadaluarsa (*Expired*) Dilarang Dieksekusi:** Setiap envelope aksi membawa batas TTL ketat.
14. **Proteksi Idempotensi Terhadap Duplikasi Aksi:** Aksi yang sama tidak boleh dieksekusi lebih dari satu kali (*nonce / idempotency key*).
15. **Redaksi Informasi Sensitif pada Seluruh Log:** Kredensial, token, dan teks dokumen rahasia wajib disamarkan dalam log observabilitas.

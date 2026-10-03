# Threat Model & Attack Vector Mitigations

**Status:** LOCKED  
**Version:** 1.1  

---

## 1. Pemodelan Ancaman Kunci
| Vektor Ancaman | Dampak Potensial | Mitigasi Wajib NEXUS |
|---|---|---|
| **Prompt Injection via Web/Dokumen** | Memanipulasi LLM untuk mengeksekusi tool jahat | Konten eksternal diperlakukan sebagai DATA semata; LLM bukan pemutus izin eksekusi; evaluasi Permission Engine deterministik di luar LLM. |
| **Pencurian Token Sesi** | Pembajakan akun pengguna | Token akses berumur pendek; token refresh menggunakan rotasi sekali pakai; deteksi reuse otomatis membatalkan seluruh sesi; token disimpan di Keychain. |
| **Kompromi Jaringan (MITM)** | Intersepsi perintah aksi remote | Seluruh lalu lintas terenkripsi TLS (HTTPS / WSS); validasi sertifikat TLS standar dan verifikasi tanda tangan digital aksi. |
| **IDOR / Cross-User Access** | Pengguna A membaca memori/proyek Pengguna B | Validasi server-side wajib menyertakan filter `user_id` yang diambil dari token sesi terverifikasi pada setiap query DB. |
| **Replay Attack pada Aksi Mac** | Eksekusi berulang terhadap perintah lama | Setiap envelope aksi membawa `action_id`, `idempotency_key`, timestamp UTC, dan batas kadaluarsa `expires_at` (konfigurasi window & TTL: TBD-021). |
| **Pencurian Perangkat Mac** | Penyalahgunaan kredensial Mac Agent | Kunci privat disimpan di macOS Keychain / secure local storage lokal; pengguna dapat melakukan instant remote revocation (`/devices/{id}/revoke`). |
| **Bocoran Secret ke General Memory** | Paparan API key / password di prompt | Filter sensitivitas otomatis menyaring format kunci rahasia, token, password, dan OTP sebelum data disimpan ke database memori. |

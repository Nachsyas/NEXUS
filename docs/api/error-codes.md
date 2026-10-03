# Standard Error Codes — NEXUS

**Status:** LOCKED  
**Version:** 1.1  

---

| Error Code | HTTP Status | Penjelasan |
|---|---|---|
| `AUTH_INVALID_CREDENTIALS` | 401 | Kredensial login atau token sesi tidak valid |
| `AUTH_TOKEN_EXPIRED` | 401 | Access token telah kadaluarsa |
| `AUTH_REFRESH_TOKEN_REUSED` | 401 | Deteksi penggunaan ulang refresh token (sesi dibatalkan) |
| `FORBIDDEN_ACCESS` | 403 | Pengguna tidak memiliki hak akses ke resource ini |
| `DEVICE_NOT_FOUND` | 404 | Perangkat tidak terdaftar di database |
| `DEVICE_REVOKED` | 403 | Akses perangkat telah dicabut secara permanen |
| `DEVICE_OFFLINE` | 503 | Mac Agent tidak sedang terhubung ke gerbang realtime |
| `UNSUPPORTED_ACTION` | 400 | Aksi yang diminta tidak termasuk dalam daftar capability resmi |
| `ACTION_DENIED` | 403 | Aksi ditolak oleh Permission Engine |
| `ACTION_CONFIRMATION_REQUIRED` | 400 | Aksi berisiko tinggi mewajibkan konfirmasi pengguna |
| `ACTION_EXPIRED` | 400 | Waktu toleransi eksekusi aksi telah kadaluarsa |
| `ACTION_DUPLICATE` | 409 | Aksi dengan idempotency key yang sama sudah diproses |
| `MEMORY_NOT_FOUND` | 404 | ID memori tidak ditemukan |
| `PROJECT_NOT_FOUND` | 404 | ID proyek tidak ditemukan atau bukan milik pengguna |
| `KNOWLEDGE_PROCESSING_FAILED` | 500 | Pemrosesan ekstraksi atau chunking dokumen gagal |
| `AI_PROVIDER_UNAVAILABLE` | 502 | Provider model AI eksternal sedang mengalami gangguan |
| `VALIDATION_ERROR` | 422 | Skema payload permintaan tidak memenuhi aturan Pydantic |

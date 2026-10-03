# Device Trust & Lifecycle Model

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-007, ADR-008, ADR-009  

---

## 1. Pemisahan Trust State vs. Presence State
Dilarang keras mencampuradukkan status kepercayaan (*Trust*) dengan status kehadiran jaringan (*Presence*):

### Trust State (Persisten di Database)
- `PENDING_PAIRING`: Kode pairing telah dibuat namun belum diklaim oleh agen.
- `PAIRED`: Perangkat telah terverifikasi, keypair terdaftar, dan dipercaya.
- `REVOKED`: Hak akses perangkat telah dicabut permanen oleh pengguna.

### Presence State (Efemeral di Redis / Runtime)
- `ONLINE`: Perangkat aktif terhubung dan merespons heartbeat WSS.
- `STALE`: Heartbeat terlambat diterima melampaui ambang batas toleransi (konfigurasi ambang: TBD-022).
- `OFFLINE`: Koneksi WebSocket terputus atau melebihi batas waktu timeout (konfigurasi batas waktu: TBD-022).
- `UNKNOWN`: Kondisi perangkat belum dapat ditentukan.

> **PENTING: OFFLINE ≠ REVOKED. ONLINE ≠ OTOMATIS DIPERCAYA.**

## 2. Protokol Pairing Perangkat
1. Pengguna terotentikasi meminta pairing code melalui aplikasi iOS (`POST /api/v1/devices/pairing`).
2. Server membuat kode numerik/alfanumerik jangka pendek sekali pakai (*short-lived one-time code*, durasi TTL dan batas replay dikonfigurasi via TBD-021).
3. Pengguna memasukkan kode tersebut pada Mac Agent lokal.
4. Mac Agent menginisiasi pembuatan asymmetric key pair lokal di mana private key tetap berada di macOS Keychain / secure local storage dan tidak pernah ditransmisikan.
5. Mac Agent mengklaim kode ke server (`POST /api/v1/devices/pairing/claim`) bersamaan dengan public key yang terdaftar dan identitas kapabilitas. Mekanisme authenticated challenge/response atau skema verifikasi safe digunakan untuk memvalidasi kepemilikan keypair (skema signing & algoritma: TBD-020).
6. Server mencocokkan kepemilikan user, memvalidasi klaim dengan proteksi replay, dan menandai perangkat sebagai `PAIRED`.

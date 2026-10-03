# Action Risk Model & Lifecycle

**Status:** LOCKED CANONICAL ARCHITECTURE  
**Version:** 1.2  
**Decision Reference:** ADR-009, ADR-015  

---

## 1. Tingkat Risiko Aksi (Risk Levels)
Setiap aksi diklasifikasikan ke dalam 4 tingkatan risiko deterministik:
- `LOW`: Aksi read-only atau observasi non-destruktif (misal: cek status baterai, status git).
- `MEDIUM`: Aksi navigasi atau membuka aplikasi resmi yang terdaftar (misal: membuka aplikasi terdaftar, membuka folder proyek).
- `HIGH`: Aksi yang mengubah state sistem atau service (misal: menyalakan atau mematikan background service lokal). Mewajibkan konfirmasi eksplisit dari pengguna.
- `CRITICAL`: Aksi destruktif atau pengubahan konfigurasi mendasar. Mayoritas aksi ini tidak didukung di Phase 1 dan ditolak secara default.

*Catatan Tata Kelola: Pemetaan formal tingkat risiko untuk setiap capability spesifik dievaluasi dan dikunci via TBD-024 sebelum Milestone M8 Remote Safe Actions.*

---

## 2. Siklus Hidup Aksi (Canonical 11-State Action Lifecycle)
Siklus hidup status entitas `Action` dikontrol secara ketat melalui 11 status resmi:
1. `REQUESTED`: Permintaan aksi baru dibuat dan diterima oleh backend.
2. `AWAITING_CONFIRMATION`: Aksi berisiko (evaluasi ASK) ditahan menunggu persetujuan pengguna.
3. `QUEUED`: Aksi telah diizinkan (atau dikonfirmasi pengguna) dan siap dikirim ke antrian dispatch.
4. `DISPATCHED`: Perintah aksi telah dikirimkan melalui saluran WSS ke Mac Agent.
5. `ACCEPTED`: Mac Agent menerima dan memvalidasi perintah (`ACTION_ACCEPTED` realtime event).
6. `RUNNING`: Mac Agent sedang mengeksekusi instruksi native secara lokal.
7. `SUCCEEDED`: Eksekusi selesai dengan sukses dan hasil dikembalikan ke backend.
8. `FAILED`: Eksekusi gagal menghasilkan output atau terjadi error lokal pada Mac Agent.
9. `CANCELLED`: Dibatalkan oleh pengguna sebelum atau selama eksekusi berjalan.
10. `EXPIRED`: Batas waktu toleransi aksi / TTL terlampaui sebelum aksi selesai dieksekusi.
11. `REJECTED`: Ditolak oleh Permission Engine lokal atau validasi schema agen karena melanggar kebijakan keamanan.

### Diagram Transisi Status
```text
       REQUESTED
           │
           ▼
 ┌───────────────────┐
 │ Memerlukan        │──Ya──► AWAITING_CONFIRMATION
 │ Konfirmasi?       │                │
 └─────────┬─────────┘        (Disetujui Pengguna)
           │                          │
          Tidak                       ▼
           └─────────────────────► QUEUED
                                      │
                                      ▼
                                  DISPATCHED
                                      │
                                      ▼
                                   ACCEPTED
                                      │
                                      ▼
                                   RUNNING
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                     SUCCEEDED                   FAILED

(State Terminal Lain: CANCELLED, EXPIRED, REJECTED)
```

### Aturan Semantik Kunci
- **Event Konfirmasi:** Konfirmasi dari pengguna bukan status terpisah (`CONFIRMED`), melainkan transisi: `AWAITING_CONFIRMATION -> (konfirmasi pengguna) -> QUEUED`.
- **Timeout / Kedaluwarsa:** Bila aksi melebihi TTL yang ditentukan, aksi bertransisi menjadi `EXPIRED`.
- **Jabat Tangan Agen:** Saat agen merespons dengan event realtime `ACTION_ACCEPTED`, entitas aksi di database beralih ke status `ACCEPTED`.

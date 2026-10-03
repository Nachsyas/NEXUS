# WebSocket Protocol — Client Gateway

**Status:** LOCKED  
**Version:** 1.1  
**URL:** `/api/v1/realtime/ws`  

---

## 1. Format Pesan Masuk & Keluar
Setiap frame WebSocket wajib berupa teks JSON yang mematuhi skema dasar berikut:
```json
{
  "protocol_version": "1.0",
  "message_id": "018f3a54-72b1-789a-bc01-23456789abcd",
  "message_type": "AI_RESPONSE_DELTA",
  "timestamp": "2026-10-03T07:17:40Z",
  "correlation_id": "req-9876",
  "payload": {}
}
```

## 2. Tipe Pesan Utama Menuju iOS Client
- `AI_RESPONSE_DELTA`: Potongan token teks jawaban streaming AI.
- `AI_RESPONSE_COMPLETE`: Jawaban AI selesai beserta metadata token.
- `ACTION_STARTED`: Perangkat target mulai memproses aksi yang didelegasikan.
- `ACTION_PROGRESS`: Progres eksekusi aksi (persentase / step info).
- `ACTION_COMPLETED`: Hasil eksekusi aksi safe sukses.
- `ACTION_FAILED`: Eksekusi aksi gagal beserta kode error terstruktur.
- `DEVICE_ONLINE` / `DEVICE_OFFLINE`: Notifikasi perubahan status kehadiran perangkat.
- `KNOWLEDGE_PROCESSING` / `KNOWLEDGE_READY`: Status indexing dokumen vault.

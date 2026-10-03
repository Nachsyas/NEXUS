# Mac Agent Protocol — Execution Node WSS

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-008, ADR-009, ADR-010  

---

## 1. Handshake Awal (AGENT_HELLO)
Saat terhubung via WSS, Mac Agent wajib mengirimkan pesan jabat tangan awal:
```json
{
  "protocol_version": "1.0",
  "message_id": "uuid-hello",
  "message_type": "AGENT_HELLO",
  "timestamp": "2026-10-03T07:17:40Z",
  "payload": {
    "device_id": "dev-mac-1234",
    "agent_version": "1.0.0",
    "platform_version": "macOS 15.0",
    "capabilities": [
      "GET_DEVICE_STATUS",
      "OPEN_APPLICATION",
      "OPEN_PROJECT",
      "GET_GIT_STATUS",
      "GET_SERVICE_STATUS",
      "START_APPROVED_SERVICE",
      "STOP_APPROVED_SERVICE",
      "GET_APPROVED_LOGS"
    ]
  }
}
```

Respons Backend:
- `AGENT_ACCEPTED`: Jabat tangan disetujui, sesi aktif dimulai.
- `REJECT_REVOKED_DEVICE`: Perangkat telah dicabut izinnya.
- `REJECT_INCOMPATIBLE_VERSION`: Versi protokol tidak didukung.

## 2. Heartbeat & Dispatch
- `HEARTBEAT`: Dikirim oleh Mac Agent secara periodik (interval detak ringan terkonfigurasi, lihat TBD-022) untuk konfirmasi status aktif.
- `EXECUTE_ACTION`: Dikirim backend untuk menginstruksikan eksekusi capability tertentu yang telah lolos otorisasi.
- `ACTION_ACCEPTED` / `ACTION_RESULT`: Respon Mac Agent melaporkan penerimaan dan hasil eksekusi aksi.
- **Resiliensi Protokol:** Mendukung *bounded reconnect* dengan exponential backoff dan jitter, validasi sesi, resinkronisasi status pasca putus koneksi, dan proteksi duplikasi pesan.

# Realtime Architecture — WebSocket Protocols

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-008  

---

## 1. Gerbang Realtime
Komunikasi realtime menggunakan WebSocket terenkripsi (WSS) untuk melayani dua jenis klien:
1. **iOS Client:** Menerima delta respons teks streaming AI, pembaruan status aksi perangkat, dan status presence.
2. **Mac Agent:** Menerima perintah dispatch aksi berizin dan mengirimkan telemetry, heartbeat, serta progres aksi.

## 2. Struktur Envelope Pesan Realtime
```json
{
  "protocol_version": "1.0",
  "message_id": "uuid-v4-or-v7",
  "message_type": "EVENT_OR_COMMAND_TYPE",
  "timestamp": "2026-10-03T07:17:40Z",
  "correlation_id": "req-uuid",
  "payload": {}
}
```

## 3. Resiliensi Koneksi & Konfigurasi Realtime
- **Lightweight Heartbeat:** Mekanisme detak jantung periodik ringan antara klien/agen dan backend gateway untuk memelihara koneksi aktif dan mendeteksi kondisi mati mendadak (interval detak, stale threshold, dan timeout bersifat terkonfigurasi, lihat TBD-022).
- **Bounded Reconnect:** Rekoneksi otomatis terikat batas menggunakan *Exponential Backoff dengan Random Jitter* guna mencegah sambungan berulang tak terbatas dan reconnection storm.
- **Session Validation:** Validasi token otentikasi dan status trust perangkat pada saat jabat tangan (handshake) dan secara berkala saat penyambungan ulang.
- **State Resynchronization:** Saat koneksi pulih setelah terputus, klien dan server melakukan resinkronisasi status (pending action states, missed presence updates) untuk menjamin konsistensi.
- **Duplicate Protection:** Setiap pesan WSS membawa `message_id` unik untuk menjamin pemrosesan idempoten dan mencegah duplikasi pesan pada lapisan transport.

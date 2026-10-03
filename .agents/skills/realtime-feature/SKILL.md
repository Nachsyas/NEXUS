# Skill: realtime-feature

## 1. Description
Menambahkan event stream baru pada gerbang WebSocket klien atau agen.

## 2. When Used
Saat mengimplementasikan streaming AI, telemetry, atau status aksi.

## 3. Prerequisites
Format envelope realtime `docs/api/websocket-protocol.md` telah dipatuhi.

## 4. Required Docs
- `docs/architecture/realtime-architecture.md`
- `docs/api/websocket-protocol.md`

## 5. Workflow
1. Definisikan tipe event baru dan skema payload-nya.
2. Terapkan serialisasi dan deserialisasi JSON yang aman.
3. Tangani kasus koneksi terputus dan antrian pesan yang hilang.
4. Buat tes integrasi WebSocket client-server.

## 6. Validation
Uji ketahanan rekoneksi otomatis dengan simulasi jaringan terputus.

## 7. Docs Update
Perbarui daftar event di `docs/api/websocket-protocol.md`.

## 8. Stop Conditions
Berhenti jika pengiriman event realtime memblokir thread worker utama.

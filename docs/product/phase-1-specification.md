# Phase 1 Specification — NEXUS Core

**Status:** LOCKED  
**Version:** 1.1  
**Tema:** *NEXUS knows, remembers, understands, and performs basic actions.*

---

## 1. Ruang Lingkup Fitur Phase 1
1. **Account & Identity:** Sign in with Apple, pemisahan entitas user dan auth identity, rotasi session token, Keychain storage.
2. **iOS Client:** Antarmuka SwiftUI modern (Home, Intelligence, NEXUS Orb, Memory, Devices), streaming respons, tap-to-talk voice, offline state handling.
3. **Text & Voice Interaction:** Streaming chat via WebSocket (WSS), tap-to-talk voice dengan AVFoundation, visible listening UI.
4. **Personal & Project Memory:** Klasifikasi fakta personal & proyek, sensitivity check, deduplikasi, supersession, POST `/memories/{id}/forget`.
5. **Context Engine V1:** Intent extraction, entity resolution, active project context, ranking terarah, bounded token budget, eliminasi memori terlupakan/usang.
6. **Knowledge Vault:** Upload dokumen (PDF, MD, TXT, Code), parsing asinkron, chunking, embeddings, pgvector store, RAG search dengan sitasi valid.
7. **Research Radar V1:** Ingesti feed AI/tech, normalisasi, summarization, relevansi personal, feed sementara (save to knowledge vault opsional).
8. **Device Pairing & Mac Agent V1:** Pairing code sekali pakai, asymmetric keypair lokal di Mac Keychain / secure local storage (algoritma kriptografi: TBD-020), WSS outbound persist, heartbeat periodik terkonfigurasi & presence telemetry.
9. **Remote Safe Actions:** 8 capability Mac terdaftar (GET_DEVICE_STATUS, OPEN_APPLICATION, OPEN_PROJECT, GET_GIT_STATUS, GET_SERVICE_STATUS, START_APPROVED_SERVICE, STOP_APPROVED_SERVICE, GET_APPROVED_LOGS).
10. **Permission Engine & Risk Model:** Model DENY / ASK / ALLOW, klasifikasi risiko LOW / MEDIUM / HIGH / CRITICAL, approval gate pada aksi berisiko, emergency kill switch.
11. **Audit Trail & Observability:** Pencatatan setiap aksi, korelasi request_id / action_id, metrik performa latency dan AI evaluation baseline.

## 2. Explicit Non-Goals Phase 1
- Full Remote Desktop
- Arbitrary Terminal / Unrestricted Shell
- HealthKit / Garmin / Smart Home
- Financial Execution / Autonomous Destructive Action
- 24/7 Always-listening cloud microphone
- Multi-agent autonomous loops

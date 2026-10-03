# System Overview — NEXUS Architecture

**Status:** LOCKED  
**Version:** 1.1  
**Source of Truth:** Prompt Master v1.1  

---

## 1. Topologi Sistem Tingkat Tinggi
NEXUS dirancang sebagai ekosistem kecerdasan personal multi-komponen yang berkoordinasi secara aman dan asinkron:

```text
                     NEXUS

               PERSONAL AI CORE
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     MEMORY         CONTEXT       REASONING
        │              │              │
        └──────────────┼──────────────┘
                       │
                 ORCHESTRATION
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   PERCEPTION       AWARENESS       ACTION
        │              │              │
   Voice/Text        Projects       Devices
   Documents         Research       Apps
   Sensors           Device State   Services
                       │
                       ▼
                    PRESENCE
                       │
              iPhone / Mac / Future
```

## 2. Komponen Utama
1. **iOS Client (Interaksi & Endpoint Personal):**
   - Dibangun dengan Swift dan SwiftUI murni.
   - Bertindak sebagai antarmuka interaksi utama (teks, suara, kontrol memori, status perangkat).
   - Berkomunikasi dengan Backend via HTTPS REST API dan WebSocket (WSS).
2. **NEXUS Core Backend (Modular Monolith):**
   - Dibangun dengan Python dan FastAPI.
   - Mengelola otentikasi, perutean model AI, mesin konteks, orkestrasi aksi, dan audit trail.
   - Menggunakan PostgreSQL sebagai primary persistent database dan pgvector untuk pencarian semantik vektor.
   - Menggunakan Redis untuk presence, rate limiting, pub/sub realtime, dan state efemeral.
   - Didukung worker asinkron untuk tugas berat (chunking, embedding, scraping riset).
3. **Mac Agent (Secure Execution Node):**
   - Aplikasi Swift native untuk macOS (menu bar background agent).
   - Menghubungkan diri ke backend via koneksi outbound WebSocket persisten (WSS).
   - Menjalankan aksi yang divalidasi secara lokal berbasis kemampuan (*capability-based execution*).
   - Menyimpan kredensial pasangan perangkat di macOS Keychain.

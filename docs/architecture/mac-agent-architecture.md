# Mac Agent Architecture — Secure Execution Node

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-007, ADR-008, ADR-009, ADR-010  

---

## 1. Peran & Tanggung Jawab
Mac Agent adalah **Secure Execution Node**, BUKAN remote shell. Agent ini berjalan sebagai aplikasi native macOS (menu bar utility) yang menghubungkan workstation Mac ke ekosistem NEXUS.

## 2. Komponen Internal
```text
                   Backend WebSocket Gateway
                              │  ▲ (Outbound WSS)
                              ▼  │
┌─────────────────────────────────────────────────────────────┐
│                       Mac Agent                             │
│                                                             │
│   ┌─────────────────────┐       ┌───────────────────────┐   │
│   │  ConnectionManager  │       │   HeartbeatManager    │   │
│   └──────────┬──────────┘       └───────────┬───────────┘   │
│              ▼                              ▼               │
│   ┌─────────────────────┐       ┌───────────────────────┐   │
│   │   ActionValidator   │◄──────┤   LocalPolicyEngine   │   │
│   └──────────┬──────────┘       └───────────────────────┘   │
│              ▼                                              │
│   ┌─────────────────────┐       ┌───────────────────────┐   │
│   │  ActionDispatcher   │──────►│  CapabilityRegistry   │   │
│   └─────────────────────┘       └───────────┬───────────┘   │
│                                             ▼               │
│                                 ┌───────────────────────┐   │
│                                 │ Capability Handler    │   │
│                                 │ (Native Apple APIs)   │   │
│                                 └───────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 3. Protokol Keamanan Lokal
- **Outbound WSS Only:** Mac Agent tidak membuka port listening inbound; koneksi selalu diinisiasi keluar menuju backend.
- **Kredensial:** Keypair kriptografis disimpan di macOS Keychain / secure local storage lokal (algoritma signing & skema: TBD-020). Private key tidak pernah meninggalkan Mac.
- **Local Policy & Kill Switch:** Pengguna di Mac dapat memencet tombol "Pause Remote Actions", "Disconnect", atau "Quit Agent" secara lokal kapan saja.
- **Capability Scoped:** Hanya 8 aksi safe yang diperbolehkan di Phase 1. Semua payload lain ditolak (*Unsupported Action*).

# Mac Agent Architecture — Secure Execution Node

**Status:** LOCKED  
**Version:** 1.2  
**Decision Reference:** ADR-007, ADR-008, ADR-009, ADR-010, TBD-027  

---

## 1. Peran & Tanggung Jawab
Mac Agent adalah **Secure Execution Node**, BUKAN remote shell. Agent ini berjalan sebagai aplikasi native macOS (menu bar utility) yang menghubungkan workstation Mac ke ekosistem NEXUS.

NEXUS iOS Client dan NEXUS Mac Agent adalah node produk terpisah secara arsitektural. Keberadaan build Mac-compatible dari target iOS/Catalyst tidak boleh diperlakukan sebagai pengganti NEXUS Mac Agent.

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

## 4. Packaging Lifecycle: Foundation Executable vs Phase 1 App Packaging
- **M0 Foundation Packaging:** Executable berbasis Swift Package (`apps/mac-agent/Package.swift`). Bentuk ini berfungsi sebagai kerangka eksekusi dasar (*foundation executable*) untuk memvalidasi build, struktur modul (`AgentCore`, `Capabilities`, `Security`, `Realtime`), dan boundary tanpa shell arbitrer.
- **Phase 1 Final Packaging (TBD-027):** Belum dikunci oleh M0 (*NOT YET LOCKED BY M0*). Sebelum kapabilitas sistem dan pairing perangkat diimplementasikan pada M6/M7, arsitektur harus mengevaluasi format packaging macOS resmi (misal: macOS App Bundle `.app` dengan menu bar status item via `NSStatusItem` / SwiftUI `MenuBarExtra`) yang diperlukan untuk integrasi macOS Keychain, izin TCC (Transparency, Consent, and Control), siklus hidup aplikasi (launch at login, background daemon/agent), kontrol visual lokal pengguna, dan kill switch.

# iOS Architecture — NEXUS Client

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-006  

---

## 1. Arsitektur Presentasi & Logika
Aplikasi iOS dibangun menggunakan Swift modern dan SwiftUI, mengikuti pola arsitektur MVVM / Clean Architecture dengan isolasi konkurensi Swift (Structured Concurrency):

```text
Presentation Layer (SwiftUI Views & ViewModels)
   ↓
Domain Layer (Use Cases & Business Entities)
   ↓
Data Layer (Repositories, API Client, Local Cache)
   ├── Remote (URLSession REST & URLSessionWebSocketTask)
   └── Local (SwiftData Cache & Keychain Services)
```

## 2. Penggunaan SwiftData
- SwiftData **HANYA** digunakan untuk caching lokal, metadata baru, antrian offline yang terikat batas (*bounded offline sync queue*), dan state antarmuka.
- SwiftData **BUKAN** sumber kebenaran permanen untuk Memori NEXUS. Backend PostgreSQL adalah authoritative source of truth.

## 3. Fitur Utama iOS
- **NEXUS Orb:** Representasi visual state AI (idle, listening, thinking, executing, success, error).
- **Navigation Tabs:** Home, Intelligence, NEXUS (Percakapan), Memory, Devices.
- **Audio & Input:** Tap-to-talk dengan AVFoundation, visualisasi gelombang suara, transkripsi real-time.
- **Integrasi Sistem:** App Intents dan Siri Shortcuts untuk Quick Capture dan tombol aksi (Action Button).

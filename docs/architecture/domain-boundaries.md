# Domain Boundaries & Dependency Rules

**Status:** LOCKED  
**Version:** 1.1  

---

## 1. Daftar Domain Inti Backend
Backend NEXUS diorganisir sebagai Modular Monolith dengan batas domain yang tegas:

1. `auth`: Pengelolaan identitas Sign in with Apple, sesi JWT, refresh token rotation.
2. `users`: Profil pengguna dan preferensi personal.
3. `projects`: Pengelolaan proyek kerja aktif, teknologi, dan konteks proyek.
4. `memory`: Penyimpanan dan kurasi memori jangka panjang (Personal & Project facts).
5. `context`: Mesin perakit paket konteks berbatas anggaran token (Context Engine).
6. `conversations`: Pengelolaan sesi obrolan, riwayat pesan, dan Private Session.
7. `knowledge`: Knowledge Vault, upload dokumen, ekstraksi teks, embedding, dan RAG.
8. `research`: Ingesti riset eksternal, kurasi berita AI/teknologi, dan integrasi minat.
9. `devices`: Registrasi perangkat, pairing handshake, pemantauan status kehadiran.
10. `actions`: Mesin orkestrasi aksi, validasi envelope aksi, dan pelacakan siklus hidup aksi.
11. `permissions`: Penegakan kebijakan izin (DENY, ASK, ALLOW) dan manajemen risiko.
12. `audit`: Pencatatan log peristiwa audit yang aman dan append-only.
13. `ai`: Abstraksi LLM Provider, Model Router, dan tool-calling schemas.
14. `realtime`: Gerbang WebSocket untuk streaming respons AI, presence, dan telemetry.

## 2. Aturan Aliran Ketergantungan (Cross-Domain Rules)
Aliran ketergantungan standar di dalam setiap domain:
```text
Transport (Router / WebSocket Gateway)
   ↓
Application Service
   ↓
Domain Logic / Interfaces / Entities
   ↓
Infrastructure Adapter / Repository
```

### Aturan Non-Negotiable:
- **Dilarang Direct Repository Shortcut:** Domain A dilarang mengakses Repository Domain B secara langsung (misalnya `MemoryService` langsung mengimpor `DeviceRepository`).
- Kolaborasi lintas domain wajib melalui `Application Service` domain tujuan atau via event bus/abstraksi antarmuka yang disetujui.
- Router hanya bertanggung jawab atas validasi request dan serialisasi respons.
- Repository hanya bertanggung jawab atas persistensi data, dilarang mengandung logika bisnis.

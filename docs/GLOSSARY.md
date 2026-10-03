# Glossary of Terms — NEXUS

Daftar definisi istilah resmi dalam ekosistem NEXUS:

- **NEXUS:** Sistem pendamping kecerdasan personal (*Personal AI Companion & Intelligence Ecosystem*).
- **NEXUS Core:** Layanan backend modular monolith yang mengorkestrasi identitas, memori, konteks, dan kecerdasan.
- **Endpoint:** Perangkat fisik atau antarmuka tempat pengguna berinteraksi dengan NEXUS (misal: iPhone, Mac).
- **Mac Agent:** Secure execution node lokal di macOS yang menjalankan aksi yang disetujui secara aman.
- **Personal Memory:** Memori jangka panjang mengenai fakta personal, preferensi, dan kebiasaan pengguna.
- **Project Memory:** Memori terisolasi mengenai keputusan arsitektur, progres, dan fakta sebuah proyek kerja.
- **Knowledge Vault:** Penyimpanan dokumen sumber pengguna (PDF, Catatan, Kode) yang diindeks untuk RAG semantik.
- **Research Radar:** Ingesti berita dan riset eksternal yang dianalisis relevansinya terhadap minat pengguna.
- **Context Engine:** Mesin pengumpul dan penyaring informasi relevan ke dalam paket konteks berbatas anggaran token.
- **Capability:** Kemampuan eksekusi terstruktur yang diizinkan pada perangkat (bukan shell sembarangan).
- **Permission Engine:** Mesin deterministik di luar LLM yang menegakkan izin (DENY, ASK, ALLOW).
- **Trust State:** Status kepercayaan persisten perangkat (PENDING_PAIRING, PAIRED, REVOKED).
- **Presence State:** Status kehadiran jaringan runtime perangkat (ONLINE, STALE, OFFLINE, UNKNOWN).
- **Private Session:** Sesi obrolan sementara tanpa persistensi memori dan tanpa pembelajaran perilaku.

> **PENTING:**
> - Memory ≠ Knowledge
> - Memory ≠ Conversation
> - Research ≠ Knowledge (sampai disimpan secara eksplisit oleh pengguna)
> - Action ≠ Jawaban AI
> - Device Presence ≠ Device Trust Identity
> - Permission ≠ Capability

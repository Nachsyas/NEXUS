# Database Architecture & Data Contracts

**Status:** LOCKED CANONICAL ARCHITECTURE  
**Version:** 1.3  
**Decision Reference:** ADR-002, ADR-012  

---

## 1. Prinsip Utama Desain Data
1. **Source of Truth:** PostgreSQL (+ pgvector) adalah single source of truth untuk seluruh state permanen NEXUS.
2. **Pemisahan Semantik Mutlak (ADR-012):**
   - *Memories* menyimpan nilai semantik personal/proyek yang terkualifikasi dan divalidasi.
   - *Conversations/Messages* menyimpan riwayat interaksi dialog interaktif.
   - *Knowledge Vault* menyimpan dokumen referensi berdensitas tinggi (eksternal/proyek).
   - *Research Items* menyimpan kurasi radar teknologi/paper eksternal.
3. **Data Minimization & User Scoping:** Seluruh data terikat kuat pada `user_id` untuk menjamin multi-tenancy yang aman dan mencegah IDOR.
4. **Waktu Kanonikal:** Seluruh timestamp wajib disimpan dalam zona waktu UTC (`TIMESTAMPTZ`).

---

## 2. Kontrak Data Konseptual (19 Entitas Konseptual di 9 Domain)

### 2.1 Identity & User Domain

#### `users`
- **Tujuan:** Entitas inti pengguna sistem sebagai jangkar identitas internal.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `display_name`: string
  - `status`: string (ACTIVE | SUSPENDED | DELETED)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
  - `last_login_at`: UTC timestamp (nullable)
- **Semantik:** Entitas `users` sengaja independen dari alamat email provider autentikasi eksternal. Email login eksternal, provider subject ID, dan token pihak ketiga dikelola secara terisolasi pada `auth_identities`.

#### `auth_identities`
- **Tujuan:** Pemetaan akun penyedia autentikasi eksternal (Sign in with Apple, OAuth provider) ke pengguna internal.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `provider`: string (misal: APPLE)
  - `provider_subject`: string (identifier unik stabil dari provider)
  - `email`: string (nullable, klaim email dari provider bila dibagikan)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
  - `last_verified_at`: UTC timestamp (nullable)
- **Semantik:** Mengisolasi identitas autentikasi eksternal dari entitas pengguna inti, memungkinkan migrasi atau penambahan provider di masa mendatang.

#### `user_preferences`
- **Tujuan:** Konfigurasi personalisasi pengguna dalam berinteraksi dengan NEXUS.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id, Unique)
  - `language`: string (default bahasa respons)
  - `response_detail`: string (CONCISE | DETAILED | TECHNICAL)
  - `interaction_style`: string (DIRECT | EXPLORATORY)
  - `proactivity_level`: string (LOW | MEDIUM | HIGH)
  - `default_project_id`: UUID (Foreign Key -> projects.id, nullable)
  - `default_device_id`: UUID (Foreign Key -> devices.id, nullable)
  - `storage_mode`: string (nullable)
  - `research_update_frequency`: string (nullable)
  - `notification_preferences`: JSON
  - `voice_settings`: JSON (opsional / preferensi audio terkonfigurasi)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
- **Semantik:** Mengontrol preferensi interaksi dan pembentukan konteks AI tanpa mencampuri profil identitas dasar pengguna.

---

### 2.2 Project Domain

#### `projects`
- **Tujuan:** Konteks kerja spesifik (ide, riset, atau implementasi software) yang membatasi memori dan pengetahuan teknis.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `name`: string
  - `slug`: string (nullable)
  - `description`: string
  - `status`: string (IDEA | PLANNING | ACTIVE | PAUSED | COMPLETED | ARCHIVED)
  - `priority`: string / integer (nullable)
  - `is_active`: boolean (penanda fokus proyek aktif saat ini)
  - `summary`: string (nullable, ringkasan status arsitektural)
  - `progress`: float / integer (nullable, persentase penyelesaian)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
  - `archived_at`: UTC timestamp (nullable)
- **Semantik:** Menjadi batas isolasi konteks (*context boundary*) mutlak untuk mencegah kebocoran antar proyek (*zero cross-project leakage*).

#### `project_technologies`
- **Tujuan:** Daftar teknologi, framework, pustaka, dan bahasa pemrograman yang digunakan pada sebuah proyek.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `project_id`: UUID (Foreign Key -> projects.id)
  - `name`: string
  - `category`: string (nullable)
  - `version`: string (nullable)
  - `metadata`: JSON (nullable)
- **Semantik:** Digunakan oleh Context Engine untuk meningkatkan relevansi saran teknis dan penalaran kode.

---

### 2.3 Memory Domain

#### `memories`
- **Tujuan:** Penyimpanan memori personal dan proyek yang terstruktur semantik, dinamis, berevolusi, dan dapat diverifikasi.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `project_id`: UUID (Foreign Key -> projects.id, nullable untuk memori global)
  - `memory_type`: string (PERSONAL_FACT | PREFERENCE | INTEREST | SKILL | GOAL | PROJECT_FACT | PROJECT_DECISION | PROJECT_PROGRESS | PROJECT_NEXT_ACTION | BEHAVIOR_PATTERN)
  - `subject`: string (entitas/subjek memori)
  - `predicate`: string (relasi/atribut)
  - `value_text`: string (representasi teks nilai fakta)
  - `value_json`: JSON (nullable, data terstruktur pelengkap)
  - `summary`: string (ringkasan memori untuk prompt injection hemat token)
  - `embedding`: vector (representasi embedding untuk retrieval semantik)
  - `importance`: float (skor kepentingan fakta 0.0 - 1.0)
  - `confidence`: float (skor keyakinan fakta 0.0 - 1.0)
  - `sensitivity`: string (LOW | MEDIUM | HIGH | RESTRICTED)
  - `source_type`: string (CONVERSATION | USER_EXPLICIT | PROJECT_UPDATE | DOCUMENT | SYSTEM_INFERENCE | BEHAVIORAL_INFERENCE)
  - `source_id`: string (nullable, UUID pesan atau referensi dokumen sumber)
  - `status`: string (ACTIVE | SUPERSEDED | EXPIRED | FORGOTTEN | PENDING_CONFIRMATION)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
  - `expires_at`: UTC timestamp (nullable, waktu kedaluwarsa memori sementara)
  - `superseded_by`: UUID (Foreign Key -> memories.id, nullable)
- **Semantik:** Bukan sekadar generic note store, melainkan memori terstruktur semantik. Hasil klasifikasi `NEVER_STORE` menolak penyimpanan informasi ke dalam general Memory (misal: kredensial, rahasia sistem, data sesi privat). Mendukung evolusi fakta (`SUPERSEDED`), kedaluwarsa (`EXPIRED`), dan penghapusan privasi (`FORGOTTEN`).

---

### 2.4 Conversation & Messaging Domain

#### `conversations`
- **Tujuan:** Kontainer sesi percakapan interaktif antara pengguna dan NEXUS.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `project_id`: UUID (Foreign Key -> projects.id, nullable)
  - `title`: string (nullable)
  - `type`: string (GENERAL | PROJECT | RESEARCH | DEVICE | PRIVATE)
  - `status`: string (ACTIVE | ARCHIVED | DELETED)
  - `private_session`: boolean (sesi privat tanpa persistensi memori jangka panjang)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
  - `last_message_at`: UTC timestamp (nullable)
  - `archived_at`: UTC timestamp (nullable)
- **Semantik:** Mengelompokkan rangkaian pesan dialog dengan tipe spesifik dan batas privasi eksplisit.

#### `messages`
- **Tujuan:** Butir pesan individual dalam sebuah percakapan.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `conversation_id`: UUID (Foreign Key -> conversations.id)
  - `role`: string (USER | ASSISTANT | SYSTEM_EVENT | TOOL)
  - `sender_user_id`: UUID (Foreign Key -> users.id, nullable; hanya diisi bila role adalah USER)
  - `content_type`: string (TEXT | VOICE_TRANSCRIPT | IMAGE_REFERENCE | DOCUMENT_REFERENCE | ACTION_RESULT)
  - `content`: string
  - `raw_payload`: JSON (nullable, data tambahan atau metadata alat)
  - `token_count`: integer (nullable)
  - `created_at`: UTC timestamp
- **Semantik:** Alur kepemilikan data adalah `message -> conversation -> user`. Role ASSISTANT, SYSTEM_EVENT, dan TOOL tidak mewajibkan `user_id` sebagai sender identity.

#### `conversation_summaries`
- **Tujuan:** Ringkasan berkala riwayat percakapan panjang untuk menjaga jendela token tetap efisien.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `conversation_id`: UUID (Foreign Key -> conversations.id)
  - `summary`: string
  - `from_message_id`: UUID (Foreign Key -> messages.id)
  - `to_message_id`: UUID (Foreign Key -> messages.id)
  - `created_at`: UTC timestamp
- **Semantik:** Kompresi rolling-window historis yang mempertahankan batas pesan awal dan akhir (`from_message_id` dan `to_message_id`) untuk provenance yang dapat diaudit.

---

### 2.5 Knowledge Domain

#### `knowledge_items`
- **Tujuan:** Dokumen referensi eksternal berdensitas tinggi (spesifikasi, PDF, catatan arsitektur, dokumentasi kode).
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `project_id`: UUID (Foreign Key -> projects.id, nullable)
  - `type`: string (MARKDOWN | PDF | TEXT | CODE_METADATA)
  - `title`: string
  - `mime_type`: string (nullable)
  - `object_key`: string (nullable, S3-compatible key)
  - `size_bytes`: integer (nullable)
  - `content_hash`: string (nullable, SHA-256 untuk deduplikasi konten)
  - `processing_status`: string (PENDING | PROCESSING | READY | FAILED | DELETED)
  - `processing_error`: string (nullable)
  - `metadata`: JSON (nullable, fleksibel untuk sumber dan metadata pelengkap)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
  - `deleted_at`: UTC timestamp (nullable)
- **Semantik:** Mendukung deduplikasi hash, penyimpanan object storage, soft-deletion, dan pelacakan status pemrosesan. Siklus hidup status resmi sumber daya adalah `PENDING -> PROCESSING -> READY` (atau `FAILED`, `DELETED`).

#### `knowledge_chunks`
- **Tujuan:** Potongan teks semantik hasil partisi dari `knowledge_items` untuk RAG retrieval.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `knowledge_item_id`: UUID (Foreign Key -> knowledge_items.id)
  - `chunk_index`: integer
  - `content`: string
  - `embedding`: vector
  - `token_count`: integer (nullable)
  - `page`: integer (nullable, pelacakan nomor halaman sumber)
  - `section`: string (nullable, pelacakan bagian/heading dokumen)
  - `metadata`: JSON (nullable)
  - `created_at`: UTC timestamp
- **Semantik:** Diindeks via `pgvector` untuk pencarian kedekatan semantik saat perakitan prompt konteks dengan provenance halaman dan seksi yang jelas.

---

### 2.6 Research Domain

#### `research_items`
- **Tujuan:** Artikel ilmiah, paper arXiv, dan berita rilis teknologi eksternal yang di-ingest ke Research Radar.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `source_type`: string (ARXIV | RSS | ARTICLE | TECH_BLOG)
  - `source_identifier`: string (identifier unik pada sumber asal)
  - `title`: string
  - `url`: string
  - `authors`: JSON (nullable)
  - `published_at`: UTC timestamp (nullable)
  - `abstract`: string (nullable)
  - `summary`: string (nullable)
  - `content_hash`: string (SHA-256 untuk deduplikasi konten)
  - `category`: string
  - `embedding`: vector
  - `metadata`: JSON (nullable)
  - `created_at`: UTC timestamp
  - `expires_at`: UTC timestamp (nullable)
- **Semantik:** Corpus radar komprehensif; mendukung deduplikasi hash, pencarian vektor relevansi, dan pelacakan identitas asal sumber.

#### `user_research_state`
- **Tujuan:** Status keterlibatan dan preferensi kurasi pengguna terhadap item riset tertentu.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `research_item_id`: UUID (Foreign Key -> research_items.id)
  - `state`: string (UNSEEN | SEEN | SAVED | DISMISSED)
  - `relevance_score`: float (nullable)
  - `why_relevant`: string (nullable)
  - `seen_at`: UTC timestamp (nullable)
  - `saved_at`: UTC timestamp (nullable)
  - `dismissed_at`: UTC timestamp (nullable)
  - `followed_at`: UTC timestamp (nullable)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
- **Semantik:** State resmi pengguna adalah `UNSEEN`, `SEEN`, `SAVED`, atau `DISMISSED` dengan pelacakan waktu interaksi dan alasan relevansi.

---

### 2.7 Device & Execution Node Domain

#### `devices`
- **Tujuan:** Registrasi identitas fisik perangkat keras (Mac workstation atau iPhone) dalam ekosistem trust pengguna.
- **Field Konseptual:**
  - `id`: UUID (Primary Key, durable Device ID)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `device_name`: string
  - `platform`: string (MACOS | IOS)
  - `device_type`: string (misal: WORKSTATION, MOBILE)
  - `model`: string (nullable)
  - `agent_version`: string (nullable)
  - `trust_state`: string (PENDING_PAIRING | PAIRED | REVOKED)
  - `last_seen_at`: UTC timestamp (nullable)
  - `paired_at`: UTC timestamp (nullable)
  - `revoked_at`: UTC timestamp (nullable)
  - `public_key`: string
  - `metadata`: JSON
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
- **Semantik:** Menyimpan identitas perangkat permanen. Status presensi realtime jaringan dikelola di Redis. Kode pairing bersifat efemeral dalam alur pairing workflow dan bukan bagian identitas permanen perangkat.

#### `device_capabilities`
- **Tujuan:** Katalog aksi aman yang dideklarasikan secara eksplisit oleh Mac Agent saat handshake.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `device_id`: UUID (Foreign Key -> devices.id)
  - `capability`: string
  - `enabled`: boolean
  - `metadata`: JSON (nullable, deskripsi human-readable, parameter spesifik)
  - `last_verified_at`: UTC timestamp (nullable)
- **Semantik:** Eksekusi hanya diizinkan untuk capability terdaftar resmi. Dilarang keras mendaftarkan *arbitrary shell execution*.

#### `device_sessions`
- **Tujuan:** Riwayat jejak audit sesi koneksi perangkat.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `device_id`: UUID (Foreign Key -> devices.id)
  - `session_identifier`: string
  - `connected_at`: UTC timestamp
  - `last_heartbeat_at`: UTC timestamp
  - `disconnected_at`: UTC timestamp (nullable)
  - `status`: string (CONNECTED | DISCONNECTED | STALE)
  - `metadata`: JSON (nullable)
- **Semantik:** Menyimpan riwayat koneksi historis perangkat tanpa menyimpan rahasia sesi dalam bentuk teks terang.

---

### 2.8 Permission & Policy Domain

#### `permissions`
- **Tujuan:** Aturan izin otorisasi deterministik yang mengatur eksekusi kapabilitas pada berbagai cakupan.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `device_id`: UUID (Foreign Key -> devices.id, nullable)
  - `project_id`: UUID (Foreign Key -> projects.id, nullable)
  - `routine_id`: UUID (nullable)
  - `capability`: string (identitas capability)
  - `decision`: string (ALLOW | ASK | DENY)
  - `scope`: string (GLOBAL | DEVICE | PROJECT | ROUTINE)
  - `created_at`: UTC timestamp
  - `updated_at`: UTC timestamp
  - `expires_at`: UTC timestamp (nullable)
- **Semantik:** Dievaluasi secara deterministik di luar LLM sebelum perintah diteruskan ke Mac Agent.

---

### 2.9 Action & Audit Domain

#### `actions`
- **Tujuan:** Rekaman eksekusi instruksi aksi aman ke Mac Agent dengan pelacakan siklus hidup lengkap.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id)
  - `device_id`: UUID (Foreign Key -> devices.id)
  - `project_id`: UUID (Foreign Key -> projects.id, nullable)
  - `action_type`: string (capability terdaftar yang dipanggil)
  - `payload`: JSON (parameter eksekusi tervalidasi)
  - `risk_level`: string (LOW | MEDIUM | HIGH | CRITICAL)
  - `status`: string (REQUESTED | AWAITING_CONFIRMATION | QUEUED | DISPATCHED | ACCEPTED | RUNNING | SUCCEEDED | FAILED | CANCELLED | EXPIRED | REJECTED)
  - `requested_at`: UTC timestamp
  - `expires_at`: UTC timestamp (batas waktu kedaluwarsa aksi / TTL)
  - `confirmed_at`: UTC timestamp (nullable, waktu konfirmasi oleh pengguna)
  - `started_at`: UTC timestamp (nullable, waktu eksekusi mulai di agen)
  - `completed_at`: UTC timestamp (nullable, waktu eksekusi selesai)
  - `result`: JSON (nullable, hasil eksekusi aksi)
  - `error_code`: string (nullable, kode error bila gagal)
  - `request_id`: UUID (nullable, pelacakan korelasi HTTP/WSS)\n  - `correlation_id`: UUID (korelasi penelusuran terdistribusi)
  - `idempotency_key`: UUID (kunci pencegahan eksekusi berulang)
- **Semantik:** Siklus hidup 11 status deterministik. Konfirmasi oleh pengguna mentransisikan `AWAITING_CONFIRMATION` langsung ke `QUEUED`. Kedaluwarsa waktu mentransisikan ke `EXPIRED`. Penerimaan agen mentransisikan ke `ACCEPTED`.

#### `audit_logs`
- **Tujuan:** Log audit append-only yang tidak dapat dimodifikasi untuk setiap kejadian kritis sistem.
- **Field Konseptual:**
  - `id`: UUID (Primary Key)
  - `user_id`: UUID (Foreign Key -> users.id, nullable untuk event tingkat sistem)
  - `actor_type`: string (USER | AGENT | SYSTEM)
  - `actor_id`: string (nullable)
  - `event_type`: string
  - `resource_type`: string (nullable)
  - `resource_id`: string (nullable)
  - `action_id`: UUID (Foreign Key -> actions.id, nullable)
  - `device_id`: UUID (Foreign Key -> devices.id, nullable)
  - `result`: string (SUCCESS | FAILURE | DENIED)
  - `metadata_redacted`: JSON (metadata terstruktur yang telah disanitasi & diredaksi dari data sensitif)
  - `created_at`: UTC timestamp
- **Semantik:** Catatan immutable untuk forensik dan transparansi audit. Payload sensitif diredaksi sebelum disimpan.

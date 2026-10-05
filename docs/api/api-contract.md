# REST API Contract — v1 Baseline

**Status:** LOCKED CONTRACT  
**Base URL:** `/api/v1`  
**Envelope Standar Response:**
```json
{
  "success": true,
  "data": {},
  "meta": {}
}
```
**Envelope Standar Error:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable description",
    "details": null
  }
}
```

---

## 1. Auth & Identity

### `POST /auth/apple`
- **Tujuan:** Verifikasi identitas Sign in with Apple (identity token & auth code), pertukaran token sesi, dan resolusi/pembuatan akun pengguna internal.
- **Request Body:** `{ "identity_token": "string", "authorization_code": "string", "user_info": { "name": "string", "email": "string" } }`
- **Response Data:** `{ "access_token": "string", "refresh_token": "string", "token_type": "bearer", "user": { "id": "uuid", "display_name": "string" } }`

### `POST /auth/refresh`
- **Tujuan:** Rotasi refresh token dan penerbitan access token baru.
- **Request Body:** `{ "refresh_token": "string" }`
- **Response Data:** `{ "access_token": "string", "refresh_token": "string", "token_type": "bearer" }`

### `POST /auth/logout`
- **Tujuan:** Pencabutan sesi aktif saat ini dan invalidasi refresh token.
- **Request Body:** `{ "refresh_token": "string" }`
- **Response Data:** `{ "message": "Session revoked" }`

### `GET /auth/sessions`
- **Tujuan:** Mendapatkan daftar sesi login aktif milik pengguna.
- **Response Data:** `[ { "id": "uuid", "device_name": "string", "ip_address": "string", "created_at": "ISO-8601 UTC", "last_active_at": "ISO-8601 UTC" } ]`

### `DELETE /auth/sessions/{session_id}`
- **Tujuan:** Mencabut sesi login spesifik milik pengguna.
- **Response Data:** `{ "message": "Session terminated" }`

---

## 2. User & Preferences

### `GET /me`
- **Tujuan:** Mengambil profil identitas pengguna inti terotentikasi.
- **Response Data:** `{ "id": "uuid", "display_name": "string", "status": "ACTIVE", "created_at": "ISO-8601 UTC" }`

### `PATCH /me`
- **Tujuan:** Memperbarui data profil pengguna terotentikasi.
- **Request Body:** `{ "display_name": "string" }`
- **Response Data:** `{ "id": "uuid", "display_name": "string" }`

### `GET /me/preferences`
- **Tujuan:** Mengambil setelan preferensi pengguna (bahasa, detail respons, gaya interaksi, tingkat proaktivitas, notifikasi, dll).
- **Response Data:** `{ "language": "string", "response_detail": "CONCISE | DETAILED | TECHNICAL", "interaction_style": "DIRECT | EXPLORATORY", "proactivity_level": "LOW | MEDIUM | HIGH", "default_project_id": "uuid | null", "default_device_id": "uuid | null", "storage_mode": "string | null", "research_update_frequency": "string | null", "notification_preferences": {}, "voice_settings": {} }`

### `PATCH /me/preferences`
- **Tujuan:** Memperbarui setelan preferensi pengguna.
- **Request Body:** `{ "language": "string", "response_detail": "string", "interaction_style": "string", "proactivity_level": "string", "default_project_id": "uuid | null", "default_device_id": "uuid | null", "notification_preferences": {}, "voice_settings": {} }`
- **Response Data:** `{ "updated": true, "preferences": {} }`

---

## 3. Projects (Ratified in Milestone M2)

### `POST /projects`
- **Tujuan:** Membuat workspace proyek baru.
- **Request Body:**
  ```json
  {
    "name": "string",
    "description": "string | null",
    "status": "IDEA | PLANNING | ACTIVE | PAUSED | COMPLETED",
    "priority": "LOW | NORMAL | HIGH | CRITICAL | null",
    "summary": "string | null",
    "progress": 0,
    "technologies": ["string"]
  }
  ```
- **Response Data:**
  ```json
  {
    "id": "uuid",
    "name": "string",
    "slug": "string",
    "description": "string | null",
    "status": "PLANNING",
    "priority": "NORMAL",
    "is_active": false,
    "summary": "string | null",
    "progress": 0,
    "technologies": [
      {
        "id": "uuid",
        "name": "string",
        "category": "string | null",
        "version": "string | null",
        "metadata": {},
        "created_at": "ISO-8601 UTC",
        "updated_at": "ISO-8601 UTC"
      }
    ],
    "created_at": "ISO-8601 UTC",
    "updated_at": "ISO-8601 UTC",
    "archived_at": null
  }
  ```

### `GET /projects`
- **Tujuan:** Mengambil daftar proyek milik pengguna secara terpaginasi dan terfilter.
- **Query Params:**
  - `include_archived=boolean` (default: false)
  - `status=IDEA|PLANNING|ACTIVE|PAUSED|COMPLETED|ARCHIVED` (opsional)
  - `is_active=boolean` (opsional)
  - `page=integer` (default: 1, min: 1)
  - `limit=integer` (default: 20, min: 1, max: 100)
- **Response Data:** List of `ProjectResponse` objects.
- **Response Meta:** `{ "page": 1, "limit": 20, "total": 1, "total_pages": 1 }`

### `GET /projects/{project_id}`
- **Tujuan:** Mengambil informasi detail proyek tertentu beserta daftar teknologi terkait.
- **Response Data:** `ProjectResponse` object.

### `PATCH /projects/{project_id}`
- **Tujuan:** Memperbarui metadata proyek (nama, deskripsi, status, prioritas, ringkasan, progress, teknologi).
- **Request Body:** Partial `ProjectUpdate` fields.
- **Response Data:** Updated `ProjectResponse` object.

### `POST /projects/{project_id}/activate`
- **Tujuan:** Menetapkan proyek sebagai fokus aktif tunggal pengguna (menonaktifkan fokus aktif sebelumnya secara atomik). Idempoten.
- **Response Data:** `{ "id": "uuid", "name": "string", "slug": "string", "is_active": true }`

### `POST /projects/{project_id}/archive`
- **Tujuan:** Mengarsipkan proyek (status ARCHIVED), menonaktifkan fokus aktif jika sedang aktif, dan mencatat waktu arsip tanpa menghapus rekaman permanen.
- **Response Data:** `{ "id": "uuid", "status": "ARCHIVED", "is_active": false, "archived_at": "ISO-8601 UTC" }`

### `GET /projects/{project_id}/context`
- **Tujuan:** Mengambil ringkasan fondasi metadata konteks proyek terstruktur untuk orientasi interaksi (M2 deterministic baseline, memory_count=0 dan knowledge_count=0).
- **Response Data:**
  ```json
  {
    "project_id": "uuid",
    "name": "string",
    "slug": "string",
    "summary": "string | null",
    "status": "string",
    "priority": "string | null",
    "progress": 0,
    "is_active": true,
    "active_technologies": ["string"],
    "memory_count": 0,
    "knowledge_count": 0
  }
  ```

---

## 4. Conversations & Messaging

### `POST /conversations`
- **Tujuan:** Membuat sesi percakapan baru dengan tipe tertentu dan opsi privasi.
- **Request Body:** `{ "title": "string | null", "project_id": "uuid | null", "type": "GENERAL | PROJECT | RESEARCH | DEVICE | PRIVATE", "private_session": boolean }`
- **Response Data:** `{ "id": "uuid", "title": "string | null", "type": "string", "project_id": "uuid | null", "private_session": boolean, "created_at": "ISO-8601 UTC" }`

### `GET /conversations`
- **Tujuan:** Mengambil daftar riwayat sesi percakapan milik pengguna.
- **Query Params:** `project_id=uuid`, `type=string`, `limit=integer`, `offset=integer`
- **Response Data:** `[ { "id": "uuid", "title": "string | null", "type": "string", "project_id": "uuid | null", "private_session": boolean, "updated_at": "ISO-8601 UTC" } ]`

### `GET /conversations/{conversation_id}`
- **Tujuan:** Mengambil metadata sesi percakapan spesifik.
- **Response Data:** `{ "id": "uuid", "title": "string | null", "type": "string", "project_id": "uuid | null", "private_session": boolean, "created_at": "ISO-8601 UTC", "updated_at": "ISO-8601 UTC" }`

### `DELETE /conversations/{conversation_id}`
- **Tujuan:** Menghapus sesi percakapan secara permanen atau soft-delete.
- **Response Data:** `{ "message": "Conversation deleted" }`

### `GET /conversations/{conversation_id}/messages`
- **Tujuan:** Mengambil riwayat pesan dalam sesi percakapan tertentu secara kronologis.
- **Query Params:** `limit=integer`, `before=ISO-8601 UTC`
- **Response Data:** `[ { "id": "uuid", "role": "USER | ASSISTANT | SYSTEM_EVENT | TOOL", "content_type": "TEXT | VOICE_TRANSCRIPT | IMAGE_REFERENCE | DOCUMENT_REFERENCE | ACTION_RESULT", "content": "string", "created_at": "ISO-8601 UTC" } ]`

---

## 5. NEXUS Messages

### `POST /nexus/messages`
- **Tujuan:** Mengirimkan pesan interaksi (teks atau transkrip suara) ke NEXUS AI Orchestrator dengan semantik lengkap termasuk kontrol private session. Respons streaming dapat dilanjutkan via WSS.
- **Request Body:**
  ```json
  {
    "conversation_id": "uuid",
    "content": "string",
    "input_type": "TEXT | VOICE_TRANSCRIPT",
    "project_id": "uuid | null",
    "private_session": false,
    "client_context": {},
    "client_message_id": "uuid"
  }
  ```
- **Response Data:** `{ "message_id": "uuid", "role": "ASSISTANT", "content": "string", "streaming": boolean }`

### `GET /messages/{message_id}/context`
- **Tujuan:** Transparansi konteks (Context Inspector) — menampilkan memori, dokumen knowledge, dan telemetri perangkat yang digunakan model untuk menyusun jawaban.
- **Response Data:** `{ "message_id": "uuid", "memories_used": [], "knowledge_used": [], "device_telemetry_used": [] }`

---

## 6. Memory & Control Center

### `POST /memories`
- **Tujuan:** Menambahkan entri memori personal/proyek terstruktur secara manual atau via reasoning engine.
- **Request Body:**
  ```json
  {
    "memory_type": "PERSONAL_FACT | PREFERENCE | INTEREST | SKILL | GOAL | PROJECT_FACT | PROJECT_DECISION | PROJECT_PROGRESS | PROJECT_NEXT_ACTION | BEHAVIOR_PATTERN",
    "subject": "string",
    "predicate": "string",
    "value_text": "string",
    "value_json": null,
    "project_id": "uuid | null"
  }
  ```
- **Response Data:** `{ "id": "uuid", "subject": "string", "predicate": "string", "value_text": "string", "status": "ACTIVE" }`

### `GET /memories`
- **Tujuan:** Mengambil daftar memori aktif pengguna dengan filter status, kategori, atau proyek.
- **Query Params:** `status=ACTIVE | SUPERSEDED | EXPIRED | FORGOTTEN | PENDING_CONFIRMATION`, `project_id=uuid`, `memory_type=string`
- **Response Data:** `[ { "id": "uuid", "subject": "string", "predicate": "string", "value_text": "string", "memory_type": "string", "status": "string", "created_at": "ISO-8601 UTC" } ]`

### `GET /memories/{memory_id}`
- **Tujuan:** Mengambil detail lengkap entri memori terstruktur tertentu.
- **Response Data:** `{ "id": "uuid", "memory_type": "string", "subject": "string", "predicate": "string", "value_text": "string", "summary": "string", "importance": 0.8, "confidence": 0.9, "status": "string", "project_id": "uuid | null", "created_at": "ISO-8601 UTC", "superseded_by": "uuid | null" }`

### `PATCH /memories/{memory_id}`
- **Tujuan:** Memperbarui konten, nilai, atau kategori memori.
- **Request Body:** `{ "value_text": "string", "value_json": null }`
- **Response Data:** `{ "id": "uuid", "value_text": "string", "status": "string" }`

### `POST /memories/search`
- **Tujuan:** Pencarian semantik memori berbasis embedding kemiripan vektor.
- **Request Body:** `{ "query": "string", "project_id": "uuid | null", "limit": integer }`
- **Response Data:** `[ { "id": "uuid", "subject": "string", "predicate": "string", "value_text": "string", "similarity_score": float } ]`

### `POST /memories/{memory_id}/forget`
- **Tujuan:** Mengubah status memori menjadi `FORGOTTEN` agar tidak lagi digunakan dalam penyusunan konteks.
- **Response Data:** `{ "id": "uuid", "status": "FORGOTTEN", "forgotten_at": "ISO-8601 UTC" }`

---

## 7. Knowledge Vault

### `POST /knowledge`
- **Tujuan:** Mengunggah dan mendaftarkan dokumen baru ke Knowledge Vault (markdown, PDF, teks, repo metadata).
- **Request Body:** Multipart form atau `{ "title": "string", "source_type": "string", "content": "string", "project_id": "uuid | null" }`
- **Response Data:** `{ "id": "uuid", "title": "string", "status": "PENDING" }`

### `GET /knowledge`
- **Tujuan:** Mengambil daftar item dokumen dalam Knowledge Vault.
- **Query Params:** `project_id=uuid`, `status=string`, `limit=integer`, `offset=integer`
- **Response Data:** `[ { "id": "uuid", "title": "string", "source_type": "string", "status": "PENDING | PROCESSING | READY | FAILED | DELETED", "created_at": "ISO-8601 UTC" } ]`

### `GET /knowledge/{knowledge_id}`
- **Tujuan:** Mengambil metadata dan status dokumen knowledge.
- **Response Data:** `{ "id": "uuid", "title": "string", "source_type": "string", "status": "PENDING | PROCESSING | READY | FAILED | DELETED", "chunk_count": integer, "created_at": "ISO-8601 UTC" }`

### `DELETE /knowledge/{knowledge_id}`
- **Tujuan:** Menghapus dokumen knowledge beserta potongan chunk embedding terkait.
- **Response Data:** `{ "message": "Knowledge item deleted" }`

### `GET /knowledge/{knowledge_id}/status`
- **Tujuan:** Memeriksa status sumber daya dokumen dan status job pemrosesan di latar belakang.
- **Response Data:** `{ "id": "uuid", "status": "PENDING | PROCESSING | READY | FAILED | DELETED", "job": { "status": "QUEUED | RUNNING | SUCCEEDED | FAILED", "progress": float, "error": "string | null" } }`

### `POST /knowledge/search`
- **Tujuan:** Pencarian dokumen berbasis kemiripan semantik potongan vektor (RAG context).
- **Request Body:** `{ "query": "string", "project_id": "uuid | null", "limit": integer }`
- **Response Data:** `[ { "knowledge_id": "uuid", "chunk_id": "uuid", "content": "string", "similarity_score": float } ]`

### `POST /knowledge/ask`
- **Tujuan:** Mengajukan pertanyaan spesifik terhadap corpus Knowledge Vault (Q&A terisolasi).
- **Request Body:** `{ "query": "string", "knowledge_ids": ["uuid"], "project_id": "uuid | null" }`
- **Response Data:** `{ "answer": "string", "citations": [ { "knowledge_id": "uuid", "chunk_id": "uuid", "snippet": "string" } ] }`

---

## 8. Research Radar

### `GET /research/feed`
- **Tujuan:** Mengambil feed riset teknologi dan paper yang terkurasi berdasarkan minat pengguna.
- **Query Params:** `limit=integer`, `filter=string`
- **Response Data:** `[ { "id": "uuid", "title": "string", "summary": "string", "source_url": "string", "published_at": "ISO-8601 UTC", "state": "UNSEEN | SEEN | SAVED | DISMISSED" } ]`

### `POST /research/{research_id}/save`
- **Tujuan:** Menyimpan item riset ke daftar bookmark / koleksi pribadi.
- **Response Data:** `{ "id": "uuid", "state": "SAVED" }`

### `POST /research/{research_id}/dismiss`
- **Tujuan:** Mengabaikan item riset agar tidak muncul lagi di feed utama.
- **Response Data:** `{ "id": "uuid", "state": "DISMISSED" }`

### `POST /research/{research_id}/seen`
- **Tujuan:** Menandai item riset telah dilihat oleh pengguna.
- **Response Data:** `{ "id": "uuid", "state": "SEEN" }`

### `POST /research/{research_id}/follow`
- **Tujuan:** Mengikuti topik atau entitas riset terkait untuk kurasi mendatang.
- **Response Data:** `{ "id": "uuid", "followed": true }`

### `POST /research/{research_id}/explain`
- **Tujuan:** Meminta penjelasan sintetis dari AI mengenai relevansi paper/artikel terhadap proyek aktif pengguna.
- **Response Data:** `{ "id": "uuid", "explanation": "string", "project_relevance": "string" }`

### `GET /research/interests`
- **Tujuan:** Mengambil daftar topik minat riset pengguna.
- **Response Data:** `[ { "id": "uuid", "topic": "string", "weight": float } ]`

### `PATCH /research/interests`
- **Tujuan:** Memperbarui daftar minat dan kata kunci riset pengguna.
- **Request Body:** `{ "interests": [ { "topic": "string", "weight": float } ] }`
- **Response Data:** `{ "updated": true, "interests": [] }`

---

## 9. Devices & Mac Agent

### `GET /devices`
- **Tujuan:** Mengambil daftar seluruh perangkat terdaftar milik pengguna beserta status trust dan presence-nya.
- **Response Data:** `[ { "id": "uuid", "name": "string", "platform": "macos | ios", "trust_state": "PAIRED | PENDING_PAIRING | REVOKED", "presence_state": "ONLINE | OFFLINE | STALE", "last_seen_at": "ISO-8601 UTC" } ]`

### `GET /devices/{device_id}`
- **Tujuan:** Mengambil informasi detail perangkat tertentu.
- **Response Data:** `{ "id": "uuid", "name": "string", "platform": "string", "device_type": "string", "trust_state": "string", "presence_state": "string", "capabilities": [], "created_at": "ISO-8601 UTC" }`

### `GET /devices/{device_id}/status`
- **Tujuan:** Mengambil status realtime dan telemetri kehadiran perangkat.
- **Response Data:** `{ "device_id": "uuid", "presence_state": "ONLINE | OFFLINE | STALE", "last_heartbeat_at": "ISO-8601 UTC" }`

### `POST /devices/pairing`
- **Tujuan:** Inisiasi permintaan kode pairing jangka pendek sekali pakai (*short-lived one-time code*, durasi TTL terkonfigurasi, lihat TBD-021).
- **Request Body:** `{ "device_name": "string", "platform": "macos" }`
- **Response Data:** `{ "pairing_code": "string", "expires_at": "ISO-8601 UTC" }`

### `POST /devices/pairing/claim`
- **Tujuan:** Mac Agent mengklaim kode pairing ke server bersamaan dengan public key lokal yang baru dibuat.
- **Request Body:** `{ "pairing_code": "string", "device_name": "string", "public_key": "string", "capabilities": ["string"] }`
- **Response Data:** `{ "device_id": "uuid", "trust_state": "PAIRED" }`

### `POST /devices/{device_id}/revoke`
- **Tujuan:** Mencabut izin perangkat secara definitif (`REVOKED`). Koneksi WSS akan langsung diputus.
- **Response Data:** `{ "device_id": "uuid", "trust_state": "REVOKED" }`

### `GET /devices/{device_id}/permissions` *(Convenience)*
- **Tujuan:** Mengambil daftar konfigurasi izin khusus untuk perangkat yang ditentukan.
- **Response Data:** `[ { "permission_id": "uuid", "capability_id": "string", "decision": "ALLOW | ASK | DENY", "scope": "DEVICE" } ]`

---

## 10. Actions & Remote Execution

### `POST /actions`
- **Tujuan:** Mengajukan permintaan eksekusi aksi terstruktur ke Mac Agent via backend Permission Engine.
- **Request Body:** `{ "device_id": "uuid", "capability_id": "string", "parameters": {}, "project_id": "uuid | null", "idempotency_key": "uuid" }`
- **Response Data:** `{ "action_id": "uuid", "status": "REQUESTED | AWAITING_CONFIRMATION | QUEUED", "expires_at": "ISO-8601 UTC" }`

### `GET /actions/{action_id}`
- **Tujuan:** Memantau status siklus hidup aksi (11 status kanonikal: REQUESTED, AWAITING_CONFIRMATION, QUEUED, DISPATCHED, ACCEPTED, RUNNING, SUCCEEDED, FAILED, CANCELLED, EXPIRED, REJECTED).
- **Response Data:** `{ "action_id": "uuid", "status": "string", "result": null, "error": null, "updated_at": "ISO-8601 UTC" }`

### `POST /actions/{action_id}/confirm`
- **Tujuan:** Pengguna memberikan konfirmasi eksplisit dari iOS untuk mengeksekusi aksi berstatus `AWAITING_CONFIRMATION` (evaluasi ASK). Transisi status langsung menjadi `QUEUED`.
- **Response Data:** `{ "action_id": "uuid", "status": "QUEUED" }`

### `POST /actions/{action_id}/cancel`
- **Tujuan:** Membatalkan aksi sebelum atau selama eksekusi.
- **Response Data:** `{ "action_id": "uuid", "status": "CANCELLED" }`

---

## 11. Permissions

### `GET /permissions`
- **Tujuan:** Mengambil daftar aturan izin pengguna di semua scope (GLOBAL, DEVICE, PROJECT, ROUTINE).
- **Response Data:** `[ { "id": "uuid", "capability": "string", "decision": "ALLOW | ASK | DENY", "scope": "string", "device_id": "uuid | null", "project_id": "uuid | null" } ]`

### `GET /permissions/{permission_id}`
- **Tujuan:** Mengambil rincian aturan izin spesifik.
- **Response Data:** `{ "id": "uuid", "capability": "string", "decision": "ALLOW | ASK | DENY", "scope": "string", "device_id": "uuid | null", "project_id": "uuid | null" }`

### `PATCH /permissions/{permission_id}`
- **Tujuan:** Memperbarui keputusan izin (misal: mengubah ASK menjadi ALLOW untuk scope tertentu).
- **Request Body:** `{ "decision": "ALLOW | ASK | DENY" }`
- **Response Data:** `{ "id": "uuid", "decision": "string", "updated_at": "ISO-8601 UTC" }`

---

## 12. Activity & Audit

### `GET /activity`
- **Tujuan:** Mengambil log audit linimasa aktivitas sistem (aksi yang dijalankan, perubahan izin, pairing, dsb) secara append-only dengan metadata diredaksi.
- **Query Params:** `limit=integer`, `offset=integer`, `category=string`, `project_id=uuid`
- **Response Data:** `[ { "id": "uuid", "event_type": "string", "actor_type": "USER | AGENT | SYSTEM", "result": "SUCCESS | FAILURE | DENIED", "metadata_redacted": {}, "created_at": "ISO-8601 UTC" } ]`

---

## 13. Storage

### `GET /storage`
- **Tujuan:** Mengambil informasi status kapasitas penyimpanan dokumen dan kuota (Knowledge Vault & Binary Assets).
- **Response Data:** `{ "total_bytes_used": integer, "file_count": integer, "storage_provider": "S3-compatible" }`

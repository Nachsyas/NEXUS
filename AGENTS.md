# AGENTS.md — NEXUS Operating Guidelines for AI Agents

**Status:** CANONICAL — NON-NEGOTIABLE  
**Target:** Seluruh AI coding agent (Antigravity dan subagent lainnya)  
**Source of Truth:** Prompt Master v1.1

---

## 1. Identitas & Prinsip NEXUS
> **"NEXUS bukan aplikasi yang memiliki AI. NEXUS adalah AI companion, sedangkan aplikasi hanyalah salah satu cara untuk berinteraksi dengannya."**

NEXUS adalah Personal AI Companion & Intelligence Ecosystem.
Positioning: *A Personal AI Companion that remembers, understands, connects, and acts.*

Authority Hierarchy:
```text
NEXUS PRODUCT VISION
  ↓
APPROVED PRODUCT SPECIFICATION
  ↓
APPROVED ARCHITECTURE
  ↓
ACCEPTED ADR
  ↓
ENGINEERING CONSTITUTION
  ↓
PHASE / MILESTONE SPECIFICATION
  ↓
AGENTS.md / SOP / SKILLS
  ↓
IMPLEMENTATION
```
Jika terjadi konflik: **NEXUS SPECIFICATION > TEMPLATE > AGENT PREFERENCE**. Dilarang mengubah NEXUS agar sesuai dengan preferensi bawaan agent.

---

## 2. Locked Stack Phase 1
- **iOS Client:** Swift, SwiftUI, SwiftData (hanya untuk cache/offline metadata, bukan source of truth long-term memory), URLSession, WebSocket, AVFoundation, App Intents, Keychain.
- **macOS Agent:** Swift native, SwiftUI/Menu bar, URLSessionWebSocketTask, macOS Keychain, Capability-based execution node (BUKAN remote shell).
- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy, Alembic (Modular Monolith).
- **Database:** PostgreSQL + pgvector (Primary source of truth).
- **Cache/Presence:** Redis (Ephemeral state only).
- **Storage:** S3-compatible storage (dokumen & binary assets).
- **Realtime:** WebSocket (WSS).

---

## 3. Engineering Constitution (Aturan Non-Negotiable)
Dilarang keras:
1. Spaghetti code, god classes/services, circular dependencies.
2. Cross-domain repository shortcuts (domain A membaca repository domain B secara langsung).
3. Business logic di router atau di repository.
4. Hidden global mutable state.
5. Unrestricted remote shell pada Mac Agent.
6. Memperlakukan LLM sebagai authorization authority (LLM hanya mengusulkan structured tool, Permission Engine deterministik di luar LLM yang memutuskan).
7. Menyimpan secret/credential ke dalam general Memory.
8. Unbounded queries, unbounded context window, unbounded cache, infinite retry.
9. Silent architectural changes atau silent technical debt.
10. Falsifikasi hasil test, benchmark, atau dokumentasi.

---

## 4. Keamanan & Invarian Kritis
- **AI Tidak Boleh Bypass Policy:** Seluruh aksi perangkat melalui Permission Engine deterministik.
- **Mac Agent Least Privilege:** Hanya mengeksekusi capability yang terdaftar resmi.
- **Device Trust vs Presence:** Offline ≠ Revoked; Online ≠ Otomatis Dipercaya.
- **Data Minimization & Multi-Tenancy:** Setiap query database wajib scoped ke `user_id`. Tidak ada IDOR.
- **Private Session:** Saat aktif, dilarang melakukan persistensi memori jangka panjang atau behavioral learning.

---

## 5. Standing Autonomous Execution Policy & Failure Recovery

### 5.1 Otorisasi Pelaksanaan Mandiri (Standing Authorization)
Begitu pengguna secara eksplisit memulai atau menyetujui sebuah task, milestone, atau instruksi kerja (seperti kickoff M0):
- Instruksi tersebut memberikan **otorisasi penuh (standing authorization)** untuk seluruh pekerjaan rekayasa normal di dalam lingkup tugas yang telah disetujui.
- **Perilaku Default:** 
  ```text
  DO THE WORK.
  VALIDATE IT.
  FIX PROBLEMS.
  CONTINUE.
  DOCUMENT IT.
  COMPLETE THE ASSIGNMENT.
  ```
- **Dilarang keras meminta konfirmasi mikro (*micro-confirmations*)** seperti:
  - *"Bolehkah saya melanjutkan?"*
  - *"Bolehkah saya mengedit file ini?"*
  - *"Bolehkah saya membuat folder ini?"*
  - *"Bolehkah saya menjalankan command ini?"*
  - *"Bolehkah saya menjalankan test?"*
  - *"Bolehkah saya memperbaiki error ini?"*
  - *"Bolehkah saya memperbarui dokumentasi?"*
  jika tindakan tersebut memang merupakan bagian dari cakupan tugas atau milestone yang telah disetujui.

### 5.2 Tindakan Otonom yang Diizinkan di Dalam Lingkup
Dalam lingkup tugas yang disetujui, agen diizinkan secara mandiri untuk:
1. Memeriksa (*inspect*) repositori dan berkas.
2. Membuat, mengedit, dan memindahkan berkas proyek yang disetujui.
3. Menjalankan proses build.
4. Menjalankan pengujian otomatis (*unit, integration, contract tests*).
5. Menjalankan formatter, linter, dan static analysis.
6. Menjalankan perintah pengembangan lokal (*database migration, local services*).
7. Memeriksa status dan diff Git.
8. Memperbaiki error atau regresi yang muncul selama pelaksanaan tugas.
9. Menjalankan ulang validasi yang sempat gagal hingga berhasil.
10. Memperbarui dokumen tata kelola, stage evidence, dan context files (`PROJECT-STATE.md`, `CURRENT-STAGE.md`, `NEXT-ACTIONS.md`, `KNOWN-ISSUES.md`, `HANDOFF.md`).

### 5.3 Protokol Pemulihan Kegagalan Mandiri (Autonomous Failure Recovery)
Jika terjadi kegagalan pada suatu sub-tahap (misal: test error, lint failure, validasi gagal):
```text
REPRODUCE → INVESTIGATE → FIX → RE-RUN → VERIFY → CONTINUE
```
Agen dilarang berhenti atau meminta bantuan pengguna hanya karena sebuah sub-langkah teknis mengalami kegagalan. Investigasi akar masalah, perbaiki, uji kembali, dan lanjutkan hingga selesai.

### 5.4 Batasan Keputusan Pengguna (User Decision Boundary)
Otorisasi mandiri **TIDAK MENGIZINKAN** agen membuat keputusan baru yang menjadi hak prerogatif pengguna (*user-owned decisions*). Agen wajib BERHENTI dan meminta keputusan pengguna hanya pada batas berikut:
1. Adanya item TBD yang belum terselesaikan namun mutlak dibutuhkan oleh pekerjaan saat ini.
2. Perubahan terhadap arsitektur yang telah berstatus `LOCKED`.
3. Perluasan ruang lingkup (*scope expansion*) di luar milestone aktif.
4. Penambahan kapabilitas baru yang berpotensi destruktif.
5. Penggantian teknologi inti stack baseline.
6. Keputusan lisensi pihak ketiga.
7. Tindakan destruktif permanen di luar lingkup kerja yang disetujui.
8. Rilis produksi yang memerlukan persetujuan formal.
9. Ambiguitas keamanan yang tidak dapat diselesaikan secara aman melalui prinsip least-privilege / fail-closed.

*Kaidah Non-Blocking:* Jika salah satu keputusan terblokir, agen tetap melanjutkan seluruh tugas lain yang tidak terblokir dalam milestone aktif. Dilarang menghentikan seluruh milestone tanpa alasan valid.

### 5.5 Batasan Keamanan Platform (Platform Security Controls)
Kebijakan ini mengatur alur kerja agen. Kebijakan ini **TIDAK MEMBERIKAN OTORISASI** untuk membypass:
- Dialog izin sistem operasi (macOS permission dialogs / TCC).
- Otentikasi dan kredensial sistem.
- Persyaratan penandatanganan kode Xcode (*code signing*).
- Kontrol keamanan GitHub atau cloud provider.
- Dialog keamanan dan sandbox wajib milik platform Antigravity.
Dilarang melemahkan keamanan sistem demi mendapatkan otonomi kerja.

---

## 6. Protokol Kerja Sesi
### Start-of-Session:
1. Baca `AGENTS.md`.
2. Baca `docs/README.md`.
3. Baca `docs/context/PROJECT-STATE.md`, `CURRENT-STAGE.md`, dan `HANDOFF.md`.
4. Periksa canonical documentation dan accepted ADR yang relevan.
5. Periksa actual repository state (jangan percaya dokumen jika kode bertentangan).
6. Identifikasi task persis sebelum memulai.

### End-of-Session:
1. Jalankan testing dan pemeriksaan relevan.
2. Catat bukti nyata (evidence) di stage docs (implementation log, files changed, test results).
3. Update `PROJECT-STATE.md`, `CURRENT-STAGE.md`, `NEXT-ACTIONS.md`, dan `HANDOFF.md`.
4. Laporkan status secara faktual.

---

## 7. Daftar Skills Resmi
Agent wajib mengacu pada SOP dan skill terdaftar di `.agents/skills/<skill-name>/SKILL.md`:
`read-context`, `create-feature`, `create-api`, `database-change`, `memory-feature`, `context-engine`, `ai-tool`, `mac-agent-action`, `device-capability`, `realtime-feature`, `knowledge-pipeline`, `research-pipeline`, `security-review`, `performance-review`, `architecture-review`, `write-tests`, `debug-issue`, `adr`, `stage-close`, `release-check`.

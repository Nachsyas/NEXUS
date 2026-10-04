# CONTINUATION HANDOFF — READ FIRST

**Target:** Pengembang atau AI Agent Baru  
**Current State:** Milestone M1 (Account & Identity Foundation) CLOSED — COMPLETE, RATIFIED & VERIFIED. Ready for Milestone M2 (Projects) authorization.  
**Canonical Remote:** `https://github.com/Nachsyas/NEXUS.git` (main, PUBLIC)  
**Local Repository (Current Machine):** `/Users/user/Documents/Nexus`  

---

## 1. What Was Just Completed
Milestone M1 (Account & Identity Foundation) telah selesai dilaksanakan secara penuh, diverifikasi, diratifikasi, diuji, dan didokumentasikan:
- **Canonical Domain Models & Separation:** `User` (UUIDv7) dipisahkan secara ketat dari `AuthIdentity` (`provider = 'APPLE'`). Invarian utama: `User` != `Authentication Provider`.\n- **Database Schema & Migrations:** Tabel `users`, `auth_identities`, `user_preferences`, `sessions`, `rotated_token_hashes` dibuat dan diterapkan via Alembic migration `0002_identity_and_sessions.py` (verifikasi rollback dan forward 100% sukses).
- **Apple Identity Verification Boundary:** `AppleIdentityVerifier` abstrak dengan `ProductionAppleVerifier` (validasi JWKS RS256) dan `MockAppleVerifier` (pengujian offline tanpa koneksi Apple live). Status faktual: `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`.
- **Token Security Architecture (ADR-020 ACCEPTED):** Short-lived HS256 JWT access token (15 menit configurable TTL di `Settings`), opaque 256-bit refresh token (30 hari configurable TTL di `Settings`). Plaintext refresh token **tidak pernah disimpan di database**; hanya SHA-256 hash yang disimpan.
- **Security Invariants & Algorithm Safety:** Dekoding token dibatasi ketat ke `algorithms=["HS256"]`; token dengan algoritma `none` atau signature salah ditolak dengan 401 `AUTH_INVALID_CREDENTIALS`. Token expired ditolak dengan `AUTH_TOKEN_EXPIRED`. Validator Settings menolak secret placeholder pada production.
- **Refresh Token Rotation & Reuse Detection:** Rotasi token atomik dengan riwayat token yang dirotasi (`rotated_token_hashes`). Penggunaan ulang token yang telah dirotasi langsung membatalkan seluruh keluarga sesi (`token_family_id`) dan tersimpan permanen ke DB dengan status `REUSE_DETECTED`. Sesi yang telah di-revoke tidak dapat melakukan refresh.
- **User Preferences:** Inisialisasi preferensi default saat pertama kali login Apple, dapat dimodifikasi melalui `/api/v1/me/preferences`.
- **Multi-Tenant Isolation & IDOR Protection:** Seluruh endpoint memvalidasi kepemilikan data (`user_id == current_user.user_id`). Verifikasi tes mencakup 6 dimensi isolasi (baca/ubah profil, baca/ubah preferensi, daftar/hentikan sesi). Akses lintas-pengguna ditolak dengan `403 FORBIDDEN_ACCESS`.
- **iOS Client (`apps/ios/NEXUS/`):**
  - `NexusKeychainService`: Penyimpanan kredensial aman hardware-backed via Security framework (`kSecClassGenericPassword`, `kSecAttrAccessibleAfterFirstUnlock`).
  - `NexusAPIClient`: URLSession client dengan deserialisasi model nonisolated untuk Swift 6 Concurrency.
  - `AuthManager`: Observable auth state machine (`.unauthenticated`, `.authenticating`, `.authenticated`, `.error`).
  - `AuthView`: Tampilan SwiftUI Sign in with Apple, indikator loading, kartu profil pengguna terautentikasi, dan tombol logout.
- **Verifikasi Kualitas & Tes:**
  - Pytest: 23/23 lulus dalam 1.06s.
  - Ruff linter: 0 error.
  - Ruff format: 100% konsisten.
  - Mypy strict mode: 0 error pada 30 berkas sumber.
  - iOS Build: `** BUILD SUCCEEDED **` (Universal Simulator arm64/x86_64).
  - macOS Agent Build: `Build complete! (0.29s)`.
- **Dokumentasi Milestone M1:** Seluruh 12 berkas dokumentasi tahap M1 lengkap tersedia di lokasi kanonikal `docs/stages/phase-1/M1-account-identity/`.

## 2. Standing Autonomous Policy & Stop Boundary
- Milestone M1 telah selesai, diverifikasi, diratifikasi, dan ditutup secara resmi (**CLOSED — COMPLETE**).
- **BATAS PEMBERHENTIAN (*STOP BOUNDARY*):** Berhenti di batas akhir Milestone M1. Dilarang memulai Milestone M2 tanpa instruksi eksplisit pengguna.

## 3. DO NOT CHANGE
- Dilarang membuang pemisahan canonical `User` != `AuthIdentity`.
- Dilarang menyimpan token refresh plaintext di basis data.
- Dilarang menyimpan kredensial autentikasi di `UserDefaults`, `plist`, atau file plain pada iOS.
- Dilarang mengabaikan token family revocation pada reuse detection.
- Dilarang memulai Milestone M2 tanpa perintah eksplisit pengguna.
- Roadmap urutan milestone kanonikal: M0 Foundation -> M1 Account & Identity -> M2 Projects -> M3 Memory Core. Dilarang menganggap M2 sebagai Personal Profile & Memory Core.

## 4. Next Exact Task
Menunggu instruksi pengguna: `START M2 PROJECTS` (atau perintah sejenis untuk membuka M2). Dilarang memulai M2 secara mandiri.

## 5. Required Reading Before Starting M2
1. [`AGENTS.md`](../../AGENTS.md)
2. [`docs/stages/phase-1/M1-account-identity/completion-report.md`](../stages/phase-1/M1-account-identity/completion-report.md)
3. [`docs/context/PROJECT-STATE.md`](PROJECT-STATE.md)
4. [`docs/context/CURRENT-STAGE.md`](CURRENT-STAGE.md)
5. [`docs/context/NEXT-ACTIONS.md`](NEXT-ACTIONS.md)

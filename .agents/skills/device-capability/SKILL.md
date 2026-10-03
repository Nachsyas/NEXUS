# Skill: device-capability

## 1. Description
Mengimplementasikan fungsi lokal native macOS untuk satu capability spesifik.

## 2. When Used
Saat menambah atau memperbaiki safe capability pada Mac Agent.

## 3. Prerequisites
Capability telah disetujui dalam daftar resmi Phase 1.

## 4. Required Docs
- `docs/architecture/mac-agent-architecture.md`
- `docs/security/permission-model.md`

## 5. Workflow
1. Buat class/struct handler Swift yang mengimplementasikan protocol `CapabilityHandler`.
2. Validasi parameter input secara ketat.
3. Eksekusi menggunakan Apple native APIs (misal `NSWorkspace`).
4. Tangkap error secara elegan dan kembalikan output terstruktur.
5. Daftarkan di `CapabilityRegistry`.

## 6. Validation
Jalankan unit test Swift untuk memvalidasi input valid dan invalid.

## 7. Docs Update
Dokumentasikan capability baru di `docs/api/mac-agent-protocol.md`.

## 8. Stop Conditions
Berhenti jika handler memerlukan Full Disk Access tanpa justifikasi ketat.

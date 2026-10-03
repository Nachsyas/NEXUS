# Permission Model — Deterministic Authorization

**Status:** LOCKED CANONICAL ARCHITECTURE  
**Version:** 1.1  
**Decision Reference:** ADR-015  

---

## 1. Tingkat Keputusan Izin (Permission Decisions)
Sistem izin NEXUS beroperasi secara deterministik di luar model AI dengan tiga tingkatan mutlak:
- `DENY`: Aksi dilarang mutlak dan langsung ditolak secara fail-closed tanpa meminta konfirmasi pengguna.
- `ASK`: Aksi ditahan hingga pengguna memberikan persetujuan eksplisit melalui notifikasi atau dialog konfirmasi di aplikasi iOS.
- `ALLOW`: Aksi diizinkan berjalan otomatis selama parameter payload valid, sesuai skema, dan lolos risk policy.

> **INVARIAN KEAMANAN MUTLAK:** Eksekusi shell terminal arbitrer (*Arbitrary Shell*) berstatus **DENY** secara permanen di seluruh scope dan tidak didukung oleh arsitektur NEXUS (ADR-010).

---

## 2. Cakupan Izin (Permission Scopes)
- `GLOBAL`: Berlaku untuk semua perangkat dan konteks milik pengguna.
- `DEVICE`: Dibatasi khusus untuk satu perangkat fisik tertentu (`device_id`).
- `PROJECT`: Dibatasi khusus dalam konteks proyek aktif tertentu (`project_id`).
- `ROUTINE`: Berlaku untuk alur otomatisasi terjadwal yang telah disetujui sebelumnya.

---

## 3. Matriks Kebijakan Izin Default (Proposed Policy — Status: TBD-023)
*Catatan Tata Kelola: Matriks per-capability default di bawah ini berstatus **PROPOSED / TBD-023** dan belum berstatus locked. Keputusan resmi per kapabilitas akan dikunci sebelum Milestone M8 Remote Safe Actions. Pengecualian mutlak: Arbitrary Shell tetap LOCKED DENY.*

| Capability ID | Proposed Default Decision | Scope Minimum | Konfirmasi Pengguna | Catatan Status |
|---|---|---|---|---|
| `GET_DEVICE_STATUS` | ALLOW | DEVICE | Tidak | PROPOSED (TBD-023) |
| `GET_GIT_STATUS` | ALLOW | PROJECT | Tidak | PROPOSED (TBD-023) |
| `OPEN_APPLICATION` | ASK | DEVICE | Ya, kecuali user mengaktifkan allowlist | PROPOSED (TBD-023) |
| `OPEN_PROJECT` | ALLOW | PROJECT | Tidak | PROPOSED (TBD-023) |
| `GET_SERVICE_STATUS` | ALLOW | DEVICE | Tidak | PROPOSED (TBD-023) |
| `START_APPROVED_SERVICE` | ASK | DEVICE | Ya | PROPOSED (TBD-023) |
| `STOP_APPROVED_SERVICE` | ASK | DEVICE | Ya | PROPOSED (TBD-023) |
| `GET_APPROVED_LOGS` | ASK | DEVICE | Ya (redaksi log sensitif) | PROPOSED (TBD-023) |
| *Arbitrary Shell Execution* | **DENY** | GLOBAL | **DITOLAK PERMANEN** | **LOCKED (ADR-010)** |

# Skill: adr

## 1. Description
Mengajukan proposal perubahan atau penetapan arsitektur baru.

## 2. When Used
Saat diperlukan perubahan arsitektur, penggantian database, atau penambahan protokol baru.

## 3. Prerequisites
Adanya kebutuhan teknis nyata yang didukung bukti dan perbandingan alternatif.

## 4. Required Docs
- `docs/decisions/`
- Prompt Master Section 162-164

## 5. Workflow
1. Beri nomor urut ADR baru (format: `ADR-XXX-judul.md`).
2. Tulis Context, Problem, Proposed Decision, Alternatives, dan Consequences.
3. Tetapkan status awal sebagai `PROPOSED`.
4. HENTIKAN implementasi dan tunggu review serta persetujuan pengguna.
5. Ubah status menjadi `ACCEPTED` hanya setelah pengguna menyetujui.

## 6. Validation
Proposal memuat analisis dampak keamanan dan performa yang objektif.

## 7. Docs Update
Daftarkan ADR baru di `docs/context/ACTIVE-DECISIONS.md`.

## 8. Stop Conditions
Agent dilarang keras mengubah status ADR menjadi ACCEPTED secara sepihak.

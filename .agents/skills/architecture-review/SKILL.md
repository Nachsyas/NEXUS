# Skill: architecture-review

## 1. Description
Memverifikasi kepatuhan terhadap batas domain dan Engineering Constitution.

## 2. When Used
Pada setiap penyelesaian stage atau refactoring modul.

## 3. Prerequisites
Kode telah ditulis dan siap diperiksa.

## 4. Required Docs
- `docs/architecture/domain-boundaries.md`
- `AGENTS.md`

## 5. Workflow
1. Periksa dependensi antar modul (larangan circular dependency).
2. Pastikan tidak ada repository shortcut lintas domain.
3. Periksa agar router tidak memuat business logic.
4. Isi kuesioner `architecture-review.md` pada stage terkait.

## 6. Validation
Semua pertanyaan pelanggaran arsitektur terjawab NO.

## 7. Docs Update
Update stage `architecture-review.md`.

## 8. Stop Conditions
Berhenti jika ditemukan antipattern god-service atau coupling liar.

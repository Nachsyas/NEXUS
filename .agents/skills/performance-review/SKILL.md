# Skill: performance-review

## 1. Description
Memvalidasi latensi, throughput, dan penggunaan memori terhadap anggaran performa.

## 2. When Used
Saat menutup milestone atau saat terdeteksi regresi performa.

## 3. Prerequisites
Skenario pengujian terukur telah disiapkan.

## 4. Required Docs
- `docs/architecture/performance-budget.md`
- `docs/SOP/07-performance-engineering.md`

## 5. Workflow
1. Jalankan benchmark pada endpoint atau pipeline target.
2. Catat metrik p50, p95, dan p99.
3. Bandingkan dengan angka baseline sebelumnya.
4. Identifikasi adanya N+1 query atau token overflow.
5. Catat hasil faktual pada `performance-results.md`.

## 6. Validation
Pastikan tidak ada regresi performa yang melampaui toleransi budget.

## 7. Docs Update
Update stage `performance-results.md`.

## 8. Stop Conditions
Berhenti jika angka metrik yang dicatat adalah hasil rekaan tanpa pengujian riil.

# Skill: context-engine

## 1. Description
Membangun logika agregasi konteks lintas sumber (memori, dokumen, telemetri).

## 2. When Used
Saat merakit prompt konteks untuk LLM reasoning.

## 3. Prerequisites
Komponen Memory dan Knowledge Vault telah dapat di-query.

## 4. Required Docs
- `docs/architecture/context-engine.md`
- `docs/ai/eval-cases/context-selection.md`

## 5. Workflow
1. Ekstraksi intent dan identifikasi proyek aktif.
2. Ambil kandidat konteks sesuai prioritas kanonikal.
3. Terapkan pemeringkatan (*ranking*) dan penyaringan (buang duplikat/forgotten).
4. Terapkan pemotongan berbatas anggaran token (*Token Budget*).
5. Susun objek Context Package yang transparan.

## 6. Validation
Pastikan zero cross-project leakage dan token tidak pernah overflow.

## 7. Docs Update
Update stage test results pada milestone M5.

## 8. Stop Conditions
Berhenti jika memori Proyek A masuk ke dalam konteks Proyek B.

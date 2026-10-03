# Skill: ai-tool

## 1. Description
Membuat skema pemanggilan fungsi/tool untuk reasoning model AI.

## 2. When Used
Saat memperluas kapabilitas yang dapat diusulkan oleh LLM.

## 3. Prerequisites
Logika eksekusi riil telah siap di backend atau Mac Agent.

## 4. Required Docs
- `docs/architecture/ai-orchestration.md`
- `docs/security/permission-model.md`

## 5. Workflow
1. Buat skema JSON/Pydantic typed untuk parameter tool.
2. Dokumentasikan fungsi tool secara lugas.
3. Hubungkan pemanggilan tool ke Permission Engine (BUKAN langsung eksekusi OS).
4. Buat mock test evaluasi tool selection.

## 6. Validation
Uji LLM dengan skenario benar dan skenario penolakan (eval-cases).

## 7. Docs Update
Catat skema tool pada arsitektur AI Orchestration.

## 8. Stop Conditions
Berhenti jika tool memberikan akses shell bebas atau bypass izin.

# Skill: security-review

## 1. Description
Memeriksa kepatuhan terhadap 15 Invarian Keamanan NEXUS.

## 2. When Used
Sebelum menutup stage atau saat menambahkan fitur sensitif.

## 3. Prerequisites
Implementasi fitur telah selesai dan siap direview.

## 4. Required Docs
- `docs/security/security-architecture.md`
- `docs/security/threat-model.md`
- `docs/SOP/06-security-review.md`

## 5. Workflow
1. Periksa ada tidaknya celah IDOR pada query database.
2. Periksa apakah ada secret atau token yang dicetak di log.
3. Pastikan tidak ada jalur eksekusi shell arbitrer.
4. Isi template `security-review.md` pada stage aktif.
5. Laporkan temuan blocking bila ada.

## 6. Validation
Seluruh cek list keamanan berstatus PASS atau NOT APPLICABLE.

## 7. Docs Update
Update stage `security-review.md`.

## 8. Stop Conditions
Berhenti dan gagalkan penutupan stage jika ada temuan BLOCKING atau HIGH risk.

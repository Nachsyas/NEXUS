# Skill: create-api

## 1. Description
Mendesain dan mengimplementasikan endpoint REST API v1 sesuai kontrak.

## 2. When Used
Saat mengekspos kapabilitas backend ke iOS Client atau Mac Agent.

## 3. Prerequisites
Skema payload dan kontrak endpoint telah didefinisikan.

## 4. Required Docs
- `docs/api/api-contract.md`
- `docs/api/error-codes.md`
- `docs/security/security-architecture.md`

## 5. Workflow
1. Tentukan URL endpoint di bawah `/api/v1`.
2. Definisikan skema Pydantic untuk request dan response envelope standar.
3. Pastikan otentikasi dan otorisasi memeriksa `current_user_id`.
4. Tambahkan penanganan error terstruktur dengan kode error resmi.
5. Buat integration/contract test.

## 6. Validation
Uji coba endpoint dengan test client; pastikan tidak ada unhandled 500 error.

## 7. Docs Update
Perbarui `docs/api/api-contract.md` jika ada endpoint baru.

## 8. Stop Conditions
Berhenti jika endpoint berpotensi membocorkan data multi-tenant (IDOR).

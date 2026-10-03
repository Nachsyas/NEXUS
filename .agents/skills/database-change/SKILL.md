# Skill: database-change

## 1. Description
Mengelola migrasi skema tabel, indeks, dan ekstensi pada PostgreSQL.

## 2. When Used
Saat menambah model, kolom, atau indeks baru pada database.

## 3. Prerequisites
Desain entitas telah divalidasi dan query pattern telah dipetakan.

## 4. Required Docs
- `docs/architecture/database-architecture.md`
- `docs/SOP/02-code-standards.md`

## 5. Workflow
1. Buat model SQLAlchemy dengan field UTC timestamp dan relasi yang tepat.
2. Generate skrip migrasi via Alembic.
3. Review skrip migrasi untuk memastikan ada logika `upgrade()` dan `downgrade()`.
4. Uji migrasi maju dan mundur pada database lokal.
5. Pastikan indeks mendukung pola query riil.

## 6. Validation
Jalankan migrasi dan pastikan tabel terbentuk dengan tipe data yang benar.

## 7. Docs Update
Dokumentasikan perubahan skema pada stage notes dan architectural docs jika relevan.

## 8. Stop Conditions
Berhenti jika migrasi bersifat destruktif tanpa backup atau rencana rollback.

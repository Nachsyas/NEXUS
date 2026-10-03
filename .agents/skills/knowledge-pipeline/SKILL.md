# Skill: knowledge-pipeline

## 1. Description
Mengimplementasikan alur parsing, chunking, embedding, dan pengindeksan dokumen.

## 2. When Used
Saat mengembangkan fitur Knowledge Vault (M10).

## 3. Prerequisites
Storage object lokal/cloud dan pgvector telah aktif.

## 4. Required Docs
- `docs/architecture/knowledge-architecture.md`
- `docs/decisions/ADR-004-pgvector-phase-1-vector-store.md`

## 5. Workflow
1. Terima file unggahan dan validasi ukuran serta tipe MIME.
2. Simpan file ke S3-compatible storage.
3. Terbitkan job pemrosesan ke background worker.
4. Ekstrak teks, pecah menjadi chunk dengan metadata halaman.
5. Generate embedding dan simpan ke tabel `knowledge_chunks`.
6. Tandai status dokumen menjadi `READY` atau `FAILED`.

## 6. Validation
Uji pencarian semantik dengan cosine distance pada pgvector.

## 7. Docs Update
Catat benchmark latensi retrieval pada `performance-budget.md`.

## 8. Stop Conditions
Berhenti jika dokumen gagal diolah namun status dibiarkan `PROCESSING` terus-menerus.

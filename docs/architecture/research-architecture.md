# Research Radar Architecture — External Intelligence

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-012  

---

## 1. Pipeline Ingesti Riset
```text
Sumber Riset Terverifikasi (ArXiv, Tech Feeds, Release Notes)
              ↓
      Ingesti Asinkron
              ↓
    Normalisasi Format & Metadata
              ↓
  Deduplikasi URL, Judul & Hash Konten
              ↓
       Klasifikasi Kategori
              ↓
  Ringkasan Eksekutif (NEXUS Summary)
              ↓
       Embedding Vektor
              ↓
  Pencocokan Minat Pengguna & Scoring
              ↓
     Research Feed Sementara
```

## 2. Siklus Hidup Item Riset
- Item riset berstatus sementara (*ephemeral*) dan akan kadaluarsa sesuai kebijakan retensi.
- Jika pengguna memilih **SAVE**, item riset dipindahkan secara permanen ke dalam **Knowledge Vault**.
- Konten eksternal tidak dipercaya (*untrusted content*) dan tidak boleh mengubah aturan sistem ataupun mengeksekusi tool.

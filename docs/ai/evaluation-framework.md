# AI Evaluation Framework — Quality & Safety

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-011, ADR-015  

---

## 1. Filosofi Evaluasi AI
Model bahasa (LLM) diuji bukan hanya dengan unit test tradisional, melainkan melalui suite evaluasi terstruktur untuk mengukur:
- Kualitas pengambilan memori (*Memory Retrieval Precision & Recall*).
- Batasan dan anggaran token konteks (*Context Selection & Budgeting*).
- Resistensi terhadap injeksi prompt (*Prompt Injection Resistance*).
- Kepatuhan skema pemilihan tool (*Tool Selection Safety*).
- Kejujuran penolakan saat bukti tidak ada (*Knowledge Grounding*).

## 2. Metrik Pengujian Inti
- `Recall@K` & `Precision@K`: Proporsi memori relevan yang berhasil ditarik.
- `Cross-Project Leakage Rate`: Wajib 0% (tidak boleh ada memori Proyek A yang bocor ke Proyek B).
- `Forgotten Memory Inclusion Rate`: Wajib 0% (memori yang sudah di-forget tidak boleh muncul).
- `Tool Hallucination Rate`: Persentase LLM memanggil aksi yang tidak ada di schema.

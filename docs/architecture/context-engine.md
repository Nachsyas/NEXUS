# Context Engine Architecture — Bounded Relevance

**Status:** LOCKED  
**Version:** 1.1  

---

## 1. Peran Context Engine
Context Engine bertanggung jawab mengumpulkan, menyaring, memprioritaskan, dan membungkus informasi yang relevan ke dalam paket konteks (*Context Package*) sebelum diteruskan ke Model Reasoning.

## 2. Pipeline Pemrosesan
```text
User Request
    ↓
Intent Analysis & Extraction
    ↓
Entity Resolution
    ↓
Active Project Resolution
    ↓
Candidate Retrieval
    ├── Conversation History (Recent & Summarized)
    ├── Personal Memory (Active, High Confidence)
    ├── Project Memory (Scoped to Active Project)
    ├── Knowledge Vault (Vector Search Chunks)
    ├── Device State (Telemetry snapshot)
    └── Research Radar (Relevant items)
    ↓
Ranking & Relevance Scoring
    ↓
Filtering (Deduplication, Privacy, Sensitivity)
    ↓
Token Budget Allocation (Bounded Budget)
    ↓
Context Package Assembly
```

## 3. Prioritas Pengambilan Konteks
1. Current user request
2. Current active conversation context
3. Explicit active project context
4. Explicit personal memory
5. Relevant knowledge chunks
6. Current verified device state
7. Recent relevant context
8. Research items
9. Behavioral inference

## 4. Invarian Batasan
- Konteks wajib dibatasi oleh *Token Budget* (tidak boleh melebihi batas model).
- Dilarang menggabungkan memori Proyek A ke dalam obrolan Proyek B (*strict project isolation*).
- Dilarang memuat memori yang berstatus `FORGOTTEN` atau `SUPERSEDED`.

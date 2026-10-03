# AI Orchestration & Model Router

**Status:** LOCKED  
**Version:** 1.1  
**Decision Reference:** ADR-011, ADR-015  

---

## 1. Arsitektur Model Router
NEXUS bersifat agnostik terhadap vendor AI. Komponen AI dipisahkan oleh antarmuka abstrak:

```text
                  Application Service
                           │
                           ▼
                     AI Service
                           │
                           ▼
                     Model Router
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
Provider Adapter A   Provider Adapter B   Provider Adapter C
  (e.g., Anthropic)    (e.g., OpenAI)       (e.g., Local/Self)
```

## 2. Kriteria Perutean (Routing Criteria)
- Tipe tugas (penalaran kompleks, ekstraksi cepat, ringkasan riset, formatting).
- Kompleksitas dan latensi yang ditargetkan.
- Kebijakan privasi (misal: Private Session dapat merutekan ke model tertentu).
- Ketersediaan dan error fallback otomatis.

## 3. Tool Calling & Otorisasi
- LLM hanya berhak mengusulkan *Structured Tool Call* dengan skema yang tervalidasi.
- **LLM BUKAN Otoritas Keamanan:** Usulan tool dialihkan ke runtime *Permission Engine* dan *Risk Policy* di luar LLM.
- Jika aksi dinilai berisiko atau memerlukan izin pengguna, eksekusi ditahan hingga ada konfirmasi eksplisit dari pengguna.

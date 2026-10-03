# Performance Budget & Constraints

**Status:** LOCKED CANONICAL POLICY  
**Version:** 1.1  
**Decision Reference:** ADR-014  

---

## 1. Prinsip Pengukuran (Measurement-First Performance Engineering)
Pengembangan performa NEXUS mengikuti kaidah mutlak:
> **REPRODUCE → MEASURE → TRACE → IDENTIFY BOTTLENECK → CAPTURE BASELINE → CHANGE SMALLEST COMPONENT → MEASURE AGAIN → DOCUMENT**

Dilarang keras menetapkan target performa numerik definitif sebelum baseline empiris diukur.
Sebelum pengukuran riil dijalankan:
- **Baseline:** `NOT MEASURED`
- **Observed:** `NOT MEASURED`
- **Target:** `TBD AFTER BASELINE`
- **Regression:** `DEFINED AFTER BASELINE`

Satu-satunya panduan engineering awal yang disetujui sebelumnya sebagai batas desain arsitektur lokal adalah alokasi penyimpanan lokal iOS:
- **iOS Local Storage Guideline:** `~1–2 GB` penggunaan normal, idealnya tetap di bawah `~3 GB` (untuk cache, embedding offline, dan data lokal).

---

## 2. Matriks Anggaran Performa (Measurement-First Tracking Table)

| Metrik | Komponen | Baseline | Observed | Target | Regression Threshold | Status |
|---|---|---|---|---|---|---|
| **API p95 Latency** | REST API endpoints standar | NOT MEASURED | NOT MEASURED | TBD AFTER BASELINE | TBD AFTER BASELINE | PENDING BASELINE (M0/M1) |
| **First Token Latency** | AI Streaming Response | NOT MEASURED | NOT MEASURED | TBD AFTER BASELINE | TBD AFTER BASELINE | PENDING BASELINE (M4) |
| **Context Assembly Time** | Context Engine retrieval & ranking | NOT MEASURED | NOT MEASURED | TBD AFTER BASELINE | TBD AFTER BASELINE | PENDING BASELINE (M5) |
| **Vector Search p95 Latency** | pgvector similarity retrieval | NOT MEASURED | NOT MEASURED | TBD AFTER BASELINE (lihat TBD-025) | TBD AFTER BASELINE | PENDING BASELINE (M3/M10) |
| **Mac Action Dispatch Latency** | WebSocket Action Dispatch to ACK | NOT MEASURED | NOT MEASURED | TBD AFTER BASELINE | TBD AFTER BASELINE | PENDING BASELINE (M7/M8) |
| **iOS Memory Footprint** | iOS Client runtime active | NOT MEASURED | NOT MEASURED | TBD AFTER BASELINE | TBD AFTER BASELINE | PENDING BASELINE (M0/M2) |
| **iOS Local Storage Footprint** | Local offline cache & metadata | NOT MEASURED | NOT MEASURED | ~1–2 GB (ideal < 3 GB) | > 3 GB | APPROVED GUIDELINE |
| **Mac Agent Memory Footprint** | Mac background utility process | NOT MEASURED | NOT MEASURED | TBD AFTER BASELINE | TBD AFTER BASELINE | PENDING BASELINE (M6/M7) |

---

## 3. Disiplin Pembaruan Budget
1. Baseline ditangkap saat implementasi pertama yang berfungsi (*working implementation*) pada stage terkait selesai dan dapat diuji.
2. Setiap kali benchmark dijalankan, angka faktual diisikan ke kolom `Baseline` dan `Observed` pada dokumen `performance-results.md` di stage aktif.
3. Target numerik definitif baru diajukan dan disepakati setelah baseline empiris pertama terdokumentasi.

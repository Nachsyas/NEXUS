# SOP 07 — Performance Engineering & Profiling

**Status:** CANONICAL SOP  
**Version:** 1.1  

## Alur Resolusi Kinerja:
1. **Reproduce:** Buat skrip untuk mereproduksi kondisi lambat secara konsisten.
2. **Measure:** Tangkap metrik baseline angka (p50, p95, p99).
3. **Trace:** Analisis bottleneck (DB slow query, token overhead, alokasi memori).
4. **Fix:** Terapkan perbaikan terkecil yang bertanggung jawab.
5. **Measure Again:** Uji ulang dan pastikan terjadi perbaikan nyata sebelum mencatat ke dokumentasi.

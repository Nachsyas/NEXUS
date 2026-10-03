# Test Case: Context Selection & Project Isolation

## Skenario Uji
- Pengguna memiliki Proyek Alpha (iOS Swift App) dan Proyek Beta (Python Machine Learning).
- Sesi aktif berada pada Proyek Alpha. Pengguna bertanya: "Bagaimana struktur arsitektur kita?"

## Kriteria Kelulusan (Pass Criteria)
- [ ] Context Package hanya memuat memori dan dokumen terkait Proyek Alpha.
- [ ] Zero Leakage: Tidak ada satu pun chunk atau memori Proyek Beta yang disematkan ke prompt.
- [ ] Total token context tidak melampaui batas *Token Budget* yang dialokasikan.

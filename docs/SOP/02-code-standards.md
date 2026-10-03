# SOP 02 — Code Standards & Quality Guidelines

**Status:** CANONICAL SOP  
**Version:** 1.1  

## 1. Standar Python / FastAPI
- Menggunakan type annotations lengkap pada fungsi dan method.
- Skema input dan output wajib menggunakan Pydantic BaseModel.
- Menghindari mutable default arguments dan global state tersembunyi.
- Tangani error dengan exception terstruktur, jangan biarkan unhandled exception bocor ke transport layer.

## 2. Standar Swift / SwiftUI
- Mengikuti idiomatic Swift: PascalCase untuk tipe/protokol, camelCase untuk method/variabel.
- Manfaatkan Swift Structured Concurrency (`async`/`await`, `Task`, `Actor`). Hindari Combine baru jika tidak diperlukan.
- Tampilan SwiftUI wajib memisahkan state (`@State`, `@Observable`) dan logic dari UI view.

# SOP 08 — Observability & Structured Logging

**Status:** CANONICAL SOP  
**Version:** 1.1  

## Format Log Terstruktur:
Setiap log operasional wajib menyertakan identitas korelasi:
- `request_id`: ID unik request HTTP atau koneksi WS.
- `correlation_id`: ID rantai alur antarkomponen.
- `action_id`: ID pelacakan aksi remote (jika relevan).
- `user_id`: ID pengguna pemilik aksi (jika terotentikasi).
- **Redaksi:** Dilarang mencetak authorization header, cookie, password, atau payload rahasia.

# SOP 03 — Git Workflow & Commit Guidelines

**Status:** CANONICAL SOP  
**Version:** 1.1  

## 1. Aturan Commit
- Format pesan commit: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Satu commit fokus pada satu tujuan logis.
- Dilarang keras melakukan commit terhadap file credential, `.env`, sertifikat pribadi, atau token rahasia.
- Jika terjadi kebocoran secret ke Git: Kredensial wajib segera dirotasi / dicabut di server target.

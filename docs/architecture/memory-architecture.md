# Memory Architecture — Storage of Meaning

**Status:** LOCKED CANONICAL ARCHITECTURE  
**Version:** 1.2  
**Decision Reference:** ADR-012  

---

## 1. Filosofi Memori
> **"Store meaning, not everything."**

NEXUS tidak menyimpan seluruh log percakapan sebagai memori. Memori adalah abstraksi nilai esensial yang diekstraksi dari interaksi pengguna setelah melalui verifikasi kepentingan dan sensitivitas.

---

## 2. Taksonomi Tipe Memori (10 Canonical Memory Types)
Setiap entri memori diklasifikasikan secara ketat ke dalam salah satu dari 10 tipe kanonikal berikut:
- `PERSONAL_FACT`: Fakta spesifik tentang pengguna (misal: nama panggilan, zona waktu).
- `PREFERENCE`: Preferensi eksplisit pengguna (misal: gaya bahasa lugas, format kode).
- `INTEREST`: Minat teknologi atau topik riset yang diminati pengguna.
- `SKILL`: Keahlian teknis atau domain yang dikuasai pengguna.
- `GOAL`: Target atau sasaran jangka panjang pengguna.
- `PROJECT_FACT`: Fakta arsitektur atau keputusan bisnis sebuah proyek.
- `PROJECT_DECISION`: Keputusan teknis yang telah dikunci dalam proyek.
- `PROJECT_PROGRESS`: Pencapaian milestone terkini proyek.
- `PROJECT_NEXT_ACTION`: Langkah prioritas berikutnya pada proyek.
- `BEHAVIOR_PATTERN`: Pola perilaku (skema siap di Phase 1, aktivasi analitik di Phase 2+).

*(Catatan: Terminologi generik seperti FACT, DECISION, atau CONTEXT bukan tipe memori level atas yang sah).*

---

## 3. Tingkat Sensitivitas Memori (Sensitivity Levels)
Memori dievaluasi terhadap 4 tingkatan sensitivitas deterministik:
- `LOW`: Fakta umum, minat publik, atau preferensi non-kritis.
- `MEDIUM`: Fakta internal proyek, alur kerja pribadi.
- `HIGH`: Informasi pribadi sensitif, detail lingkungan lokal.
- `RESTRICTED`: Konteks privat yang memerlukan isolasi ketat dan audit akses.

### Hasil Klasifikasi Khusus: `NEVER_STORE`
Informasi yang mengandung kredensial, rahasia sistem (*API keys, passwords, private keys*), data sesi privat, atau data terlarang lainnya diklasifikasikan sebagai `NEVER_STORE`.
- **Semantik:** Penolakan mutlak (*rejection*). Informasi ini dilarang keras untuk dipersistensikan ke dalam general Memory dalam kondisi apa pun.

---

## 4. Sumber Bukti Memori (Canonical Source Types / Provenance)
Asal-usul pembentukan memori dilacak melalui 6 tipe sumber kanonikal:
- `CONVERSATION`: Diekstraksi secara otomatis dari dialog percakapan pengguna.
- `USER_EXPLICIT`: Diinput atau diedit secara manual dan eksplisit oleh pengguna di Control Center.
- `PROJECT_UPDATE`: Dihasilkan dari aktivitas sinkronisasi repositori atau pembaruan status proyek.
- `DOCUMENT`: Diekstraksi dari analisis dokumen pada Knowledge Vault.
- `SYSTEM_INFERENCE`: Disimpulkan oleh reasoning engine backend dari korelasi berbagai artefak.
- `BEHAVIORAL_INFERENCE`: Disimpulkan dari pola penggunaan berulang lintas sesi.

---

## 5. Pipeline Penulisan Memori
```text
New Information from User Interaction
              │
              ▼
    Worth Storing? (Evaluation)
              │
              ▼
      Sensitivity Check (Secrets Filter) ──NEVER_STORE──► [REJECT / DO NOT STORE]
              │ (LOW / MEDIUM / HIGH / RESTRICTED)
              ▼
        Classification (10 Canonical Types)
              │
              ▼
       Deduplication
              │
              ▼
     Conflict Detection
              │
              ▼
Create / Update / Supersede / Ignore
```

---

## 6. Status & Forget Semantics
- Status: `ACTIVE`, `SUPERSEDED`, `EXPIRED`, `FORGOTTEN`, `PENDING_CONFIRMATION`.
- Saat pengguna meminta melupakan memori (`POST /api/v1/memories/{id}/forget`), status berubah menjadi `FORGOTTEN`.
- Memori berstatus `FORGOTTEN` atau `SUPERSEDED` dijamin tidak akan pernah ditarik oleh Context Engine ke dalam prompt LLM.

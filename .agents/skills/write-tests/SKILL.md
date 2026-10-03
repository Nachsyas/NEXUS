# Skill: write-tests

## 1. Description
Membuat unit test, integration test, dan contract test otomatis.

## 2. When Used
Setiap kali menulis fitur baru atau mereproduksi bug.

## 3. Prerequisites
Target kode yang diuji telah memiliki antarmuka yang jelas.

## 4. Required Docs
- `docs/SOP/04-testing.md`

## 5. Workflow
1. Buat skenario kasus uji positif, negatif, dan batas (*boundary values*).
2. Tulis test menggunakan pytest (Python) atau Swift Testing / XCTest (Swift).
3. Jalankan test runner lokal dan pastikan hasil konsisten.
4. Catat ringkasan pengujian pada `test-results.md`.

## 6. Validation
Semua tes yang ditulis wajib lulus (*100% pass rate*).

## 7. Docs Update
Update `test-results.md` pada stage aktif.

## 8. Stop Conditions
Berhenti jika test mengandalkan mock data palsu yang menutupi cacat arsitektur.

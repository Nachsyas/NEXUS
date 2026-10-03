# Skill: mac-agent-action

## 1. Description
Mengelola siklus hidup eksekusi aksi remote pada workstation Mac.

## 2. When Used
Saat mengeksekusi capability Mac yang diminta oleh pengguna.

## 3. Prerequisites
Perangkat berstatus PAIRED dan koneksi WSS berstatus ONLINE.

## 4. Required Docs
- `docs/architecture/mac-agent-architecture.md`
- `docs/api/mac-agent-protocol.md`
- `docs/security/action-risk-model.md`

## 5. Workflow
1. Bungkus perintah ke dalam envelope aksi terstandar (bawa TTL & idempotency key).
2. Periksa level risiko dan evaluasi Permission Engine (tahan jika status ASK).
3. Dispatch via WSS ke Mac Agent.
4. Mac Agent memvalidasi lokal, mengeksekusi capability, dan mengirimkan ACK/Result.
5. Catat hasil ke audit log.

## 6. Validation
Verifikasi bahwa aksi kadaluarsa atau duplikat ditolak secara deterministik.

## 7. Docs Update
Update log eksekusi dan stage records pada M8.

## 8. Stop Conditions
Berhenti jika Mac Agent diminta menjalankan arbitrary shell script.

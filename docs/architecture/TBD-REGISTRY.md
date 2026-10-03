# TBD Registry — Decisions To Be Decided

**Status:** CANONICAL REGISTRY  
**Version:** 1.4  

Setiap item bertanda TBD di bawah ini belum diputuskan. Agent dilarang mengimplementasikan asumsi sepihak sebelum keputusan diresmikan via ADR berstatus ACCEPTED atau dokumen spesifikasi yang disetujui pengguna.

| TBD-ID | Topik | Komponen Terdampak | Alasan Masih TBD | Pilihan Alternatif | Keputusan Wajib Sebelum | Status | ADR Terkait |
|---|---|---|---|---|---|---|---|
| **TBD-001** | Primary cloud/deployment provider | Infrastructure | Memerlukan analisis biaya operasional dan kepatuhan hosting | AWS, GCP, Fly.io, Hetzner | M14 Beta / Production | OPEN | - |
| **TBD-002** | Production S3-compatible provider | Knowledge & Storage | Evaluasi integrasi cloud storage | AWS S3, Cloudflare R2, MinIO Self-hosted | M10 Production Deploy | OPEN | - |
| **TBD-003** | Primary LLM provider(s) | AI Orchestrator | Evaluasi kualitas penalaran, harga token, dan privasi | Anthropic Claude, OpenAI, Local Open-Weights | M4 AI Conversation | OPEN | ADR-011 |
| **TBD-004** | Embedding model | Vector Store & RAG | Benchmark akurasi retrieval bahasa & kode | OpenAI text-embedding-3, Voyage AI, Local BGE/Nomic | M3 / M10 Feature | OPEN | ADR-004 |
| **TBD-005** | Background worker implementation | Workers | Menentukan framework antrian asinkron Python | Celery, ARQ, SAQ, Dramatiq | M10 Knowledge Ingestion | OPEN | - |
| **TBD-006** | Queue/job implementation broker | Backend Workers | Bergantung pada pilihan worker engine | Redis Queue, RabbitMQ, PostgreSQL Queue | M10 Knowledge Ingestion | OPEN | - |
| **TBD-007** | Production observability provider | Monitoring | Evaluasi tracing dan log telemetry | OpenTelemetry + Grafana/Loki, Datadog, Sentry | M14 Beta Reliability | OPEN | - |
| **TBD-008** | Production secret manager | Security Infrastructure | Penentuan brankas kunci production | HashiCorp Vault, AWS Secrets Manager, Infisical | M14 Production Deploy | OPEN | - |
| **TBD-009** | Research source implementation | Research Radar | Pilihan API agregator riset | ArXiv API, Semantic Scholar, Tavily, NewsAPI | M11 Research Radar | OPEN | - |
| **TBD-010** | Production notification architecture | iOS Notifications | Desain sistem notifikasi server-to-device | APNs Direct via HTTP/2, Firebase Cloud Messaging | M12 / M13 Feature | OPEN | - |
| **TBD-011** | NEXUS license / distribution model | Project Governance | Menunggu keputusan pemangku kepentingan komersial | Proprietary, BSL, Fair-source, Dual License | Public Distribution | OPEN | - |
| **TBD-012** | Production deployment topology | Infrastructure | Arsitektur clustering & ingress | Docker Compose Single Node, K8s, Nomad | M14 Beta Deploy | OPEN | - |
| **TBD-013** | Python package/env manager | Backend Environment | Standardisasi tooling manajemen dependensi | uv (Astral) | M0 Foundation Setup | PROPOSED BY M0 IMPLEMENTATION | ADR-016 |
| **TBD-014** | Primary ID strategy | Database Architecture | Evaluasi format ID (UUIDv4 vs UUIDv7 vs ULID) | UUIDv7 (RFC 9562 time-ordered) | M0 Database Migration | PROPOSED BY M0 IMPLEMENTATION | ADR-017 |
| **TBD-015** | Python linter/formatter/type check | Backend CI | Standardisasi pipeline linting | Ruff + Mypy | M0 CI Baseline | PROPOSED BY M0 IMPLEMENTATION | ADR-018 |
| **TBD-016** | Local S3-compatible implementation | Local Development | Tool simulasi S3 untuk dev lokal | MinIO container, LocalStack, File-system mock | M0 Development Setup | OPEN | - |
| **TBD-017** | Local background-job implementation | Local Development | Engine runner job lokal | Inline background tasks, Redis worker lokal | M0 / M10 Development | OPEN | - |
| **TBD-018** | AI evaluation runner/framework | AI Testing | Pemilihan framework evaluasi otomatis | Promptfoo, Ragas, DeepEval, Custom Test Runner | M4 AI Evaluation | OPEN | - |
| **TBD-019** | Push notification provider | iOS Client | Layanan pengiriman APNs | Apple Push Notification service (APNs) murni | M12 Voice/Actions | OPEN | - |
| **TBD-020** | Device cryptographic key algorithm & signing scheme | Mac Agent & Device Trust | Menentukan algoritma keypair asimetris lokal dan skema challenge-response | Ed25519, ECDSA (P-256), Secure Enclave integration | M6 Device Pairing | OPEN | ADR-007 |
| **TBD-021** | Pairing-code TTL & replay-window configuration | Device Trust & Security | Menentukan durasi kadaluarsa pairing code dan batas jendela toleransi replay | 3 menit, 5 menit, 10 menit | M6 Device Pairing | OPEN | - |
| **TBD-022** | Heartbeat interval, stale threshold, & reconnect timing defaults | Realtime Architecture & Mac Agent | Menentukan interval periodik heartbeat WSS, ambang stale, dan backoff rekoneksi | Interval 15s/30s, Timeout 30s/60s, Stale 45s | M7 Device Intelligence | OPEN | ADR-008 |
| **TBD-023** | Phase 1 default permission matrix per capability | Permission Engine & Security | Menentukan keputusan awal (ALLOW vs ASK) untuk tiap capability sebelum evaluasi runtime | Matriks izin default per-capability (Proposed di permission-model.md) | M8 Remote Safe Actions | OPEN | ADR-015 |
| **TBD-024** | Phase 1 action risk mapping per capability | Action Risk Model & Mac Agent | Mengklasifikasikan tingkat risiko (LOW, MEDIUM, HIGH, CRITICAL) untuk tiap aksi aman Mac | Pemetaan risiko formal per capability | M8 Remote Safe Actions | OPEN | - |
| **TBD-025** | pgvector index strategy & performance target | Database & Performance | Memilih strategi indeks (HNSW vs IVFFlat) dan target latensi retrieval berbasis data riil | HNSW, IVFFlat, Flat (tanpa indeks untuk skala kecil) | First production-scale vector benchmark | OPEN | ADR-004 |
| **TBD-026** | PostgreSQL major version baseline | Database & Environment | Menetapkan versi major resmi PostgreSQL untuk dev lokal dan container | PostgreSQL 16 (pgvector/pgvector:pg16) | M0 Foundation Setup | PROPOSED BY M0 IMPLEMENTATION | ADR-019 |
| **TBD-027** | Mac Agent Phase 1 packaging architecture | Mac Agent & OS Integration | Evaluasi packaging macOS untuk Keychain, TCC, lifecycle, status menu bar UI | Swift Package CLI Executable vs App Bundle (.app) Menu Bar Utility | M6 Device Pairing / M7 Device Intelligence | OPEN | ADR-007 |

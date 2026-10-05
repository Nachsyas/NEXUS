# Milestone M3: Known Issues & Technical Debt

## 1. Technical Debt & Open Items
1. **LIVE APPLE E2E: NOT YET MANUALLY VERIFIED:**
   - *Status:* OPEN (Carried forward from M1/M2).
   - *Impact:* Automated testing uses `MockAppleVerifier` and HTTP mocking. Real Sign in with Apple on physical devices with Apple Developer credentials remains open for physical device verification.

2. **Vector Index Optimization (TBD-025):**
   - *Status:* OPEN.
   - *Impact:* Pgvector table currently uses exact flat sequential scan for similarity search (`<=>`). While optimal and ultra-fast (<35ms) for early tenant sizes, scale testing will evaluate HNSW vs IVFFlat indexes when dataset sizes warrant index maintenance overhead.

3. **Production Embedding Provider Selection (TBD-030):**
   - *Status:* OPEN.
   - *Impact:* Production semantic search returns HTTP 503 until a production embedding model (e.g. OpenAI `text-embedding-3-small` or self-hosted BGE) is selected and integrated via governance.

# NEXT ACTIONS: Milestone M2 Completion & Next Steps

**Date:** 2026-10-05  
**Current Milestone:** Milestone M2 — Projects (PRE-MERGE CORRECTIVE PASS COMPLETE ON `milestone/m2-projects`)  
**Active PR:** PR #1 (`https://github.com/Nachsyas/NEXUS/pull/1`)  
**Next Milestone:** Milestone M3 — Memory Core (STRICTLY PENDING PR #1 MERGE & EXPLICIT USER AUTHORIZATION)  

---

## Completed Corrective Actions (Pre-Merge Pass)
1. [x] Implement preference `default_project_id` ownership verification in `UserService.update_user_preferences` (cross-user rejection with 404, null clearing).
2. [x] Implement bounded deterministic slug collision retry loop (5 attempts) with nested savepoints (`db.begin_nested()`) preventing 500 errors on concurrent creation.
3. [x] Serialize project activation on user row lock with `select(User.id).where(User.id == user_id).with_for_update()` backed by `uq_projects_user_active`.
4. [x] Align project priority enum across backend, iOS, tests, and contract to `LOW`, `NORMAL`, `HIGH` (removed `CRITICAL`).
5. [x] Remove future `memory_count` and `knowledge_count` placeholders from M2 context endpoint, schemas, iOS models, and UI.
6. [x] Correct roadmap drift in PR description and documentation to canonical roadmap: M4 AI Conversation, M5 Context Engine, M6 Device Pairing.
7. [x] Execute real concurrency unit tests for slug collision and active focus safety via `asyncio.gather` (37/37 tests passing).
8. [x] Verify database migration forward, rollback, and re-apply cycle (`upgrade head` -> `downgrade -1` -> `upgrade head`) with orphan cleanup.
9. [x] Verify client targets: iOS Simulator (`** BUILD SUCCEEDED **`) and Mac Agent (`Build complete!`).
10. [x] Re-run governance check: no local file paths (`file:///`) in repo markdown.

---

## Immediate Next Steps
1. [ ] Commit corrective pass changes to `milestone/m2-projects`.
2. [ ] Push changes to `origin milestone/m2-projects`.
3. [ ] Update PR #1 description via `gh pr edit 1`.
4. [ ] Verify GitHub Actions CI status for PR #1.
5. [ ] Present Final Corrective Report and STOP (Do NOT merge PR #1; do NOT start M3).

---

## Subsequent Milestone (Phase 1 / M3 — Memory Core)
*Strict stop boundary: Do NOT initiate M3 until PR #1 is merged to main and explicit user authorization is provided.*
- **Canonical Order:** M0 Foundation -> M1 Account & Identity -> M2 Projects -> M3 Memory Core -> M4 AI Conversation -> M5 Context Engine -> M6 Device Pairing.

# Milestone M2: Known Issues & Caveats

## 1. Preserved System Caveats
- **Live Apple E2E Authentication:**
  `LIVE APPLE E2E: NOT YET MANUALLY VERIFIED`
  - As documented in Milestone M1, end-to-end verification of Sign in with Apple against Apple's production identity service requires a physical Apple device provisioned with an active Apple Developer Team ID and App ID entitlements.
  - Production code for Apple identity token verification (`ProductionAppleVerifier`) and the iOS UI (`AuthView` + `SignInWithAppleButton`) are fully implemented and verified via unit tests and mock verifiers. This caveat remains open until manual physical device testing is executed.

## 2. Milestone M2 Specific Considerations
- **None Blocking:** All 50 M2 acceptance criteria are fully met.
- **Future Scope Pointers:**
  - Automated project summarization via LLM will be introduced in Milestone M5 (Context Engine).
  - Associating memory items, vector embeddings, and conversation sessions with projects will be introduced in Milestone M3 (Memory Core).

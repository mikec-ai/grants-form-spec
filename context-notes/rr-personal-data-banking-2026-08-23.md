---
type: Context Note
title: R&R Personal Data banking receipt
timestamp: '2026-08-24T03:26:18Z'
superbee_updated_by: codex
---
# Summary

R&R Personal Data 1.2 is now declaratively authored, exact-source validated, and banked unregistered in the Simpler consumer. The producer and consumer flows remained generic: no form-specific compiler, loader, renderer, adapter, conformance, or registration branch was added.

- Timed start: `2026-08-24T03:00:15Z` (`2026-08-23 23:00:15 EDT`).
- Producer PR: `mikec-ai/grants-form-spec#68`, merged revision `6b5717763d5769efd8b92a3cdbb61bc6935909fb` at `2026-08-24T03:20:22Z` (20m 07s).
- Producer hosted CI completed at `2026-08-24T03:21:34Z` (21m 19s): 112 TypeScript tests, 270 Python tests (9 skipped), 29 exact-XSD fixtures/profiles, evidence/artifact/promotion/package gates, and zero unclassified fields/exceptions.
- Generic promotion started at `2026-08-24T03:21:58Z` and generated consumer PR `mikec-ai/simpler-grants-gov#61`.
- Consumer PR merged revision `dd2da405ac63b2221e1966b5f3192fd24744dcfe` at `2026-08-24T03:26:18Z`: 4m 20s for promotion and CI; 26m 03s total.
- Consumer receipt: bundle SHA-256 `0f2e62ee303de460e2110a6cb13c9001924afddbf8cf15858d7bc7ac52c340d3`; 37 selected forms and 426 artifacts; `registrations.json` unchanged.
- Reuse: `research-person/name`, one shared declarative director capture shape, and one shared XML director mapping across role-qualified PD/PI and repeated co-PD/co-PI questions.
- New semantic identities: `personal-data/project-director` and `personal-data/co-project-director`; the common shape does not conflate the roles.
- Intentionally deferred from banking/release: race and disability exclusivity interactions, SF-424 R&R name prefill, dynamic repeat controls, browser save/reload and locked/print behavior, accessibility, privacy/access controls, analytics, exports, retention, and production registration.
- Workflow friction observed: bot-authored consumer PR checks required a one-time manual Actions approval before the existing bank-only CI would start.

This receipt completes [Author and integrate R&R Personal Data](../tasks/author-integrate-rr-personal-data.md) at the banking boundary. The detailed source and architecture audit remains on that task; catalog browser and operational release gates remain separate work.

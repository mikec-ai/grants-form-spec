---
type: Task
title: Bank PHS 398 Research Plan in SGG
priority: P0
description: >-
  Promote the already-delivered Research Plan artifact closure into the SGG
  consumer bank without inventing a runtime identity or reopening architecture.
superbee_progress_status: in_progress
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-24T02:59:00.691Z'
assignee: consumer_promotion_agent
---
# Goal

Bank PHS 398 Research Plan in the public SGG consumer from an exact immutable producer revision, using the generic supervised promotion path.

# Why now

- Producer PR #60 is merged and the form serves 213,859 recorded two-year form instances.
- The producer package already composes thirteen role-qualified attachment questions over the shared Attachment Form mechanism.
- This is the only form on the current 33-form producer main that is not in the current 32-form consumer bank.

# Acceptance criteria

- Pin an exact producer revision containing PHS 398 Research Plan and promote its complete transitive artifact and official-XSD closure.
- Verify bundle, artifact, provenance, source, and XSD digests through the existing generic consumer gates.
- Leave runtime identity, compatibility projection, registration, preview, and production enablement unchanged.
- Add no Research Plan-specific compiler, adapter, loader, renderer, or conformance branch.
- Record producer and consumer revisions, selected artifact count, bundle hash, PR, and gate results in the delivery receipt.
- Preserve the existing human semantic, policy, instruction, accessibility, lifecycle, and release gates as explicit downstream work.

# Scope boundary

This task proves low-cost cross-repository banking. It does not claim production readiness, runtime parity, or resolution of the documented cross-form policy conditions.

# Promotion attempt receipt, 2026-08-23

- Consumer baseline: public fork `mikec-ai/simpler-grants-gov` main at `12977071e36c041a5f469a28006fcb843b973f30`.
- Attempted immutable producer revision: `a237bc9bdbc34784652840946faf46d53e10e3a4`.
- Requested additive selection: `phs398-research-plan`, `phs-human-subjects`, `nifa-supplemental`, and `phs-inclusion-enrollment-report` over the existing 32-form bank.
- Producer preflight passed, but consumer promotion failed closed before mutation because Research Plan pinned official XSD SHA `6e7171465d1f...` while the producer fixture was normalized SHA `9fb4f0f4be97...`.
- Producer repair is draft PR https://github.com/mikec-ai/grants-form-spec/pull/66. Consumer work remains unchanged until that PR is independently reviewed and merged; promotion will repin to the producer merge SHA.
- No runtime identity, registration, preview, compatibility projection, or HHS repository was changed.

[depends on](author-integrate-phs398-research-plan.md)

[consumer delivery uses](automate-cross-repo-form-promotion.md)

# Rebased cohort promotion receipt, 2026-08-23

- Draft consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/58
- Consumer base: `9fa568e1e6eb04e7218a9685cdf255215080cafb`; consumer head: `11038593df1e125c62ce43fad8273144f3cf93ed`.
- Immutable producer revision: `70fa65f82f66901f8a6a330aa8ef70479ded9b5e`; source bundle SHA-256: `4b147e74598d4abd8fe9e00926ec66c7eb35809119e5c0579b737e73ea376289`.
- Automated consumer PR #56 concurrently banked PHS Inclusion Enrollment Report and refreshed the same producer bundle. After rebasing, PR #58 adds only PHS 398 Research Plan and PHS Human Subjects and Clinical Trials.
- The complete bank contains 36 forms and 418 selected artifacts. Runtime-enabled forms remain 29 and registered forms remain 5. Runtime-identity SHA-256 remains `7e85abbd0796bf80396483e0eb9381b2159da94f0923b7b5e7967f6b559810cc`; registration SHA-256 remains `01b1d451dee808b1f6241ae63841d1bd90839b73cda701765b407f3ae98b7ff6`.
- Exact root XSDs and transitive artifact closure were vendored and verified for the two additions. No identity, registration, preview, compiler, adapter, renderer, or form-specific consumer branch was added.
- Local gates after rebase: producer preflight passed 109 TypeScript and 250 Python tests; consumer non-DB form-spec suite passed 233 tests; focused integrity/provenance/registration/updater suite passed 39 tests; repository-native format, Ruff, and mypy gates passed.
- PR #58 is intentionally held for infrastructure PR #59. After #59 merges, it will be rebased again so overlapping inventory assertions can be removed and the final delta can classify as bank-only. Independent review and hosted CI remain required before merge.

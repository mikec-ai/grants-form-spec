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
  at: '2026-08-24T02:50:54.761Z'
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

# Successful cohort promotion receipt, 2026-08-23

- Draft consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/58
- Consumer base: `32f09a1ee`; consumer head: `535720a081d25eb82fd2611a863759db8690ab49`.
- Immutable producer revision: `70fa65f82f66901f8a6a330aa8ef70479ded9b5e`; source bundle SHA-256: `4b147e74598d4abd8fe9e00926ec66c7eb35809119e5c0579b737e73ea376289`.
- The complete bank now contains 36 forms and 418 selected artifacts. NIFA Supplemental was already banked on consumer main; this promotion adds PHS 398 Research Plan, PHS Human Subjects and Clinical Trials, and PHS Inclusion Enrollment Report from the same immutable bundle.
- Runtime-enabled forms remain 29 and registered forms remain 5. The runtime-identity and registration files are byte-identical before and after promotion; all seven bank-only forms fail closed at runtime.
- Exact root XSDs were vendored and verified for all three newly added forms. No identity, registration, preview, compiler, adapter, renderer, or form-specific consumer branch was added.
- Local gates: producer preflight passed 109 TypeScript and 250 Python tests; consumer non-DB form-spec suite passed 233 tests; focused integrity/provenance/registration/updater suite passed 39 tests; repository-native format, Ruff, and mypy gates passed.
- The DB-backed SF-424A lifecycle test remains an environment-only local exception because host `grants-db` is unavailable. Hosted CI is running; this task remains in progress until independent review and merge.

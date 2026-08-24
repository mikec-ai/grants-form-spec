---
type: Task
title: Bank PHS 398 Research Plan in SGG
priority: P0
description: >-
  Promote the already-delivered Research Plan artifact closure into the SGG
  consumer bank without inventing a runtime identity or reopening architecture.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-24T03:12:34.733Z'
assignee: consumer_promotion_agent
---
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
  at: '2026-08-24T03:07:31.629Z'
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
- Final consumer base: `c7a3a9e9da217131bc38a9b1bc7d57d3a273796d`; consumer head: `b0ab837dc1be0f1af89cd95a2439ddad0f2fa40c`.
- Immutable producer revision: `70fa65f82f66901f8a6a330aa8ef70479ded9b5e`; source bundle SHA-256: `4b147e74598d4abd8fe9e00926ec66c7eb35809119e5c0579b737e73ea376289`.
- Automated consumer PR #56 concurrently banked PHS Inclusion Enrollment Report and refreshed the same producer bundle. After rebasing, PR #58 adds only PHS 398 Research Plan and PHS Human Subjects and Clinical Trials.
- The complete bank contains 36 forms and 418 selected artifacts. Runtime-enabled forms remain 29 and registered forms remain 5. Runtime-identity SHA-256 remains `7e85abbd0796bf80396483e0eb9381b2159da94f0923b7b5e7967f6b559810cc`; registration SHA-256 remains `01b1d451dee808b1f6241ae63841d1bd90839b73cda701765b407f3ae98b7ff6`.
- Exact root XSDs and transitive artifact closure were vendored and verified for the two additions. No identity, registration, preview, compiler, adapter, renderer, or form-specific consumer branch was added.
- Local gates: producer preflight passed 109 TypeScript and 250 Python tests; consumer non-DB form-spec suite passed 233 tests before the final infrastructure rebase; focused integrity/provenance/registration/updater suite passed 29 tests after it; repository-native format, Ruff, and mypy gates passed.
- Infrastructure PR #59 merged as `c7a3a9e9da217131bc38a9b1bc7d57d3a273796d`. PR #58 was rebased over it and all three overlapping test-file edits were dropped. Its final delta is limited to portable artifacts and exact XSD fixtures; the local classifier reports `bankOnly=true`, two added forms, 36 selected forms, and 418 artifacts.
- Hosted lightweight CI passed at exact head `b0ab837dc1be0f1af89cd95a2439ddad0f2fa40c`: both classifiers and Portable Form Bank Checks succeeded; full API lint/tests, API build, Playwright cache, E2E infrastructure/tests, and report aggregation all skipped.
- Independent review verified the exact 418-artifact subset against the producer CI bundle, both official XSD byte digests, unchanged runtime and registration boundaries, and fail-closed loading for both new bank-only forms.
- Consumer PR #58 merged to public-fork main as `558570a048feec37cf3ec460f4ec17745435b1fa` on 2026-08-23. No HHS repository changed.

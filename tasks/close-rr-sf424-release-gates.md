---
type: Task
title: Close R&R SF-424 release gates
priority: P0
assignee: rr_sf424_browser
description: >-
  R&R SF-424 lifecycle, XML/XSD, and bounded real-browser compatibility evidence
  are delivered through generic portable and Simpler boundaries. Public-fork PR
  75 closes the automated rendered, edit/save/reload, accessibility-keyboard,
  and locked-print gates; human semantic, accessibility, policy, registration,
  and release approval remain explicit.
superbee_progress_status: in_progress
superbee_updated_by: codex_rr_sf424_evidence
generated:
  by: 'process:superbee'
  at: '2026-08-25T19:59:43.563Z'
---
# Scope

- Keep the portable producer authoritative and the Simpler integration generic.
- Add reusable lifecycle and wire conformance rather than form-specific runtime shortcuts.
- Preserve unresolved source conflicts and human approval gates explicitly.
- Work only in mikec-ai public repositories; do not modify HHS upstream.

## Completed

- Added the missing RRSF424 Simpler runtime type.
- Added a reusable lifecycle conformance helper that executes the production registry, validator, and rule processor.
- Proved JSON save/reload preservation, corrected-application and renewal requirements, and submit-time signature/date population.
- Added a target-neutral `Validation.notBefore` relationship and declared the R&R SF-424 project date ordering in the portable source.
- Added one generic Simpler `date_not_before` rule primitive and proved the real lifecycle rejects an end date earlier than its start date.
- Added a declarative Grants.gov XML profile covering all 28 top-level response fields, nested structures, and three attachments.
- Pinned the official RR_SF424 5.0 XSD by URL and SHA-256.
- Added generic wire-only output groups with absolute source pointers, keeping CongressionalDistrict out of the canonical question model.
- Fixed path-local scalar namespace handling generically after XSD execution exposed an element-name collision.
- Corrected form namespace selection and XSD sequence order in the declarative producer mapping.
- Proved a representative submit-populated response validates against the pinned official XSD.
- Merged producer PRs 28, 29, and 30 and adapter PRs 25 through 28 to main.
- Verification: producer preflight passes 69 TypeSpec and 49 Python tests; adapter lifecycle, rule, and XML tests pass. In the broader XML suite, 458 tests pass and 103 cannot initialize without the local grants-db service.
- Opened public-fork PR 75 with a generic nested conditional-required compiler and the bounded R&R SF-424 browser receipt. No form-specific adapter branch was added.
- Browser evidence pins producer `4e69e3fb25f8ee9554ee5e40ad84348ec99599dc` and consumer `a83d0ad933383a6b254003e4166408843ff22ca7`. Preview registration, API preflight, Apply render, edit/save/reload, automated accessibility and keyboard checks, and locked print all passed in Chrome. Save/reload preserved 89 controls; Axe reported zero detected WCAG 2 A/AA or 2.1 A/AA violations; keyboard focus reached `submission_type_code`; print exposed zero enabled interactive controls.
- Consumer verification: 47 focused conditional, ApplyForm, and matrix-contract tests; 100 related schema-processing tests; ESLint, Prettier, TypeScript, production build, and one bounded 31.2-second Chrome receipt all passed.
- Generated plans, traces, and receipts remain ignored build artifacts rather than repository content.

## Remaining

- Human review of the source-bound XML mapping and semantic/policy decisions. Current evidence remains source-bound-unreviewed and does not count as reviewed coverage.
- Manual visual review, human accessibility review, and final release acceptance.
- Runtime registration only after the relevant release gates are accepted.

## Architectural evidence

R&R SF-424 validated the intended boundary: canonical questions and cross-field relationships remain independent of Grants.gov wire wrappers, portable targets declare the wire contract, and the Simpler adapter compiles those declarations generically. Exact lifecycle, XSD, and browser execution caught reusable validation, namespace, grouping, ordering, and nested-requiredness gaps without introducing form-specific Python or frontend logic.

[depends on](author-integrate-rr-sf424.md)

## Active evidence-closure wave — 2026-08-25

- Claimed by `codex_rr_sf424_evidence` after collision-checking current open producer PRs; no open branch changes `evidence/forms/rr-sf424/evidence.json`, `tests/test_rr_sf424.py`, or the R&R SF-424 TypeSpec source.
- Scope is form-local evidence and regression coverage only: reconcile the eight already-emitted conditional targets to exact pinned official source records and package all 22 semantic identities for human review without accepting any mapping.
- No compiler, adapter, shared runtime, registration, release, or R&R Subaward Budget 10YR/30 changes are authorized in this lane. Any generic defect discovered during full validation will be reported before implementation.

### Technical closure receipt

- Merged producer PR [#117](https://github.com/mikec-ai/grants-form-spec/pull/117) at merge commit `6078fa35d8c0f1ae6dc040ed77536a2920534dd0`.
- Preserved the exact pinned F768 source URI and SHA-256, then reconciled all eight official source-bound behavior records separately from eight compiled-but-unresolved UI dispositions. No hidden/disabled or conditional-requiredness parity was inferred.
- Packaged all 22 semantic identities as proposals for human review; `semanticReview` remains `unreviewed`, with zero accepted mappings and no contribution to reviewed coverage.
- Focused local evidence: 12 tests passed / 1 skipped. Full producer preflight passed 125 TypeSpec tests, 395 Python tests / 10 skipped, 8 XML projection tests, 36 XSD fixtures, 1,721 artifact checks, and classified 0/0.
- Hosted receipts at exact head `167d5a227c5ff69b2ca74fe4331b3d307409ca78`: [form-spec CI run 32892431936](https://github.com/mikec-ai/grants-form-spec/actions/runs/32892431936) and [proof-package run 32892431932](https://github.com/mikec-ai/grants-form-spec/actions/runs/32892431932), both green.
- Independent review was clean on exact source text/path/provenance, the five-row revision-code aggregation, separation of unresolved compiled dispositions, 22 proposed/0 accepted semantics, and the strictly form-local two-file diff.
- Remaining gates are unchanged: human semantic and source-bound XML/policy review, manual visual and accessibility review, release acceptance, and runtime registration. This merge makes no production-readiness or release claim.

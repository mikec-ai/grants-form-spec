---
type: Task
title: Close R&R SF-424 Multi-Project Cover technical gates
description: >-
  Exact XML/XSD and bounded Simpler lifecycle/browser closure for the portable
  Multi-Project Cover.
superbee_updated_by: codex_mp_cover_evidence
generated:
  by: 'process:superbee'
  at: '2026-08-25T20:03:22.168Z'
superbee_progress_status: in_progress
assignee: codex_mp_cover_evidence
---
# Objective

Move the already-banked R&R SF-424 Multi-Project Cover from adapter canary to technical human-review handoff while preserving source-specific optionality and keeping human gates separate.

# Automated technical handoff receipts

- Producer PR [#106](https://github.com/mikec-ai/grants-form-spec/pull/106) merged as `762d67354d1cf2447c782a85c91ba4abb4c3253b` from reviewed head `4ccabcbb8539a747f0dee85c60da7bdb9016e362`. It pins the official 4.0 root XSD at SHA-256 `5d5599068d721e6554fa442df88711f8d9386a5fafc18b01cb1d1becc41f84e7`.
- The XML profile composes the existing R&R SF-424 mapping with a generic build-time `$rename`/`$overlay`; the only source-backed wire delta is `GGTrackingID` to `GrantsTrackingNumber`.
- The common projection now uses the existing declarative `container` mechanism for Congressional District, preventing a phantom empty wrapper when this all-optional form has no response.
- Exact-XSD tests prove an empty response, a representative lifecycle response, ordering, and the 13-character lower bound for the tracking number.
- Full producer preflight passed: 34/34 XSD fixtures, 320 blocks, 1,708 artifacts, 125 TypeScript tests, 367 Python tests, a verified 1,186-artifact bundle, and zero unclassified fields.
- Consumer PR [#112](https://github.com/mikec-ai/simpler-grants-gov/pull/112) merged as `beed3479f37158a3a5e3391d3bad59e0c5e83958` from final head `73bf5ce6608168f8ded3fe2aa8b4378f5a0d233b`. It vendors the exact XSD and profile and adds generic preview, validation, submission, and XML/XSD lifecycle proof. There are no form-specific compiler or adapter branches.
- On technical head `496d07979e09a80dbcb980a574028a60d73ec221`, 20 focused lifecycle, provenance, and integrity tests passed with Ruff, mypy, artifact integrity, and exact-XSD integrity green.
- Exact bounded browser run [#32826954842](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32826954842) completed successfully on that exact head with `PORTABLE_BROWSER_FORM_IDS=rr-sf424-multi-project-cover`: four checks passed and four nonselected checks were intentionally skipped. Evidence artifact `9555574508` was published at 89,434,917 bytes.
- A later full API run [#32850583118](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32850583118) on runtime head `d7254b232e1440c3f7fc7e1a63b8d788078693a9` passed 4,771 tests with two skipped. Its only failure was a stale Project Abstract provenance assertion that incorrectly equated a global bundle revision with that form's historical producer revision; it was not a Multi-Project Cover runtime failure.
- Final head `73bf5ce6608168f8ded3fe2aa8b4378f5a0d233b` repaired that cross-form receipt assertion. Fourteen focused Project Abstract plus Multi-Project lifecycle/provenance/integrity tests and the format, lint, migrations, security, artifact, and exact-XSD checks were green.
- Current-head bounded browser run [#32853841892](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32853841892) independently repeated the exact form-filtered result: four passed and four intentionally skipped. Evidence artifact `9565703668` was published at 111,665,073 bytes.

# Technical disposition

Automated technical handoff is complete: the producer and private-fork consumer are merged, exact XML/XSD and generic runtime lifecycle evidence are recorded, and the final consumer head has a green bounded browser receipt. This is a handoff for human review, not production readiness.

# Open human and release gates

- Human semantic review remains open; mappings remain proposed and are not accepted semantic equivalences.
- Human visual-design, content, usability, and source-fidelity review remains open.
- Accessibility review remains open, including manual inspection and assistive-technology testing; automated browser success is not accessibility approval.
- Privacy, policy, and program/content-authority review remains open.
- Human acceptance and user-acceptance iteration remain open.
- Production registration, operational approval, deployment, and release remain open. The form remains unregistered.

## Active form-local evidence closure — 2026-08-25

- Claimed by `codex_mp_cover_evidence` after checking the live board and all open producer/consumer PRs; no active owner or branch touches the Multi-Project Cover evidence or regression files.
- Reconcile the 14 emitted conditional targets against the exact pinned F769 DAT behavior records while preserving each compiled UI disposition separately. Do not infer semantic equivalence, hidden/disabled parity, inactive-value clearing, or conditional requiredness beyond exact source evidence.
- Package the existing 22 semantic identities for human review without accepting them. `semanticReview` must remain proposed with zero accepted mappings.
- Scope is strictly form-local producer evidence and regression coverage. No TypeSpec declaration, shared compiler, adapter, runtime, registration, release, or R&R Subaward Budget 10YR/30 change is authorized.

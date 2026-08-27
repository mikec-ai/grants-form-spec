---
type: Task
title: Prove expanded workbench cohort conformance
priority: P1
description: >-
  Add a data-driven conformance matrix for every package in the expanded
  workbench catalog. Acceptance: package load/digest/provenance, both presets,
  validation readiness, behavior execution where present, response isolation,
  and unsupported-capability reporting are tested without a per-form test
  branch. Keep accessibility, XML parity, policy, and human acceptance as
  separate explicit gates.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T13:30:16.390Z'
assignee: Codex
---
## Delivered

Merged [grants-form-workbench PR #18](https://github.com/mikec-ai/grants-form-workbench/pull/18) at merge commit `714fc5610264336d7cec6a617aeb478c595e8097`.

The conformance matrix is catalog-driven and contains no form-ID-specific branches. It proves for the 24-form checked-in cohort:

- 24 exact package load, SHA-256 digest, source-revision, contract-validation, and portable-behavior cases
- 48 renderer cases: every form through `generic/v1` and `simpler-compatible/v1`
- applicant-response isolation from calculated outputs
- calculation execution and receipts wherever behavior rules exist
- capability findings and exact artifact/source SHA-256 receipts across both profiles

## Verification receipts

- `GRANTS_FORM_SPEC_CHECKOUT=/private/tmp/grants-form-spec-root-expansion npm test`: 23 test files and 322 tests passed; agent-tools suite 10/10 passed
- `npm run build`: passed
- `git diff --check`: passed
- pinned producer revision: `77fcbe1d63fdb5d5e247f0a9e3bb3b7a1939b46d`
- implementation commit: `35f22406acb872d326fc42ad1c4de527c1650e1b`

GitHub Actions run `33077082826` failed before execution: the job contained zero steps and no log, so no repository check ran. The complete local gate above is the merge evidence.

## Explicitly separate gates

This result does not claim accessibility, XML round-trip fidelity, policy approval, or human acceptance. It does not promote semantic mappings or alter published coverage.

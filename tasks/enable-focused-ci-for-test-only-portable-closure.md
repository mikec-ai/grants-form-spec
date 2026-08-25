---
type: Task
title: Enable focused CI for test-only portable form closure
priority: P1
assignee: codex_ci_baseline_audit
description: >-
  Extend the fail-closed portable-form classifier so changes containing only
  exact CI-mapped form-local tests can use portable_focused CI without an
  accompanying artifact modification.
superbee_progress_status: in_progress
superbee_updated_by: codex_ci_baseline_audit
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:54:40.382Z'
---
# Problem

PR #125 changes only the exact CI-mapped test files for SF-LLL, CD-511, and Grants.gov Lobbying, but the classifier derives `form_ids` only from changed artifact paths. With no artifact delta, it returns `tier: full`, empty `portableFormIds`, and the reason `consumer or workflow changes require full CI` for the three mapped test files.

# Intended change

- When there are no artifact, XSD, manifest, registration, shared runtime, frontend, workflow, or other shared deltas, infer form IDs from an exact reverse lookup of changed test paths in `portable-form-ci-map.json`.
- Permit `portable_focused` only when every changed path is an exact mapped portable test and every mapping resolves unambiguously.
- Select the union of exact mapped tests and form IDs deterministically.
- Do not change additive-form admission or artifact-modification classification.

# Fail-closed boundaries

- Unknown test files require full CI.
- A mixture of mapped tests and any shared/consumer/workflow/registration file requires full CI.
- Ambiguous mappings, missing mappings, deletions, and unrelated files require full CI.
- Multiple forms are allowed only when every changed test maps exactly and no other delta exists.
- The classifier must not infer semantic equivalence or expand form scope from filenames.

# Acceptance criteria

- Unit regressions cover one mapped form, multiple mapped forms, unknown tests, ambiguous mappings, deletions, and mixed shared deltas.
- Existing full, bank-only, and artifact-backed portable-focused cases remain unchanged.
- The first real test-only closure PR receives a hosted `portable_focused` classification with exact selected form IDs/test files and a bounded browser receipt.
- Exact before/after classifier output and hosted run receipts are recorded here before closure.

# Initial receipt

- PR: https://github.com/mikec-ai/simpler-grants-gov/pull/125
- Head: `4c103920a9345876972f79d44ee2d04f6b738130`
- Changed paths: the three exact mapped form-local tests for `sflll`, `cd511`, and `gg-lobbying` only.
- Current result: `tier: full`, `portableFormIds: []`, `portableTestFiles: []`.

# Implementation and first hosted proof

- CI hardening PR: https://github.com/mikec-ai/simpler-grants-gov/pull/126
- Merged private-main commit: `bb8b7d5c6`
- Real test-only proof PR: https://github.com/mikec-ai/simpler-grants-gov/pull/125
- Proof head after rebase: `c22ec7ad508692cafb4c4975b723e1af3f898f2a`
- Hosted API run `32880826731` classified `portable_focused` with reason `only exact unambiguous CI-mapped portable tests changed`; exact `focusedForms` / `portableFormIds` were `cd511`, `gg-lobbying`, and `sflll`; exact `portableTestFiles` were their three form-local mapped suites; `changedArtifacts` was empty. Focused Portable Form Checks passed (job `97910331871`, 7m03s) while full API and bank jobs stayed skipped.
- Hosted E2E/browser run `32880827041` passed classification and executed the selected cohort as one bounded shard: job `97911386532` passed in 12m45s and merged report job `97915546008` passed in 38s.
- Proof PR #125 merged at `dbf71482c4d589e91027df7f6a240309171e44ec`; the first hosted test-only `portable_focused` proof is complete.

# Implementation receipt

- Implementation PR: https://github.com/mikec-ai/simpler-grants-gov/pull/126
- Implementation head: `1ea66a436`.
- Local classifier suite: 36 passed; isort and Ruff passed.
- The exact PR #125 diff through the updated classifier returns `tier: portable_focused`, `portableFormIds: [cd511, gg-lobbying, sflll]`, the exact three mapped portable tests, and `changedArtifacts: []`.
- Hosted PR #125 receipt is complete on rebased head `c22ec7ad508692cafb4c4975b723e1af3f898f2a` and merged commit `dbf71482c4d589e91027df7f6a240309171e44ec`.

[related to](close-lobbying-certification-cohort-technical-gates.md)

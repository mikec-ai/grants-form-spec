---
type: Task
title: Bank PHS 398 Cover Page Supplement in SGG
priority: P0
assignee: promote_new_forms
description: >-
  Prove the steady-state supervised artifact/XSD-only banking lane from an exact
  immutable producer revision.
superbee_progress_status: in_progress
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-24T03:48:20.631Z'
---
# Goal

Prove the steady-state cheap banking lane by promoting PHS 398 Cover Page Supplement from an exact immutable producer revision into the public SGG consumer bank.

# Fixed inputs

- Producer revision: `6b5717763d5769efd8b92a3cdbb61bc6935909fb`.
- Consumer baseline: public fork `mikec-ai/simpler-grants-gov` main at `dd2da405ac63b2221e1966b5f3192fd24744dcfe`.
- Portable form id: `phs398-cover-page-supplement`.

# Acceptance criteria

- Use the generic supervised additive updater and pin the exact producer bundle digest.
- Vendor and verify the complete transitive artifact closure and exact root XSD fixture.
- Keep runtime identity, registration, preview, adapter, compiler, and renderer unchanged.
- Require the local and hosted classifiers to select the lightweight bank-only lane.
- Run focused consumer integrity/provenance/updater checks and preserve fail-closed runtime boundaries.
- Open a draft PR only in `mikec-ai/simpler-grants-gov`; do not change HHS upstream and do not merge before independent review.

[depends on](author-integrate-phs398-cover-page-supplement.md)

# Promotion receipt, 2026-08-23

- Draft consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/60
- Consumer base: `dd2da405ac63b2221e1966b5f3192fd24744dcfe`; consumer head: `a40b3d18de57fa2b23476e51965bde37d57c0dd2`.
- Immutable producer revision: `6b5717763d5769efd8b92a3cdbb61bc6935909fb`; source bundle SHA-256: `0f2e62ee303de460e2110a6cb13c9001924afddbf8cf15858d7bc7ac52c340d3`.
- Exact root XSD SHA-256: `ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26`, matching the producer evidence pin and physical vendored bytes.
- Automated PR #61 already banked R&R Personal Data from this producer revision. PR #60 now adds only Cover Page Supplement, producing a 38-form/442-artifact bank that contains both forms. Runtime-enabled forms remain 29 and registered forms remain 5. Runtime-identity SHA-256 remains `7e85abbd0796bf80396483e0eb9381b2159da94f0923b7b5e7967f6b559810cc`; registration SHA-256 remains `01b1d451dee808b1f6241ae63841d1bd90839b73cda701765b407f3ae98b7ff6`.
- Final consumer diff contains only the portable artifact closure and exact XSD fixture. Local classifier reports `bankOnly=true`; focused integrity/provenance/registration/updater tests passed 29/29.
- Hosted lightweight CI passed again at exact rebased head `a40b3d18de57fa2b23476e51965bde37d57c0dd2`. Both classifiers succeeded, Portable Form Bank Checks passed in two seconds, and full API lint/tests, API build, Playwright cache, E2E infrastructure/tests, and report aggregation all skipped. The workflows completed in 25 and 28 seconds.
- PR #60 is mergeable and clean but remains draft/unmerged pending independent review.

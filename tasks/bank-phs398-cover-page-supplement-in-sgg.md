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
  at: '2026-08-24T03:15:49.088Z'
---
# Goal

Prove the steady-state cheap banking lane by promoting PHS 398 Cover Page Supplement from an exact immutable producer revision into the public SGG consumer bank.

# Fixed inputs

- Producer revision: `778e9b04cd01886593cbbafab1f34b8c8753c2a9`.
- Consumer baseline: public fork `mikec-ai/simpler-grants-gov` main at `558570a048feec37cf3ec460f4ec17745435b1fa`.
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
- Consumer base: `558570a048feec37cf3ec460f4ec17745435b1fa`; consumer head: `ec729a3c14670a3db2fd0c924deb0db2f9380be2`.
- Immutable producer revision: `778e9b04cd01886593cbbafab1f34b8c8753c2a9`; source bundle SHA-256: `d99df6298cd28f0ce8fe20449418b7772d2dff0f851b99d00e8d66d2d76c10f1`.
- Exact root XSD SHA-256: `ec538c9bb5fd233c36ac73ca567d31e60779ee3df2f3c7b456d9395b3ec2dc26`, matching the producer evidence pin and physical vendored bytes.
- The bank becomes 37 forms and 434 selected artifacts. Runtime-enabled forms remain 29 and registered forms remain 5. Runtime-identity SHA-256 remains `7e85abbd0796bf80396483e0eb9381b2159da94f0923b7b5e7967f6b559810cc`; registration SHA-256 remains `01b1d451dee808b1f6241ae63841d1bd90839b73cda701765b407f3ae98b7ff6`.
- Final consumer diff contains only the portable artifact closure and exact XSD fixture. Local classifier reports `bankOnly=true`; focused integrity/provenance/registration/updater tests passed 29/29.
- Hosted lightweight CI passed at exact head `ec729a3c14670a3db2fd0c924deb0db2f9380be2`. Both classifiers succeeded, Portable Form Bank Checks passed in three seconds, and full API lint/tests, API build, Playwright cache, E2E infrastructure/tests, and report aggregation all skipped. The two hosted workflows completed in 23 and 20 seconds respectively.
- PR #60 is mergeable and clean but remains draft/unmerged pending independent review.

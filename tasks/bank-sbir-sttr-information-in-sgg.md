---
type: Task
title: Bank SBIR/STTR Information in SGG
priority: P0
assignee: promote_new_forms
description: >-
  Promote the exact reviewed SBIR/STTR package through the additive
  artifact/XSD-only consumer lane.
superbee_progress_status: in_progress
superbee_updated_by: promote_new_forms
generated:
  by: 'process:superbee'
  at: '2026-08-24T04:53:29.967Z'
---
# Goal

Bank SBIR/STTR Information in the public SGG consumer from the exact reviewed producer merge through the supervised additive workflow.

# Fixed inputs

- Producer revision: `88aee1a3406c3f860bc50c9bcc92c6022b9dda3b`.
- Consumer baseline: `262d7d86be3d447ba6881c2fe283fb368321e667`.
- Portable form id: `sbir-sttr-information`.
- Producer main-push CI: https://github.com/mikec-ai/grants-form-spec/actions/runs/32690117311, passed in 2m1s and published the artifact bundle.

# Acceptance criteria

- Add only SBIR/STTR Information while preserving all 38 existing forms and their transitive closure.
- Pin and verify the exact producer bundle, exact root XSD, artifact digests, source provenance, and full 39-form selection.
- Leave runtime identities, registrations, preview, adapter, compiler, and renderer unchanged.
- Require local and hosted classifiers to select the lightweight bank-only lane; run focused integrity/provenance/registration/updater checks.
- Open a draft PR only in `mikec-ai/simpler-grants-gov`; do not change HHS upstream and do not merge before independent review.

[depends on](author-integrate-sbir-sttr-information.md)

# Promotion receipt, 2026-08-24

- Draft consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/64
- Consumer base: `262d7d86be3d447ba6881c2fe283fb368321e667`; consumer head: `276aeff173a2ce0b0907564734aad849cd01a55c`.
- Immutable producer revision: `88aee1a3406c3f860bc50c9bcc92c6022b9dda3b`; source bundle SHA-256: `2e29d798de882da67a027fa375314c32ff45215e1f7c274d0b693d75305d7470`.
- Exact root XSD SHA-256: `32ed46a450c1b77d9ef64ebf2a4086ab90b076aa2d3cdfedfab8c00324adcebf`, matching the producer evidence pin and physical vendored bytes.
- The bank becomes 39 forms and 475 selected artifacts while preserving all 38 prior forms. Runtime-enabled forms remain 29 and registered forms remain 5. Runtime-identity SHA-256 remains `7e85abbd0796bf80396483e0eb9381b2159da94f0923b7b5e7967f6b559810cc`; registration SHA-256 remains `01b1d451dee808b1f6241ae63841d1bd90839b73cda701765b407f3ae98b7ff6`.
- Producer main-push CI passed in 2m1s and published the exact bundle. Local consumer classifier reports `bankOnly=true`; focused integrity/provenance/registration/updater tests passed 29/29.
- Hosted lightweight CI is running. PR remains draft/unmerged pending independent review.

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
  at: '2026-08-24T04:30:42.309Z'
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

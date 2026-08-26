---
type: Usability Finding
title: SF-424 revision selections disappear during rerender
severity: major
category: conditional_behavior
affected_layer: shared_runtime
form_id: sf424
stable_field_path: /application_type/revision_code
reproduction: >-
  Choose Revision and select the first encoded revision checkbox on the pre-fix
  runtime.
evidence_ref: 'Private-fork PR #138; verified on b147f0acf and merged as 00d9f61c'
superbee_progress_status: resolved
superbee_updated_by: codex
---
On SF-424 Revision type, the first checkbox selection could be lost when the conditional form rerendered. This made a valid multi-choice revision code appear unreliable even though the schema contract listed the combination.

The finding is resolved on private-fork merge `00d9f61cd13032b4cdbae9089439c9cac5c5b290`.

[attributed to](../shared-defects/encoded-checkbox-state-races-conditional-rerender.md)

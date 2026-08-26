---
type: Usability Finding
title: R&R Budget values are unstable across nested personnel groups
severity: major
category: persistence
affected_layer: shared_runtime
form_id: rr-budget
stable_field_path: /budget_periods/*/(key_person|other_personnel)
reproduction: >-
  On the pre-fix runtime, enter values in nested personnel groups that share
  requested_salary leaf names and save.
evidence_ref: 'Private-fork PR #138; verified on b147f0acf and merged as 00d9f61c'
superbee_progress_status: resolved
superbee_updated_by: codex
---
Entering requested salary and fringe values in R&R Budget produced duplicate React-key warnings and the values/calculated total did not survive the interaction reliably.

The finding is resolved on private-fork merge `00d9f61cd13032b4cdbae9089439c9cac5c5b290`.

[attributed to](../shared-defects/nested-fieldlist-leaf-key-collisions.md)

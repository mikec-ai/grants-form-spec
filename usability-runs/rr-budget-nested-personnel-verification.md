---
type: Form Usability Run
title: R&R Budget — nested personnel persistence verification
form_id: rr-budget
scenario: nested-personnel-persistence-and-calculation/v1
environment: 'local signed-in Simpler preview at localhost:3000'
runtime_commit: b147f0acf23bd1de9c7bd3853a31067ce2d1baef
assignee: codex
producer_commit: 7c3be8e32968b49b5ce48f53a832c00220eb5bee
artifact_manifest_digest: 47de7baccab8ed6c7cbb1fd3eb89812b8e3968bcee4ff6b5a24ebe4dfea1d694
browser_scope: Desktop Chromium via Codex in-app browser
result: pass
superbee_progress_status: complete
superbee_updated_by: codex
---
# Intent

Verify nested personnel persistence and the existing server calculation after repairing generic FieldList identity.

# Preconditions and provenance

- Exact tested head: `b147f0acf23bd1de9c7bd3853a31067ce2d1baef`; merged consumer commit: `00d9f61cd13032b4cdbae9089439c9cac5c5b290`.
- Selected producer revision: `7c3be8e32968b49b5ce48f53a832c00220eb5bee`.
- Form manifest SHA-256: `47de7baccab8ed6c7cbb1fd3eb89812b8e3968bcee4ff6b5a24ebe4dfea1d694`.
- Local signed-in desktop Chromium preview.

# Scenario steps

1. Enter requested salary `12000` for the first key person.
2. Enter fringe benefits `1000`.
3. Save and navigate to the same form again.
4. Verify both inputs and calculated Funds Requested.

# Evidence

- Duplicate React-key warnings after the fix: zero.
- Salary `12000` and fringe `1000` persisted through save/reload.
- Protected Funds Requested displayed `13000.00` after server calculation.
- The dedicated FieldList regression suite passed 26 tests; the combined focused form/widget suite passed 30 tests.

# Outcome and follow-up

Pass. The shared identity repair is merged and verified; future nested FieldLists with repeated leaf names inherit the fix.

[discovers](../usability-findings/rr-budget-values-unstable-across-nested-groups.md)

[verifies](../shared-defects/nested-fieldlist-leaf-key-collisions.md)

[validates](../tasks/scope-nested-fieldlist-child-identity.md)

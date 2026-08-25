---
type: Task
title: Fix portable browser-plan read-only ancestry
priority: P1
assignee: codex_nifa_closure
superbee_progress_status: in_progress
superbee_updated_by: codex_nifa_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T16:49:36.048Z'
---
The capability-driven browser plan currently inspects only the leaf schema node addressed by a UI definition. A descendant field under a `readOnly: true` parent object can therefore be advertised as editable, causing the bounded save/reload harness to mutate protected pre-populated data.

Evidence: exact-head NIFA bounded run `32872824432` selected `/properties/funding_opportunity/properties/title` for its deterministic edit even though `/properties/funding_opportunity` is read-only. The server correctly restored the authoritative prefill after reload.

Acceptance criteria:

- Generic browser-plan discovery propagates read-only protection through object ancestry without mutating source schemas.
- A nested synthetic regression proves descendants of a read-only parent are protected and not editable.
- A NIFA regression proves `funding_opportunity.title` is never selected for deterministic editing.
- Existing direct-leaf read-only and editable-field behavior remains covered.
- No form-specific compiler, adapter, or browser-harness branch is introduced.

Boundaries:

- Do not modify attachment behavior or the isolated WebKit print failure in this task.
- This closes only automated browser-plan correctness; it makes no semantic, accessibility, policy, agency, UAT, registration, release, or production-readiness claim.

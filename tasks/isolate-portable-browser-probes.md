---
type: Task
title: Isolate stateful portable browser probes
priority: P1
assignee: codex_nifa_closure
description: >-
  Prevent a failed stateful browser probe from contaminating or falsely clearing
  independent portable-form receipts.
superbee_progress_status: done
superbee_updated_by: codex_nifa_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:38:30.624Z'
---
The portable catalog browser harness runs attachment upload before its independent save/reload receipt. A failed or inconclusive stateful probe can leave unsaved page state and probe-local request/page-error entries behind, causing unrelated later receipts to fail or be falsely cleared.

Evidence: NIFA exact-head run `32875020792` uploaded the attachment, timed out waiting for the attachment save confirmation, then submitted `program--program_code_name=Browser canary` from the same contaminated page. The request contained the edit, while the later reload was blank. Focused frontend shaping and API validation preserve the program value outside that stateful sequence.

Acceptance criteria:

- A failed or inconclusive stateful probe retains its original receipt.
- Only request failures and page errors observed during that probe are attributed to and removed with its isolation boundary.
- Pre-existing or unrelated ledger entries remain visible and continue to fail later probes.
- Independent save/reload evidence re-enters the persisted form before editing.
- Passed and not-applicable probes do not trigger unnecessary isolation.
- Generic regression coverage proves the ownership boundary; no NIFA- or attachment-specific runtime branch is added.

Implementation: private-fork PR #121, commit `0621722700cf354f241cedba19b8118a684df044`. The unresolved attachment timeout and WebKit `Load failed` remain separate shared gates.

## Closure receipt

Merged private-fork PR #121 as `cfb57f79915b50980f9d11f880dbf87dac78e7ef`. Exact-head bounded run `32877753834` retains `attachment_upload_reload=inconclusive` with timeout/harness ownership in all four browsers, records the attachment probe's own empty failed-request and page-error deltas, and then passes independent save/reload, accessibility, and print in all four browsers. The attachment timeout remains unresolved and was not reclassified.

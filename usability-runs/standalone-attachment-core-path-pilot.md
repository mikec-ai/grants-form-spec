---
type: Form Usability Run
title: Attachment Form — standalone consumer core-path pilot
form_id: attachment-form
scenario: ordered-attachment-clarity-and-state-v1
environment: 'local grants-form-workbench consumer at 127.0.0.1:5173'
runtime_commit: b38afad6e33fe1afd1afa67a048a0137e77768b1
assignee: Codex
producer_commit: 77fcbe1d63fdb5d5e247f0a9e3bb3b7a1939b46d
artifact_manifest_digest: 17861ef970eb80b84ec9aa079eeb03b588dbd2d75aceb2fafdbdb56f8db5e5b7
browser_scope: Desktop Chromium via Codex in-app browser
superbee_progress_status: complete
superbee_updated_by: Codex
result: fail
---
# Intent

Exercise the ordered attachment path as an applicant would before human acceptance review: select a real PDF, inspect the response, switch consumer presentation, remove the file, and verify that visible state and response state agree.

# Preconditions and provenance

- Runtime: grants-form-workbench commit b38afad6e33fe1afd1afa67a048a0137e77768b1 plus the uncommitted codex/agent-usability-gate fix under review.
- Producer: grants-form-spec commit 77fcbe1d63fdb5d5e247f0a9e3bb3b7a1939b46d.
- Selected package digest: 17861ef970eb80b84ec9aa079eeb03b588dbd2d75aceb2fafdbdb56f8db5e5b7.
- The package contains 15 unreviewed occurrences and no behavior artifact; this run does not upgrade semantic review.

# Scenario steps

1. Load Attachment Form 1.2 in the standalone consumer.
2. Select an actual PDF for Attachment 1.
3. Confirm that response JSON contains only the generated UUID reference.
4. Switch from the Simpler-compatible presentation to Generic JSON Forms and confirm the response is unchanged.
5. Remove Attachment 1 in the generic presentation and compare the announcement, visible selection, registry state, and response JSON.
6. Repeat the shared-control test after the fix under both presentations.

# Evidence

- Selection produced a UUID-only response; local filename and bytes remained outside response data.
- Presentation switching preserved the exact response.
- Before the fix, Generic JSON Forms announced removal while the UUID remained in response data. Simpler-compatible removal committed correctly.
- The existing shared attachment-array test reproduced a delayed or lost removal under the full suite, while focused runs passed. That timing sensitivity supports treating this as a shared runtime/harness race rather than a form-specific defect.
- The standalone consumer Save draft control has no persistence handler, so persistence, reload, and backend lifecycle claims remain outside this run and belong in the SGG integration gate.

# Outcome and follow-up

Fail for the cross-presentation removal scenario, while selection, UUID-only response data, and presentation preservation pass. The finding is triaged to the shared runtime/harness boundary and remains open. This is exactly why the agent gate precedes human review: the form should not be handed off as interaction-complete until a shared fix is implemented and verified in a later browser run.

[validates](../tasks/integrate-pre-human-agent-usability-gate.md)

[discovers](../usability-findings/generic-attachment-removal-not-committed.md)

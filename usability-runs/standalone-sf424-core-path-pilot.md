---
type: Form Usability Run
title: SF-424 — standalone consumer core-path pilot
form_id: sf424
scenario: core-applicant-behavior-and-clarity-v1
environment: 'local grants-form-workbench consumer at 127.0.0.1:5173'
runtime_commit: b38afad6e33fe1afd1afa67a048a0137e77768b1
assignee: Codex
producer_commit: 77fcbe1d63fdb5d5e247f0a9e3bb3b7a1939b46d
artifact_manifest_digest: 2a2aec94910ea74870cebba34c2667c0e62dd21ce6452099f795dcd1c1e6b245
browser_scope: Desktop Chromium via Codex in-app browser
superbee_progress_status: complete
superbee_updated_by: Codex
result: fail
---
# Intent

Determine whether the standalone consumer can support an applicant-oriented SF-424 usability pass before human acceptance review, including conditional-field behavior and clarity.

# Preconditions and provenance

- Runtime: grants-form-workbench commit b38afad6e33fe1afd1afa67a048a0137e77768b1.
- Producer: grants-form-spec commit 77fcbe1d63fdb5d5e247f0a9e3bb3b7a1939b46d.
- Selected package digest: 2a2aec94910ea74870cebba34c2667c0e62dd21ce6452099f795dcd1c1e6b245.
- The package contains 48 occurrences: 6 proposed and 42 unreviewed. This run does not convert any mapping into reviewed coverage.

# Scenario steps

1. Load SF-424 4.0 in the standalone consumer.
2. Inspect initial validation, system-owned fields, and conditional fields.
3. Attempt the revision and other-explanation paths that should change visibility or requiredness.
4. Inspect the package receipt and executable behavior availability before making a readiness claim.

# Evidence

- The form loads through the generic catalog and reports 32 initial validation issues.
- System-owned values render disabled.
- Revision Type and Other Explanation are visible before their triggering answers.
- The selected portable package supplies no behavior artifact, so the consumer cannot execute or receipt those conditional outcomes.
- A later import spike on R&R SF-424 found eight official visibility conditions, but the current adapter only projects enabled/disabled outcomes and fails closed on visible/hidden semantics.

# Outcome and follow-up

Fail for the named behavior-and-clarity scenario, while basic rendering passes. This is a useful pre-human gate result: SF-424 should not be described as behavior-complete in the standalone consumer. Project source-backed visibility bindings generically, preserve their evidence receipts, then rerun this scenario before human acceptance review.

[validates](../tasks/integrate-pre-human-agent-usability-gate.md)

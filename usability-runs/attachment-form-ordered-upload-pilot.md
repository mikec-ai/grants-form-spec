---
type: Form Usability Run
title: Attachment Form — ordered upload pilot
form_id: attachment-form
scenario: ordered-upload-recovery-v1
environment: local-simpler-private-fork
runtime_commit: 5ef1589b971cb685780f902b782c3cf6ef65e953
producer_commit: 273d1ba8da96a958448d9c19209a50b8cbe2c0dc
artifact_manifest_digest: 17861ef970eb80b84ec9aa079eeb03b588dbd2d75aceb2fafdbdb56f8db5e5b7
browser_scope: desktop-chromium-calibration
result: not_run
superbee_progress_status: queued
superbee_updated_by: codex
---
# Intent

Establish the low-complexity baseline for the manual agent-usability protocol using Attachment
Form. The applicant goal is to understand the ordering instructions, attach two representative
PDFs in the intended sequence, replace or remove one attachment, save/reload, recover from one
intentional invalid upload, and inspect the printable result.

# Preconditions and provenance

- Status at creation: queued and not run.
- Portable form id: `attachment-form`, Grants.gov legacy form id 540, version 1.2.
- Producer repository commit: `273d1ba8da96a958448d9c19209a50b8cbe2c0dc`.
- Producer form-manifest SHA-256: `17861ef970eb80b84ec9aa079eeb03b588dbd2d75aceb2fafdbdb56f8db5e5b7`.
- Consumer private-fork commit at creation: `5ef1589b971cb685780f902b782c3cf6ef65e953`.
- The form has 15 ordered attachment slots and no semantic guarantee about what each unnamed slot
  represents. The run evaluates whether the supplied instructions and interaction are usable; it
  must not invent agency-specific attachment meaning.
- Prior automated catalog evidence is context only and is not a manual usability result.

# Scenario steps

1. Open the ordinary local Simpler application-form route and explain, using only the displayed
   content, what the applicant is expected to attach and how ordering works.
2. Upload two small valid PDF fixtures to Attachment 1 and Attachment 2.
3. Attempt one invalid file upload and record the clarity, placement, and recovery path of the
   resulting feedback.
4. Replace or remove one valid attachment and confirm the UI communicates the resulting order.
5. Save, reload, and verify filenames and ordering remain understandable and stable.
6. Traverse the exercised controls by keyboard and inspect the printable representation.
7. Record applicant-facing symptoms as findings without diagnosing a shared root cause during the
   run.

# Evidence

Not run. The executing agent must add browser/viewport, local application identifier, safe route
reference, fixture names and hashes, timestamps, screenshots or trace locations, and step-level
observations here.

# Outcome and follow-up

Not run. Set the result and terminal status only after the evidence above is complete. Distinguish
product usability from missing agency-specific guidance and from browser/harness failures.

[validates](../tasks/close-attachment-form-release-gates.md)

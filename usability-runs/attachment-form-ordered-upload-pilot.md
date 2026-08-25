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
superbee_progress_status: inconclusive
superbee_updated_by: codex_attachment_usability
assignee: codex_attachment_usability
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

- Attempt timestamp: `2026-08-25T21:54:05Z`.
- Requested browser scope: desktop Chromium calibration through the ordinary local Simpler route.
- Browser connection evidence: the in-app browser selector returned exact diagnostic
  `Browser is not available: iab`; the URL-based selector for `http://localhost:3000/` then returned
  exact diagnostic `No browser is available`.
- Local application identifier and safe route reference: not observable because no supported
  browser surface was available. The requested root URL was `http://localhost:3000/`; no form or
  application route was opened.
- Runtime and producer provenance remain the pinned values above. They were not substituted with a
  different local checkout or newer build.
- Fixtures: none created or uploaded. Consequently there are no fixture hashes, screenshots, or
  browser traces for this attempt.
- Step 1: not executed; displayed ordering content could not be observed.
- Step 2: not executed; no valid files were uploaded.
- Step 3: not executed; no invalid-file feedback was elicited.
- Step 4: not executed; no attachment was replaced or removed.
- Step 5: not executed; persistence and ordering were not evaluated.
- Step 6: not executed; keyboard traversal and print representation were not evaluated.
- Step 7: no applicant-facing symptom was observed, so no Usability Finding was created.
- Prior automated catalog evidence was not used as a substitute for this manual calibration.

# Outcome and follow-up

Inconclusive due solely to unavailable browser infrastructure. This attempt provides no evidence
for or against Attachment Form usability, ordering clarity, validation, persistence, keyboard
operation, or print behavior. Keep `result: not_run`; terminal lifecycle is
`progress_status: inconclusive`. Requeue a new run against the same pinned build when a supported
desktop Chromium browser is available. No product code, issue, finding, or root-cause record was
created.

[validates](../tasks/close-attachment-form-release-gates.md)

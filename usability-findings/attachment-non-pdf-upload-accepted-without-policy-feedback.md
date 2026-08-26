---
type: Usability Finding
title: >-
  Attachment Form accepts a non-PDF upload without visible format-policy
  feedback
superbee_progress_status: triaged
severity: moderate
category: validation
affected_layer: source_or_policy
form_id: attachment-form
stable_field_path: /properties/attachment3
reproduction: >-
  Upload a synthetic text/plain file to Attachment 3 through the ordinary local
  Simpler application route and wait for the security scan to complete.
evidence_ref: local application 378723db-e895-4160-a977-03262926bd46 attachment slot 3
superbee_updated_by: codex
---
# Observation

`invalid-upload.txt` completed upload and security scanning and was shown as a saved attachment.
The UI displayed no format-policy warning or explanation distinguishing security scanning from
document-format validation.

# Reproduction

1. Open the Attachment Form through the ordinary application workflow.
2. Upload a `text/plain` fixture to Attachment 3.
3. Wait for the security scan to complete.
4. Observe that the file is displayed as saved with no inline format-policy feedback.

# Evidence boundary

The form instructions require applicants to follow the appropriate agency guidelines for file
format and naming, but this portable-preview opportunity exposes no agency guideline artifact.
Therefore this finding does not claim that PDF is the universally required format or that the
backend security scanner is defective. It records only the absence of visible format-policy
feedback for a non-PDF upload.

# Triage

Do not add a universal PDF restriction. Resolution requires an opportunity- or agency-scoped file
policy artifact that the generic attachment control can display and enforce. Until that source is
available, the current instructions are the semantic boundary and this remains an open policy
decision rather than a runtime defect.

[observed-in](../usability-runs/attachment-form-ordered-upload-primary-pilot.md)

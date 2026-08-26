---
type: Usability Finding
title: Attachment Form print route renders blank after successful saved uploads
superbee_progress_status: observed
severity: major
category: print
affected_layer: shared_runtime
form_id: attachment-form
stable_field_path: /
reproduction: >-
  Save attachments in the ordinary application route, reload to verify
  persistence, then open the ordinary print route for the same application form.
evidence_ref: >-
  local application 378723db-e895-4160-a977-03262926bd46 print route and
  frontend log
superbee_updated_by: codex
---
# Observation

After two PDFs and one text file were saved and survived a full form reload, the ordinary print
route rendered a completely blank page. The local frontend recorded
`TypeError: Cannot read properties of undefined (reading 'call')` with an HTTP 500, followed by a
failed client hydration path involving a missing `NextIntlClientProvider` context and nested
`html`/`body` elements.

# Reproduction

1. Save at least one attachment in the Attachment Form.
2. Reload the ordinary form route and verify that the filename persists.
3. Open `/print/application/{applicationId}/form/{applicationFormId}`.
4. Observe a blank print page and the server-side frontend exception.

# Evidence boundary

The PHS Human Subjects pilot loaded the same ordinary print route successfully in this environment,
so this is not classified as a blanket print-environment outage. Root cause remains unproven; the
finding is scoped to the Attachment Form/runtime interaction until implementation analysis
identifies the shared defect.

[observed-in](../usability-runs/attachment-form-ordered-upload-primary-pilot.md)

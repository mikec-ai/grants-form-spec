---
type: Usability Finding
title: Local Attachment Form print diagnostic caused by missing session keys
superbee_progress_status: dismissed
severity: minor
category: print
affected_layer: harness
form_id: attachment-form
stable_field_path: /
reproduction: >-
  Restart the local frontend without SESSION_SECRET and API_JWT_PUBLIC_KEY,
  then open the ordinary print route with the resulting unusable session cookie.
evidence_ref: >-
  local application 378723db-e895-4160-a977-03262926bd46 print route and
  frontend log
superbee_updated_by: codex
---
# Observation

After two PDFs and one text file were saved and survived a full form reload, an initial local print
attempt rendered blank. A clean diagnostic render then reported `UnauthorizedError` and the
frontend log showed that the restarted server had neither `SESSION_SECRET` nor
`API_JWT_PUBLIC_KEY`, so it could not decrypt the existing session or create a new one.

# Reproduction

1. Start the local frontend without its documented session keys.
2. Open `/print/application/{applicationId}/form/{applicationFormId}` using an existing session.
3. Observe `UnauthorizedError` because the local server cannot decrypt the session.
4. Restore the documented keys, restart, and observe the same print route render successfully.

# Evidence boundary

The authenticated re-test against the same persisted application rendered all 15 slots and all
three saved filenames. Hosted run `32788458690` also passed Attachment Form print in Chrome,
Firefox, WebKit, and mobile Chrome. This observation is dismissed as local harness/session state;
it is not an applicant-facing Attachment Form or shared-runtime defect.

[observed-in](../usability-runs/attachment-form-ordered-upload-primary-pilot.md)

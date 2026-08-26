---
type: Usability Finding
title: PHS enrollment coordinates lose visible grid context
severity: major
category: accessibility
affected_layer: form_spec
form_id: phs-inclusion-enrollment-report
stable_field_path: /reports/*/(planned|cumulativeActual)
reproduction: >-
  Open report 1 and move through the 115 numeric demographic coordinates; fields
  render sequentially without visible row/column headers.
evidence_ref: >-
  Local signed-in Chromium run on consumer b147f0acf; manifest
  sha256:a072b156d6cb701f9a65ee03d79ab36dac5580328005cf38ee599d9728616664
superbee_progress_status: triaged
superbee_updated_by: codex
---
In the first report entry, the planned and cumulative enrollment coordinates render as a long vertical sequence of 115 numeric controls. Accessible names contain coordinate words, but there are no visible matrix row/column headers or compact grid relationship. An applicant must reconstruct ethnicity, sex, and race context field by field.

Persistence and repetition are not broken: values `2` and `3` persisted after save/reload, a second report expanded the form from 115 to 230 numeric controls, and deleting it returned the form to 115.

[attributed to](../shared-defects/portable-matrix-presentation-contract-missing.md)

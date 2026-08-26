---
type: Form Usability Run
title: Attachment Form — primary ordered-upload pilot
superbee_progress_status: complete
form_id: attachment-form
scenario: ordered-upload-recovery-v1
environment: local-simpler-private-fork
runtime_commit: e34c1478593c8e09925643dc354b50cf80837932
assignee: codex-primary-usability
producer_commit: 273d1ba8da96a958448d9c19209a50b8cbe2c0dc
artifact_manifest_digest: 17861ef970eb80b84ec9aa079eeb03b588dbd2d75aceb2fafdbdb56f8db5e5b7
browser_scope: desktop-chromium-calibration
result: fail
superbee_updated_by: codex
---
# Intent

Run the first primary-agent Attachment Form calibration through Simpler's ordinary local
application workflow. Determine whether an applicant can understand the 15-slot ordering model,
upload two synthetic PDFs, recover from one invalid upload, replace or remove a file, save/reload,
and review the print representation without inventing semantic meaning for unnamed slots.

# Preconditions and provenance

- Portable form id `attachment-form`, legacy Grants.gov form id 540, version 1.2.
- Producer commit `273d1ba8da96a958448d9c19209a50b8cbe2c0dc`.
- Producer form-manifest SHA-256 `17861ef970eb80b84ec9aa079eeb03b588dbd2d75aceb2fafdbdb56f8db5e5b7`.
- Consumer private-fork commit `e34c1478593c8e09925643dc354b50cf80837932`.
- Synthetic fixture hashes will be recorded in Evidence; fixtures contain no personal, policy, or
  production data.
- The earlier delegated run was inconclusive because it could not access the desktop browser. It
  is not evidence for or against the form.

# Scenario steps

1. Open the ordinary local Simpler application route and interpret only the displayed ordering instructions.
2. Upload two valid synthetic PDF fixtures to the first two slots.
3. Attempt a synthetic invalid text upload and observe feedback and recovery.
4. Replace or remove one valid attachment and inspect how the resulting order is communicated.
5. Save, reload, and verify filenames and ordering.
6. Exercise the upload controls by keyboard where supported and inspect the ordinary print route.
7. Record symptoms as findings; do not infer a shared defect without corroboration.

# Evidence

- Ordinary local Simpler application route:
  `/workspace/applications/378723db-e895-4160-a977-03262926bd46/form/ef5c9b34-7b4f-411d-9795-162ea9e1bf04`.
- `attachment-01.pdf` SHA-256
  `8dd84aca0369730fc94dcfaf9b176d1a33fddc6715a82c116a531072e25f9ee8` uploaded to slot 1.
- `attachment-02.pdf` SHA-256
  `d6f9b754a64405cea7af6685a4bb255be6b906413f4e13fdd3f3af8b0420f38a` uploaded to slot 2.
- `invalid-upload.txt` SHA-256
  `1adfdd9a6c1b372104e6d28a9d428ff5e383d024f8910beb79872ade57f50238` uploaded to slot 3.
- Both PDFs completed upload and security scanning and displayed their filename, size, and saved date.
- The text file also completed upload and scanning without visible format-policy feedback.
- `Save and refresh` succeeded. A full reload preserved all three filenames in their original slots.
- The ordinary print route
  `/print/application/378723db-e895-4160-a977-03262926bd46/form/ef5c9b34-7b4f-411d-9795-162ea9e1bf04`
  rendered a blank page. The local frontend recorded `TypeError: Cannot read properties of
  undefined (reading 'call')` and an HTTP 500 before a broken hydration fallback.
- The upload scanner initially exposed a local harness defect: the API scanner and S3 mock had
  diverged storage mounts plus stale synthetic scan metadata. The canonical shared
  `s3mock-data` volume was restored and the exact synthetic scan bucket was backed up and cleared
  before the successful run. Those setup failures are excluded from the product findings.
- Replace/remove was not exercised because the saved-file UI exposes only `Delete`, which requires
  separate action-time confirmation. Keyboard upload was not used to alter additional form data.

# Outcome and follow-up

The core ordered-upload and persistence path works for multiple attachments, but the pilot fails
the release gate because the ordinary print representation does not render. A second bounded
finding records that a non-PDF upload receives no visible format-policy feedback; because this
preview opportunity has no agency guideline artifact, the evidence does not establish what exact
format should have been required.

[observed](../usability-findings/attachment-non-pdf-upload-accepted-without-policy-feedback.md)
[observed](../usability-findings/attachment-print-route-renders-blank.md)

[validates](../tasks/close-attachment-form-release-gates.md)

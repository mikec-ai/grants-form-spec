---
type: Form Usability Run
title: PHS Human Subjects — first reusable-fix verification
form_id: phs-human-subjects
scenario: first-reusable-fix-verification-v1
environment: local-simpler-private-fork
runtime_commit: 5c90a799336df79990528da455c1ce5a0a43be6b
producer_commit: 92aad605ea9a8e6709bd6562ce9ed000a9512fb0
artifact_manifest_digest: 968f51dd9cdcfb6ad1c66a5b2d97f361642d02c04ad4d8b0598ec8382196ae59
browser_scope: desktop-chromium-primary-agent
result: pass_with_findings
superbee_progress_status: complete
assignee: codex-primary-usability
---
# Intent

Re-run the exact failed overview-label, repeatable-group label, and top-level study-condition
scenarios after promoting the reusable producer fix into a real Simpler consumer build. Preserve the
known deeper study and print gaps rather than treating this bounded verification as whole-form
acceptance.

# Preconditions and provenance

- Executed August 25, 2026 in the Codex in-app Chromium browser against the ordinary local Simpler
  application route.
- Consumer private-fork branch commit: `5c90a799336df79990528da455c1ce5a0a43be6b`.
- Producer merge commit: `92aad605ea9a8e6709bd6562ce9ed000a9512fb0`.
- Selected artifact-manifest SHA-256:
  `968f51dd9cdcfb6ad1c66a5b2d97f361642d02c04ad4d8b0598ec8382196ae59`.
- Producer PR #119 and both hosted checks were green. Consumer PR #137 contains the promoted
  artifacts and exact consumer assertions.
- The local API, authentication, database, preview registration, and frontend were healthy before
  the scenario began.

# Scenario steps

1. Open the existing PHS Human Subjects application form through the ordinary application route.
2. Inspect visible and accessible names for all four overview controls.
3. Inspect one existing Human Subject Study and Inclusion Enrollment Report entry.
4. Confirm the study and delayed-onset collections are disabled while the controlling
   `HumanSubjectsIndicator` answer is not Yes.
5. Enter the exact source wire value `Y: Yes` and verify that both repeatable groups enable.
6. Record remaining visible behavior separately; do not infer the nine uncompiled F705 conditions
   or an embedded-study print policy.

# Evidence

- The form loaded with the expected portable-preview title and three-section navigation.
- All four overview controls had explicit visible and accessible question names, including
  “Does the proposed project involve human subjects?” and “Does any proposed research involve
  human specimens and/or data?”.
- Existing entries rendered as “Human Subject Study 1” and “Inclusion Enrollment Report 1”; the
  prior internal headings `studies 1` and `inclusionEnrollmentReports 1` were absent.
- Study controls and the delayed-onset add control were disabled before the controlling answer was
  Yes.
- After the exact value became `Y: Yes`, the existing Study Title control and delayed-onset add
  control were both enabled immediately.
- Consumer regression suite: 23 targeted adapter/XML tests passed; Ruff passed.
- Producer preflight: 126 TypeScript tests and 399 Python tests passed, plus artifact, XML, evidence,
  packaging, and field-classification gates.

# Outcome and follow-up

Result: **pass with findings** for this bounded reusable-fix verification. The overview-label and
repeater-label symptoms are resolved in the tested consumer build. The two exact top-level F705
conditions execute through the generic repeatable-group mechanism.

This is not whole-form acceptance. Nine F705 conditions, embedded-study conditional behavior, the
unresolved enrollment totals, deep print suppression, semantic review, accessibility review,
policy review, registration, and release remain open. The Attachment Form file-type finding also
remains a source/policy decision; this run provides no basis for a universal PDF restriction.

[validates](../tasks/close-phs-human-subjects-technical-gates.md)

[discovers](../usability-findings/phs-overview-required-controls-unlabelled.md)

[discovers](../usability-findings/phs-repeaters-display-internal-identifiers.md)

[discovers](../usability-findings/phs-study-schema-disclosed-without-conditions.md)

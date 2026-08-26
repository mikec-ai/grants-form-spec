---
type: Usability Finding
title: PHS repeaters display internal collection identifiers
superbee_progress_status: observed
severity: moderate
category: content
affected_layer: form_spec
form_id: phs-human-subjects
stable_field_path: >-
  /properties/studies/items/properties/populationCharacteristics/properties/inclusionEnrollmentReports
reproduction: Add one study and one inclusion enrollment report.
evidence_ref: local application 97b7c1b5-7a6b-4bbc-997d-413d6d5eb296
superbee_updated_by: codex
---
# Observation

Repeatable groups display internal collection identifiers as applicant-facing headings, including
`studies` and `inclusionEnrollmentReports`. Numbered entries inherit the same internal names.

# Reproduction

1. Add a Human Subject Study record.
2. Add an inclusion enrollment report within that study.
3. Observe the headings `studies 1` and `inclusionEnrollmentReports 1`.

# Evidence boundary

This is an applicant-facing content symptom. Similar internal headings in another form would require
separate evidence before treating it as a shared defect.

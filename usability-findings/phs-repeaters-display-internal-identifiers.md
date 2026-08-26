---
type: Usability Finding
title: PHS repeaters display internal collection identifiers
superbee_progress_status: resolved
severity: moderate
category: content
affected_layer: form_spec
form_id: phs-human-subjects
stable_field_path: >-
  /properties/studies/items/properties/populationCharacteristics/properties/inclusionEnrollmentReports
reproduction: Add one study and one inclusion enrollment report.
evidence_ref: usability-runs/phs-human-subjects-first-fix-verification
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

# Resolution

Producer PR [#119](https://github.com/mikec-ai/grants-form-spec/pull/119) gives the reusable study,
delayed-onset study, and inclusion-enrollment item models explicit entry labels. Consumer PR
[#137](https://github.com/mikec-ai/simpler-grants-gov/pull/137) promotes the exact merged producer
revision. The primary-agent browser re-run verified “Human Subject Study 1” and “Inclusion
Enrollment Report 1” in place of the two internal identifiers named by this finding.

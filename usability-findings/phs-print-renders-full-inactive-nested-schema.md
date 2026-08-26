---
type: Usability Finding
title: PHS print view renders the full inactive nested schema
superbee_progress_status: triaged
severity: major
category: print
affected_layer: unknown
form_id: phs-human-subjects
stable_field_path: /properties/studies
reproduction: >-
  Save one study and blank enrollment report, then open the ordinary print
  route.
evidence_ref: local application 97b7c1b5-7a6b-4bbc-997d-413d6d5eb296 print route
superbee_updated_by: codex
---
# Observation

The ordinary print route loaded and preserved the saved study title and exemption response, but it
also rendered the full inactive nested structure. The blank inclusion-enrollment record alone
included the entire planned and cumulative 115-coordinate matrix as disabled controls, producing an
extremely long review artifact before the applicant entered enrollment data.

# Reproduction

1. Add one study and one blank inclusion enrollment report.
2. Save and reload the form.
3. Open `/print/application/{applicationId}/form/{applicationFormId}`.
4. Observe the saved values followed by all blank inactive study and enrollment fields.

# Evidence boundary

Print rendering itself succeeded. This finding concerns review usability and scope, not loss of
saved data or print-route availability.

# Triage

The new top-level repeatable-group gates should remove inactive study groups when the source
determination is not Yes. Suppressing blank fields inside an intentionally added study requires
either exact embedded-study conditions or an approved generic print-content policy. Neither is
inferred here; verify the top-level improvement and keep the deeper print question open.

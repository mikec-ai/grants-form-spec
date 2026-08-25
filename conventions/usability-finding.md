---
type: Convention
title: Usability Finding
governs: Usability Finding
path: usability-findings/
description: >-
  A reproducible observation from a usability run, kept separate from the
  eventual shared-root-cause diagnosis.
links:
  attributed to: Shared Defect
link_descriptions:
  attributed to: The confirmed or suspected shared defect that explains this observation.
fields:
  required:
    - title
    - superbee_progress_status
    - severity
    - category
    - affected_layer
  optional:
    - form_id
    - stable_field_path
    - reproduction
    - evidence_ref
  values:
    superbee_progress_status:
      - observed
      - triaged
      - resolved
      - dismissed
    severity:
      - blocker
      - major
      - moderate
      - minor
    category:
      - navigation
      - content
      - validation
      - conditional_behavior
      - repetition
      - attachment
      - persistence
      - accessibility
      - print
      - performance
      - other
    affected_layer:
      - form_spec
      - shared_runtime
      - adapter
      - source_or_policy
      - harness
      - unknown
  terminal:
    superbee_progress_status:
      - resolved
      - dismissed
  descriptions:
    title: 'A short user-visible symptom, not a guessed implementation fix.'
    superbee_progress_status: Observed until triage establishes disposition or ownership.
    severity: Impact on completing or understanding the applicant workflow.
    category: The applicant-facing capability affected.
    affected_layer: Root-cause ownership; use unknown until evidence supports attribution.
    form_id: The form where the symptom was observed.
    stable_field_path: >-
      A stable runtime or portable field path when the finding is
      field-specific.
    reproduction: Minimal deterministic steps that reproduce the symptom.
    evidence_ref: 'A durable screenshot, trace, receipt, or local artifact reference.'
---
# Usability Finding

Record the observed symptom first. Similar wording or appearance is not proof that two findings
share a cause. Link to a Shared Defect only after triage establishes a defensible attribution.

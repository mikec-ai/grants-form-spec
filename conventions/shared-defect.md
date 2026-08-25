---
type: Convention
title: Shared Defect
governs: Shared Defect
path: shared-defects/
description: >-
  A triaged root cause that can affect multiple forms and should be fixed at the
  narrowest reusable layer.
links:
  implemented by: Task
link_descriptions:
  implemented by: The concrete implementation task that owns the shared fix.
fields:
  required:
    - title
    - superbee_progress_status
    - severity
    - affected_layer
  optional:
    - impact_scope
    - external_issue
    - owner
  values:
    superbee_progress_status:
      - suspected
      - confirmed
      - fixing
      - fixed
      - verified
      - dismissed
    severity:
      - blocker
      - major
      - moderate
      - minor
    affected_layer:
      - form_spec
      - shared_runtime
      - adapter
      - source_or_policy
      - harness
  terminal:
    superbee_progress_status:
      - verified
      - dismissed
  descriptions:
    title: 'A concise root-cause statement, not a list of form-specific symptoms.'
    superbee_progress_status: 'Verified requires a later usability run, not only a merged code change.'
    severity: Highest demonstrated applicant impact among linked findings.
    affected_layer: The narrowest reusable layer that owns the cause.
    impact_scope: >-
      Known or estimated forms and capabilities affected, with evidence
      boundaries.
    external_issue: Optional private-fork issue or pull-request URL created after triage.
    owner: Person or agent coordinating diagnosis and implementation.
---
# Shared Defect

Create this only after multiple findings or direct technical evidence support a common cause.
Prefer one reusable fix over form-specific branches. A merge may mark the defect fixed; only a
later usability run can mark it verified.

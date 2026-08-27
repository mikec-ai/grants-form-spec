---
type: Shared Defect
title: R&R SF-424 generated conditions conflict with DAT interaction semantics
severity: major
affected_layer: form_spec
impact_scope: >-
  Eight R&R SF-424 compiled conditions are currently excluded from portable
  projection. The official DAT often requires visible-but-disabled controls,
  while the generated producer UI hides them. Similar wording is not treated as
  semantic equivalence.
owner: Codex
superbee_progress_status: confirmed
superbee_updated_by: Codex
---
[implemented by](../tasks/correct-rr-sf424-condition-interactions.md)

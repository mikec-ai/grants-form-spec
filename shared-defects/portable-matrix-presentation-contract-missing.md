---
type: Shared Defect
title: Portable runtime lacks a matrix-presentation contract
severity: major
affected_layer: form_spec
impact_scope: >-
  Confirmed on PHS Inclusion Enrollment (115 coordinates); broader
  dimensional-form impact not yet measured.
external_issue: 'https://github.com/mikec-ai/simpler-grants-gov/pull/138'
owner: codex
superbee_progress_status: confirmed
superbee_updated_by: codex
---
The portable contract preserves unique coordinate-qualified paths but has no generic presentation primitive for a two-dimensional applicant-entry matrix. The consumer therefore renders PHS Inclusion Enrollment as 115 sequential controls, making row/column relationships difficult to understand and leaving screen-reader coordinate context unverified.

This diagnosis is limited to presentation and accessibility. It does not authorize compiling the 8 source-bound conditions or 28 calculation targets whose operands and blank semantics remain unpinned.

[implemented by](../tasks/add-generic-portable-matrix-presentation.md)

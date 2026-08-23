---
type: Task
title: Migrate SF-424C through the portable parity oracle
priority: P1
description: >-
  Replace legacy SF-424C with portable construction-budget composition,
  calculations, and differential XML/lifecycle parity.
superbee_progress_status: in_progress
superbee_updated_by: sf424c_parity
generated:
  by: 'process:superbee'
  at: '2026-08-23T20:30:54.120Z'
assignee: sf424c_parity
---
# Goal

Replace SGG's legacy SF-424C with portable construction-budget composition while using the existing implementation as the parity oracle.

# Evidence starting point

- The research repository contains deterministic SF-424C source extraction, DAT enrichment, and Common Grants candidate analysis, but it is not as mature as the 109-form factory cohort.
- SGG already provides a substantial schema, UI, calculation rules, XML mapping, official XSD, fixtures, and lifecycle implementation.
- Two-year usage evidence records 8,079 form instances; architectural value rather than volume drives its inclusion.

# Acceptance criteria

- Pin exact official source versions/hashes and the legacy SGG oracle revision before authoring.
- Promote the existing deterministic research evidence into the portable evidence contract without treating legacy code as semantic authority.
- Reuse reviewed monetary, budget-total, program-income, percentage, and identity concepts while preserving construction-specific cost categories and projections.
- Declare entered versus calculated values, validation, presentation, and XML mappings explicitly.
- Differentially test representative cost categories, totals, invalid totals, federal-share values, program income, save/reload, locked/print, submission, and XML/XSD behavior.
- Add only demonstrated generic calculation or projection capability and no SF-424C-specific compiler or adapter branch.
- Register only after applicable semantic, calculation, accessibility, instruction, and release gates pass.

# Exit evidence

Record which existing budget abstractions survived unchanged and which genuinely reusable construction-budget capability was added.

[depends on](release-rr-key-person-expanded-canary.md)

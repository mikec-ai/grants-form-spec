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
  at: '2026-08-23T21:12:35.828Z'
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

# Delivery receipt

- Draft PR: https://github.com/mikec-ai/grants-form-spec/pull/53
- Rebasing completed after PR #47 merged; final review-fixed frozen head: `78f2e19689158615e2799db454294d167751fe38` on `codex/sf424c-portable-parity`.
- Producer preflight after review fixes: passed; 102 TypeScript tests and 136 Python tests passed, with one environment-dependent skip.
- GitHub CI passed on the final review-fixed head in 1m21s; GitHub reports the PR clean and mergeable.
- Source provenance pinned: official XSD, DAT, read-only PDF, instructions PDF, deterministic extraction revision/source set, and public SGG oracle revision/file digest.
- Portable result: 18 semantic questions, a reused three-column construction-cost structure, 24 declarative calculations, SGG UI projection, and Grants.gov XML projection. No form-specific compiler or adapter branch was added.
- XML evidence: full, flattened federal-funding-only, contingencies-only, program-income-only, and explicitly empty budget-object responses validate against the pinned official XSD fixture. The two required subtotal containers use generic declarative `emitWhenParentPresent` semantics.
- Calculation evidence: representative values match the existing SGG oracle across cost rows, both subtotals, program income, total project costs, and federal funding share.
- Behavior evidence reconciliation: the evidence target set exactly equals the 24 calculation-rule targets. Every behavior record cites a pinned official source; the calculated eligible-cost display copy cites PDF page 1, line 17, the applicant-entered federal percentage is excluded, and the SGG implementation remains differential parity evidence only.
- Safety boundary: all 18 source-to-question mappings remain `proposed` and are excluded from published coverage metrics.
- Intentional bounded difference: empty drafts do not materialize the legacy implementation's phantom zero totals; populated results remain aligned.

# Remaining gates

- Independent review findings are addressed; freeze for review confirmation and merge coordination.
- Human semantic acceptance or revision for the 18 proposed mappings.
- Human instruction-content and accessibility review.
- Consuming-fork adapter tests for save/reload, locked, print, and submission lifecycle behavior.
- End-to-end submission XML verification, production registration, and release approval.

# Exit evidence

The generic portable compiler, rule operators (`Sum`, `Subtract`, and `PercentOf`), SGG projection, evidence projection, analysis gating, and XML profile projection survived unchanged. The only new reusable authoring capability is the declarative construction-budget question set and its shared three-column cost structure; the migration added no SF-424C-specific runtime machinery.

[depends on](release-rr-key-person-expanded-canary.md)

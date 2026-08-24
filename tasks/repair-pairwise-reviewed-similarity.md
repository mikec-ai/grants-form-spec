---
type: Task
title: Repair reviewed pairwise similarity output
priority: P0
assignee: pairwise_review_fix
description: >-
  Troubleshoot and repair the all-zero Pairwise Reviewed worksheet without
  allowing unreviewed mappings into published similarity.
superbee_progress_status: in_progress
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T15:52:26.916Z'
---
# Goal

Repair the analytical export and workbook generation so the `Pairwise Reviewed` sheet reports reviewed question overlap accurately instead of zero similarity for every form pair.

# Acceptance criteria

- Reproduce the all-zero output from the current 39-form workbook and identify the exact failed join, review-state filter, or workbook transformation.
- Fix the authoritative exporter or workbook builder rather than manually editing spreadsheet cells.
- Preserve directional metrics: intersection count, Jaccard similarity, percent of Form A shared by Form B, and percent of Form B shared by Form A.
- Continue to exclude unreviewed semantic proposals from reviewed similarity metrics.
- Add regression tests with at least one reviewed overlapping pair and one legitimate zero-overlap pair.
- Regenerate and inspect the workbook, confirming nonzero reviewed pairs where reviewed mappings support them.
- Preserve question, form, XML path/type, XSD, version, digest, and extraction provenance already represented by the analytical contract.

# Boundaries

Similar labels or structures are not evidence of semantic equivalence. Do not promote proposed mappings to reviewed status to make the numbers nonzero. Generated workbook files remain build artifacts unless the existing delivery process explicitly publishes them elsewhere.

[depends on](unified-form-analysis-export.md)

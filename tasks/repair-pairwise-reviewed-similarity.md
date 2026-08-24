---
type: Task
title: Repair reviewed pairwise similarity output
priority: P0
assignee: pairwise_review_fix
description: >-
  Troubleshoot and repair the all-zero Pairwise Reviewed worksheet without
  allowing unreviewed mappings into published similarity.
superbee_progress_status: done
superbee_updated_by: pairwise_review_fix
generated:
  by: 'process:superbee'
  at: '2026-08-24T16:02:11.253Z'
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

# Delivery receipt

Completed in public-fork PR [mikec-ai/grants-form-spec#75](https://github.com/mikec-ai/grants-form-spec/pull/75), commit `34f6941ef`.

## Diagnosis

- The current 39-form analytical projection contains 1,362 exploratory associations and zero accepted occurrence mappings. A reviewed-only overlap cannot yet be computed from that evidence.
- The exporter correctly left similarity blank when both forms lacked accepted mappings, but still emitted zero counts. The workbook therefore visually suggested 0% similarity instead of unavailable evidence.
- The eligibility rule also used the union of accepted sets. Once one form gained an accepted question, an unreviewed counterpart would have been reported as a false 0% comparison.
- The exact occurrence-path mapping join was not losing accepted rows; the missing reviewed output is the current review state, not a failed join.

## Fix and evidence

- Reviewed pair eligibility now requires at least one accepted occurrence on both forms.
- All six metrics are blank whenever either side lacks accepted evidence: intersection, both denominators, Jaccard similarity, and both directional shares.
- A direct regression fixture exercises the exact path-qualified accepted-mapping join, a reviewed overlap with 1 shared question out of 3 unique questions (33.3% Jaccard and 50% in both directions), a fully reviewed disjoint pair with a legitimate 0%, and an unavailable pair with blank metrics.
- The regenerated 39-form workbook contains 741 reviewed pairs, zero eligible pairs, and zero nonblank reviewed metric cells, faithfully reflecting the current zero accepted associations without promoting any proposal.
- Full repository preflight passed: 118 TypeSpec tests and 311 Python tests passed, with 2 intentional skips. Generated artifact digest: `d11d189a799cec8dee62d9dfa9742096913e130d7b7f2dacbe90560ee77d8ec6`.

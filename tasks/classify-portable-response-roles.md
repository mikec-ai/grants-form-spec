---
type: Task
title: Classify portable response roles
priority: P0
description: >-
  Add target-neutral occurrence roles so semantic questions, system values,
  calculations, attestations, controls, and static content remain distinct.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:35:27.885Z'
assignee: codex
---
# Objective

Represent why a value exists independently from its semantic question identity, UI widget, and XML projection.

# Scope

- Add a portable response-role vocabulary covering at least applicant input, calculated output, system value, technical field, attestation, and static content.
- Define whether the role is authored on a canonical block, an occurrence, or both, including the precedence rule for form-specific overrides.
- Emit the role in the portable artifact graph and consume it in the analysis workbook.
- Keep the vocabulary target-neutral. The SGG adapter may consume emitted roles but must not own per-form classifications.
- Preserve `unclassified` as an explicit unknown; do not infer roles from `readOnly`, labels, field names, widgets, or XML paths.

# Acceptance criteria

- Contract schema, TypeSpec decorators/types, documentation, emitter tests, and conformance fixtures agree on the vocabulary and override semantics.
- `form-question-associations.csv` reports authored roles rather than assigning every occurrence `unclassified`.
- Non-question form-local fields can be explicitly classified without being promoted into semantic similarity metrics.
- Existing artifacts remain deterministic and all producer validation passes.

# Result

Implemented in grants-form-spec PR #41 at commit `6515f80`. `@Response.role` supports applicant input, calculated output, system value, technical field, attestation, and static content on reusable blocks or form properties. Property roles override reusable defaults, and the resolved role is emitted per path in the portable form index. Analysis consumes only emitted artifacts and never infers roles from UI, labels, XML, or delivery behavior. No SGG adapter knowledge was added. Full preflight passed on the latest main branch.

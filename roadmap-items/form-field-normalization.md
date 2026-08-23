---
type: Roadmap Item
title: Classify and normalize form-local fields
description: >-
  Resolve the emitted unclassified-field ledger without duplicate questions or
  adapter-side form knowledge.
sequence: '5'
superbee_progress_status: active
superbee_updated_by: codex
---
# Outcome

Turn the current form-local-field ledger into an evidence-backed portable classification with no
unknown occurrences, while preserving canonical question lineage and keeping SGG-specific delivery
logic out of the form specification.

# Baseline

At producer commit `46e71d5`, 90 emitted form/field occurrences are unclassified. Triage separates
14 canonical-lineage artifacts, 58 likely semantic questions, 12 lifecycle-ownership decisions, and
6 attestation or UI/workflow controls.

# Sequence

1. Add a target-neutral response-role vocabulary and emitted occurrence metadata.
2. Repair lineage accounting so inherited/spread questions are not reported as local debt.
3. Normalize the SF-424 cover family and the smaller reference-form semantic backlog.
4. Resolve lifecycle-owned, attestation, and technical-control fields with source evidence.
5. Add a conformance gate that prevents unknown classifications from returning.

# Stop condition

- Every currently emitted field is attributable to a canonical semantic question, capture
  mechanism, calculated/system value, technical field, attestation, or static content.
- `unclassified-form-fields.csv` is empty for the 19-form baseline without duplicate canonical
  questions or adapter-side form profiles.
- Reviewed reuse remains distinct from implementation-derived reuse.

[contains](../tasks/classify-portable-response-roles.md)

[contains](../tasks/repair-form-local-lineage-analysis.md)

[contains](../tasks/canonicalize-sf424-cover-question-clusters.md)

[contains](../tasks/promote-residual-reference-form-questions.md)

[contains](../tasks/resolve-lifecycle-attestation-control-fields.md)

[contains](../tasks/enforce-classified-form-field-gate.md)

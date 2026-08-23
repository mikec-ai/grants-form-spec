---
type: Roadmap Item
title: Classify and normalize form-local fields
description: >-
  Thirty-form field normalization is complete and enforced by a permanent
  zero-unclassified CI gate.
sequence: '5'
superbee_progress_status: done
superbee_updated_by: codex
---
# Outcome

The form-local-field ledger is fully resolved across the 30-form producer baseline without duplicate semantic questions or adapter-side form knowledge.

# Result

- Target-neutral response roles and emitted occurrence metadata distinguish applicant input, calculated output, system values, technical fields, attestations, and static content.
- Canonical lineage accounting includes inherited and spread questions correctly.
- The SF-424 cover family and residual reference-form questions compose canonical source-bound declarations while all semantic mappings remain proposed and unpublished.
- Lifecycle, attestation, and technical controls are explicitly classified from evidence.
- The temporary 76-row ratchet was replaced by a permanent zero-unclassified CI gate in producer PR 55, merged as `825ee6b1dc3c038e4dbacbb38ffab52e4b4f6100`.
- The current 30-form analysis reports zero unclassified occurrences and an empty exception ledger.
- Any future exception must resolve canonical repository evidence and carry a recognized Superbee task or GitHub issue/PR removal reference; silent allowlists fail.

# Continuing invariant

Every emitted field must have canonical semantic lineage or an explicit non-question response role. Similarity and marginal reuse continue to count only semantic questions and intended capture mechanisms. Only reviewed mappings may contribute to published coverage.

[contains](../tasks/classify-portable-response-roles.md)

[contains](../tasks/repair-form-local-lineage-analysis.md)

[contains](../tasks/canonicalize-sf424-cover-question-clusters.md)

[contains](../tasks/promote-residual-reference-form-questions.md)

[contains](../tasks/resolve-lifecycle-attestation-control-fields.md)

[contains](../tasks/enforce-classified-form-field-gate.md)

[contains](../tasks/enforce-no-new-unclassified-debt-ratchet.md)

[contains](../tasks/correct-previous-grants-tracking-response-role.md)

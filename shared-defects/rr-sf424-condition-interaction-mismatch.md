---
type: Shared Defect
title: R&R SF-424 generated conditions conflict with DAT interaction semantics
severity: major
affected_layer: form_spec
impact_scope: >-
  All eight R&R SF-424 condition interactions are corrected in the producer and
  projected generically in the consumer. A later browser usability run is still
  required before marking the defect verified.
owner: Codex
superbee_progress_status: fixed
superbee_updated_by: Codex
external_issue: 'https://github.com/mikec-ai/grants-form-spec/pull/123'
---
[implemented by](../tasks/correct-rr-sf424-condition-interactions.md)

# Fix evidence

Producer PR #123 and consumer PR #36 are merged. Exact official DAT records authorize seven visible-but-disabled interactions and one conditionally required tracking field with no visibility change. The portable package now executes those semantics without a form-specific renderer branch.

---
type: Shared Defect
title: Encoded checkbox state races conditional rerenders
severity: major
affected_layer: shared_runtime
impact_scope: >-
  Confirmed on SF-424 Revision type; applies to any encoded-checkbox field
  inside conditional UI.
external_issue: 'https://github.com/mikec-ai/simpler-grants-gov/pull/138'
owner: codex
superbee_progress_status: verified
superbee_updated_by: codex
---
The encoded checkbox widget updated its local hidden input and invoked the ordinary change callback, but conditional UI evaluation could rerender before the parent form state reflected the first selection. The visible choice then disappeared or failed to persist.

The generic repair exposes a bounded form-data synchronization seam through widget support and retains exact source-approved combination validation.

[implemented by](../tasks/synchronize-encoded-checkbox-form-state.md)

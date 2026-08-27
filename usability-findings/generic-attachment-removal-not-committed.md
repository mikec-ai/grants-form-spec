---
type: Usability Finding
title: Generic attachment removal can announce success before the response changes
severity: moderate
category: attachment
affected_layer: shared_runtime
form_id: attachment-form
stable_field_path: /attachments
reproduction: >-
  Select an attachment in Simpler-compatible presentation, switch to Generic
  JSON Forms, then remove it; the control can announce removal while the UUID
  remains in response data.
evidence_ref: >-
  grants-form-workbench branch codex/agent-usability-gate; browser pilot plus
  packages/attachment-controls/test/attachment-controls.test.tsx
superbee_progress_status: triaged
superbee_updated_by: Codex
---
[attributed to](../shared-defects/attachment-removal-confirmation-race.md)

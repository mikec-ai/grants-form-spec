---
type: Shared Defect
title: Nested FieldLists collide on leaf-only child identity
severity: major
affected_layer: shared_runtime
impact_scope: >-
  Confirmed on R&R Budget; affects any FieldList entry with multiple nested
  groups that reuse a leaf name.
external_issue: 'https://github.com/mikec-ai/simpler-grants-gov/pull/138'
owner: codex
superbee_progress_status: verified
superbee_updated_by: codex
---
FieldList children used only the final leaf name as their React key. In R&R Budget, nested personnel groups reuse leaf names, producing duplicate keys, unstable component identity, and incorrect persistence/calculation behavior.

The fix scopes identity to the existing fully qualified generated path while preserving storage paths and submitted field names.

[implemented by](../tasks/scope-nested-fieldlist-child-identity.md)

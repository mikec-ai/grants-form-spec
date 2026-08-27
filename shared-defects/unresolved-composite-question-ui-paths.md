---
type: Shared Defect
title: Portable UI validation does not resolve packaged composite-question references
severity: major
affected_layer: shared_runtime
impact_scope: >-
  Confirmed on SF-424: five contactPerson controls point inside a packaged
  generics/person-name reference and are incorrectly rejected against the
  unresolved form schema. Any future form that scopes UI controls inside a
  composite packaged question may be affected; broader count is not yet
  measured.
owner: Codex-producer-cohort-agent
superbee_progress_status: fixing
superbee_updated_by: Codex
---
The workbench validates UI scopes against the unresolved form schema, so a valid nested control beneath a packaged question $ref appears absent. The central fix must resolve only verified packaged question references, remain cycle-safe, reject unknown references, and leave original producer artifacts unchanged.

[implemented by](../tasks/integrate-pinned-producer-cohort-in-workbench.md)

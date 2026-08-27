---
type: Shared Defect
title: Portable packaged-question reference handling is incomplete
severity: major
affected_layer: shared_runtime
impact_scope: >-
  Confirmed on SF-424 UI validation: five contactPerson controls resolve through
  generics/person-name. Independent review also proved that valid packaged
  questions using nested $id resources or $anchor fragment references can
  validate but fail compilation. Any composite question or packaged schema with
  local resource boundaries may be affected; broader catalog count is not yet
  measured.
owner: Codex-producer-cohort-agent
superbee_progress_status: fixing
superbee_updated_by: Codex
---
Validation and compilation do not yet share a fully resource-aware packaged-question resolver. The central fix must resolve only verified packaged resources, preserve JSON Schema nested resource and anchor semantics, remain cycle-safe, reject unknown references, avoid conflicting embedded resource identifiers, and leave producer artifacts unchanged.

[implemented by](../tasks/integrate-pinned-producer-cohort-in-workbench.md)

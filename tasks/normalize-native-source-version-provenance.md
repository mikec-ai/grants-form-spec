---
type: Task
title: Normalize native source version provenance
priority: P2
description: >-
  Define and backfill an unambiguous distinction between enclosing form version,
  native source version, and explicitly unknown source versions across all
  evidence sidecars.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:09:09.195Z'
---
# Goal

Remove the historical ambiguity where imported XSDs and unversioned documents can inherit an enclosing form version as though it were the source document version.

# Acceptance criteria

- The evidence contract distinguishes enclosing form version, native source version, and an explicitly unknown native version without inference.
- All canonical evidence sidecars are regenerated or deterministically backfilled.
- Versioned Grants.gov XSD URI parsing covers the formats present in pinned evidence and fails actionably on unsupported formats.
- Unversioned PDF, DAT, instruction, and other sources do not receive invented native versions.
- Tests validate every sidecar and preserve URI plus SHA source identity digests unless the contract explicitly versions them.

# Boundary

Deliver this as a dedicated provenance-contract change, separate from XML mapping-fragment refactors.

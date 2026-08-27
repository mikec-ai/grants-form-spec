---
type: Task
title: Import a pinned producer-backed form cohort into the workbench
priority: P0
assignee: Codex-producer-cohort-agent
description: >-
  Create one generic, repeatable import path from exact grants-form-spec
  revisions into the workbench catalog. The active cohort is SF-424, SF-424
  Short, Attachment Form, and PHS Assignment Request; all four currently import
  and capture 94 exact generated artifacts. Preserve raw producer manifests
  byte-for-byte plus content digests, producer paths, revisions, semantic review
  states, and question authority. A surfaced contract mismatch is handled only
  at design-time: empty optional identity values such as ombNumber are omitted
  from the strict portable projection while the exact raw value and path remain
  in a normalization receipt; non-empty values are unchanged and required empty
  fields must fail. Proposed or unreviewed mappings remain explicitly so and do
  not contribute to published semantic coverage. No form-ID branches, runtime
  producer dependency, or silent semantic acceptance.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T00:46:01.919Z'
---
[depends on](implement-portable-form-catalog.md)

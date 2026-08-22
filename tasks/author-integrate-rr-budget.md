---
type: Task
title: Author and integrate R&R Budget 3.0
priority: P0
assignee: mikec-ai
description: >-
  Completed end to end. R&R Budget 3.0 is declaratively authored from pinned
  official XSD and extraction evidence in grants-form-spec, with five repeating
  groups, 30 ordered source-resolved calculations, and three attachment
  validations. Producer PRs 6, 7, and 8 are merged; merged producer revision
  5bfce63341e6afa517d1bb159f87906fcbe80b34 produced the runtime bundle pinned by
  the adapter. Public Simpler fork PR 6 is merged at
  b6fe7b6abc8760b6729cfc807f46b4af8fe2801d through the generic adapter with no
  form-specific schema builder. UI and rule schemas match the prior local oracle
  exactly. Shared composition, hoisted-definition overlays, runtime
  construction, wire-name projections, decimal constraints, representative
  calculations, and provenance have regression coverage. Producer PR 9 is also
  merged at df2392ca855054ad1c8ea15648d1ef7dfeba99cf so CI publishes generated
  analysis beside the portable bundle instead of checking analysis or oracles
  into the runtime repository.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T18:12:47.364Z'
---


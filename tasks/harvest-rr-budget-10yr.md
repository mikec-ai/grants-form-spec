---
type: Task
title: Harvest R&R Budget 10YR through the portable architecture
priority: P0
assignee: codex
description: >-
  Completed end to end. Producer PR 15 merged at
  ee6563957311df922fbaf6c7d6ee18c3cc24c4d5 and adds source-bound R&R Budget 10YR
  with pinned official XSD/extraction evidence and semantic review status
  unreviewed. Implementation-derived analysis confirms the 5-year and 10-year
  profiles share all 14 transitive semantic questions with 100 percent
  bidirectional coverage; emitted schemas differ only in identity, period copy,
  and maxItems 5 to 10. The portable package contract now permits a missing
  legacy consumer ID instead of requiring invented data. Public Simpler fork PR
  10 merged at 3d4e6a4ab and integrates the form through the generic adapter. A
  reusable projection-profile inheritance capability lets the derivative reuse
  the R&R Budget wire mapping by reference. The complete 56-calculation graph is
  reused and representative cumulative calculations execute. Seventy-three
  portable-form, parity, projection, artifact-integrity, and registry tests
  pass. No HHS upstream branch or issue was changed.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T19:52:59.294Z'
---


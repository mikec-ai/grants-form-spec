---
type: Task
title: Harvest R&R Subaward Budget 30 through the portable architecture
priority: P0
assignee: codex
description: >-
  Completed end to end. Producer PR 16 merged at
  81d2e17ff322c92f19f31f6b57aefb058b2f614e and adds the source-bound five-year
  R&R Subaward Budget 30 ATT profile. It reuses the existing
  ResearchBudgetDetails block; the only emitted structural difference from the
  10-subaward sibling is maxItems 10 to 30 plus identity and explanatory copy.
  Implementation-derived analysis reports the same transitive semantic question
  set with 100 percent pairwise and bidirectional overlap. The official wrapper
  and embedded budget XSDs are hash-pinned, semantic review remains unreviewed,
  and ATT1 through ATT30 are explicitly treated as technical capture slots
  rather than new questions. Public Simpler fork PR 11 merged at 948117fca. Its
  execution tests exposed and fixed a generic nested-rule gap: Simpler now
  preserves and resolves @PARENT references, so cumulative calculations remain
  scoped independently to each subaward in both 10- and 30-subaward forms.
  Ninety-one focused tests pass; Ruff and Mypy pass. Broader DB-backed tests are
  locally unavailable only because grants-db is not running. No HHS upstream
  branch or issue was changed.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T20:02:13.387Z'
---


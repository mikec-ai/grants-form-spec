---
type: Task
title: Promote R&R Subaward Budget 10YR/30 through the crosswalk staging seam
priority: P0
assignee: codex
description: >-
  Use the revision-pinned promotion importer to stage deterministic
  RRSubawardBudget10_30 source facts, keep semantic mappings unreviewed, author
  the canonical declarative composition, integrate it through the public Simpler
  fork, and verify nested 10-year calculations without changing HHS upstream.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T20:04:28.037Z'
---
# Objective\n\nExercise the merged promotion importer on the next inexpensive derivative, then deliberately reconcile its staged evidence into canonical portable declarations and the thin Simpler adapter.\n\n# Acceptance criteria\n\n- Promotion packet is pinned to an exact crosswalk revision and reproducible.\n- Deterministic source facts and proposed semantics remain visibly separate.\n- Canonical composition reuses the existing research-budget question bank and rule graph.\n- Implementation-derived analysis reports overlap without treating it as reviewed semantic equivalence.\n- Public-fork adapter executes nested calculations across multiple subawards and ten budget periods.\n- Tests and preflight pass; no HHS upstream branch, PR, or issue changes.

[depends on](spike-crosswalk-promotion-importer.md)

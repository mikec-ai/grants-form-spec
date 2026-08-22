---
type: Task
title: Promote R&R Subaward Budget 10YR/30 through the crosswalk staging seam
priority: P0
assignee: codex
description: >-
  Completed end to end. The merged promotion importer staged 231 deterministic
  source records, 141 behavior records, 213 proposed runtime rules, and five
  exact schema sources from crosswalk revision
  dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef, with zero accepted semantic
  mappings. Producer PR 17 merged at 5121706d3 and added a declarative 10-period
  profile over the shared ResearchBudgetDetails block plus the 30-subaward
  wrapper. The run exposed and fixed two generic architecture gaps:
  family-ledger behavior evidence can now be promoted without a layout-specific
  exception, and anonymous declarative profiles inherit the complete shared rule
  graph. The twelfth portable form has the same 15 implementation-derived
  semantic questions as both subaward siblings, six repeating groups, and all 56
  calculations. Public Simpler fork PR 12 merged at 66557e2b7 with no renderer,
  frontend, projection profile, or new calculation capability; execution tests
  prove independent parent-scoped totals across multiple subawards. Full
  producer preflight, 55 TypeScript tests, 22 Python tests, 11 targeted adapter
  tests, Ruff, and Mypy pass. Broader non-form rule tests have 64 passes and 16
  environment-only database fixture errors because grants-db is unavailable. No
  HHS upstream state changed.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T20:42:28.643Z'
---
# Objective\n\nExercise the merged promotion importer on the next inexpensive derivative, then deliberately reconcile its staged evidence into canonical portable declarations and the thin Simpler adapter.\n\n# Acceptance criteria\n\n- Promotion packet is pinned to an exact crosswalk revision and reproducible.\n- Deterministic source facts and proposed semantics remain visibly separate.\n- Canonical composition reuses the existing research-budget question bank and rule graph.\n- Implementation-derived analysis reports overlap without treating it as reviewed semantic equivalence.\n- Public-fork adapter executes nested calculations across multiple subawards and ten budget periods.\n- Tests and preflight pass; no HHS upstream branch, PR, or issue changes.

[depends on](spike-crosswalk-promotion-importer.md)

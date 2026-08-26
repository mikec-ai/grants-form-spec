---
type: Task
title: Evaluate SF-424A generic table adoption
priority: P2
description: >-
  Assess replacing specialized budget widgets incrementally through one bounded
  proof.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-26T11:45:19.698Z'
---
# Scope

Evaluate whether the six specialized SF-424A budget widgets can be incrementally expressed through the generic table contract. Treat this as modernization analysis plus one bounded proof, not an automatic rewrite.

# Acceptance

- Compare existing specialized behavior, instructions, calculations, accessibility, and print behavior against generic capability.
- Identify which sections are safe generic-table candidates and which still require specialized behavior.
- Implement at most one representative section before recommending broader migration.

[depends on](extend-simpler-nested-table-runtime.md)

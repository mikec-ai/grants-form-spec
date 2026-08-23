---
type: Task
title: Add composable presence conditions
priority: P0
assignee: condition_agent
description: >-
  Add the smallest generic condition vocabulary needed to express count-at-limit
  OR existing attachment presence across producer and SGG frontend.
superbee_progress_status: todo
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:06:46.589Z'
---
# Goal

Represent and execute boolean condition composition and attachment presence without a form-specific branch.

# Acceptance criteria

- Declarative conditions support a presence predicate and boolean OR composition.
- Producer contracts, compiler output, and conformance tests cover the new vocabulary.
- Simpler projection/frontend evaluate it generically for scalar and attachment values.
- Existing condition behavior is unchanged.
- Synthetic and Key Person overflow-gating tests prove the capability.

# Boundary

Do not build a general expression language or application workflow engine.

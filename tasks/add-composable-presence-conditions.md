---
type: Task
title: Add composable presence conditions
priority: P0
assignee: condition_agent
description: >-
  Add the smallest generic condition vocabulary needed to express count-at-limit
  OR existing attachment presence across producer and SGG frontend.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T17:24:59.322Z'
---
---
type: Task
title: Add composable presence conditions
priority: P0
assignee: condition_agent
description: >-
  Add the smallest generic condition vocabulary needed to express count-at-limit
  OR existing attachment presence across producer and SGG frontend.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:06:54.924Z'
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

# Result

Delivered in ordered producer and adapter changes.

- grants-form-spec PR #37 merged as 9e76609aa2d074c0252de181305653a26ca237ac.
- simpler-grants-gov PR #34 merged as ca31bb29d3adb45c1805589afa304ca1b9e2dc7a.
- One bounded enabledWhenCountOrPresent decorator emits count-at-least OR target-present without exposing a general expression AST.
- Count sources must be arrays in the same resolved declaring model, aliases are supported, foreign namespace collisions are rejected, and thresholds must be positive.
- Compiler Model identity remains out-of-band in a WeakMap, preserving JSON serialization and inheritance linting.
- Canonical JSON Forms and SGG emissions agree; existing adapter any/present evaluation and recursive pointer projection are explicitly tested.
- Full producer preflight and CI passed with 90 TypeScript tests, 68 Python tests, and 660 artifacts. Adapter projection/frontend/static checks passed.

The actual Key Person overflow annotations are governed by the separate integration task.

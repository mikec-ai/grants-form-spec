---
type: Roadmap Item
title: Portable form workbench and replaceable presentation presets
description: >-
  Active independent-consumer roadmap. Architecture foundation merged in
  grants-form-workbench PR #1 on 2026-08-27 at merge commit
  19736adedbdaf61545e525d55b96d2b4c2fb38b7. It includes the replaceable
  Simpler-compatible preset, layouts, collections, typed controls, an immutable
  verified catalog, bounded declarative behaviors, and enforced dependency
  boundaries. Independent architecture review approved; 124 tests, typecheck,
  all workspace builds, dependency-tree checks, and diff checks passed locally.
  GitHub-hosted CI could not start because the account Actions billing/minute
  limit blocked the runner; this remains an external capacity gate rather than a
  failing test. The next milestone is a genuine multi-form proof using pinned
  grants-form-spec packages, live behavior execution, preset swapping, and
  bounded browser and human-review evidence without form-specific runtime
  branches.
sequence: '8'
superbee_progress_status: active
superbee_updated_by: Codex
---
[contains](../tasks/implement-simpler-compatible-renderer-preset.md)

[contains](../tasks/implement-simpler-layout-renderers.md)

[contains](../tasks/implement-simpler-collection-renderer.md)

[contains](../tasks/enforce-workbench-package-boundaries.md)

[contains](../tasks/implement-richer-simpler-compatible-controls.md)

[contains](../tasks/implement-portable-declarative-behaviors.md)

[contains](../tasks/implement-portable-form-catalog.md)

[contains](../tasks/integrate-pinned-producer-cohort-in-workbench.md)

[contains](../tasks/execute-portable-behaviors-in-workbench-renderer.md)

[contains](../tasks/prove-real-form-preset-swapping.md)

[contains](../tasks/close-workbench-multi-form-proof.md)

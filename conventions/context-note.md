---
type: Convention
title: Context Note
governs: Context Note
path: context-notes/
fields:
  required:
    - title
    - timestamp
  optional:
    - description
    - tags
sections:
  - Summary
freshness_horizon: 24h
browse_collapsed: true
superbee_updated_by: codex
---
# Context Note

An agent's cross-session orientation note: what happened, what was decided, and what's still open. Create one with `new "Context Note" <id>` (scaffolds the `# Summary` section under `context-notes/`), read it with `doc read`, and edit it with `doc update` / `doc write`. This recipe retains `timestamp` as an explicit compatibility field and uses the Superbee-specific `freshness_horizon` Kind extension so `superbee status` can surface notes older than 24h. In an OKF v0.2 bundle, `generated.at` remains the standard meaningful-change clock when provenance is present.

## Declaring a kind convention

A kind convention is a plain OKF doc (`type: Convention`) living under `conventions/`. Its FRONTMATTER is the only part core parses (this prose is not). Supported frontmatter keys:

- `governs` (required, non-empty) — the `type` value this convention governs.
- `title` (optional) — display title; defaults to `governs`.
- `description` (optional) — the kind's purpose and intended

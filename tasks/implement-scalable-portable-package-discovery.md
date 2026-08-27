---
type: Task
title: Replace static demo imports with scalable portable package discovery
priority: P1
description: >-
  Define and implement an environment-owned package discovery/loading boundary
  so additional portable packages can be added without editing a static Vite
  import map. Keep catalog identity/digest verification and producer provenance
  intact; do not move presentation or form-specific logic into the loader.
  Acceptance: generic manifest/index contract, failure and race handling,
  multi-package tests, and a migration path from the bounded demo transport.
superbee_progress_status: in_progress
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T02:49:23.117Z'
assignee: Codex-discovery-agent
---
[depends on](close-workbench-multi-form-proof.md)

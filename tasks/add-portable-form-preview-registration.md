---
type: Task
title: Add test-only portable form registration and preview
superbee_progress_status: in_progress
priority: P0
description: >-
  Expose every SGG-banked portable form through the real SGG frontend in
  test/dev without changing production registration.
actor: Codex
timestamp: '2026-08-23T22:26:30.965Z'
assignee: codex
superbee_updated_by: codex
---
# Goal

Add a test/dev-only registration and preview mechanism that can load every SGG-banked portable form through SGG's existing form runtime and frontend without changing production routing.

# Scope

- Enumerate portable forms from the promoted artifact manifest and SGG bank metadata.
- Provide stable preview/test routes or fixtures for every banked form.
- Reuse the production renderer, schema/rules/XML adapters, and lifecycle code paths.
- Keep the mechanism unavailable or inert in production configuration.
- Preserve the existing production registration allowlist exactly.

# Acceptance criteria

- A test can discover and open every banked portable form without per-form registration code.
- The preview path uses the real SGG runtime; no parallel renderer or reference consumer is introduced.
- Automated checks prove that production form registrations are unchanged.
- Adding a conforming banked form requires no hand-authored frontend registration branch.

[depends on](grants-form-data-driven-registration.md)

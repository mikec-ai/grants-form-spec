---
type: Task
title: Add test-only portable form registration and preview
superbee_progress_status: done
priority: P0
description: >-
  Expose every SGG-banked portable form through the real SGG frontend in
  test/dev without changing production registration.
actor: Codex
timestamp: '2026-08-23T22:26:30.965Z'
assignee: codex
superbee_updated_by: codex-root
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

# Completion receipt

- Consumer PR: `https://github.com/mikec-ai/simpler-grants-gov/pull/63`
- Reviewed exact head: `de383aec1831adefddbf35505005abf780e21570`
- Consumer main merge: `4c8b331798c0f31552cff2759a868ba25cd795b6`
- The implementation discovers the live artifact manifest without an allowlist and built all 39 selected packages at the time of merge through Simpler's real registry.
- Preview identities are deterministic UUIDv5 values reserved for lower-environment previews and collision-checked against the production registry.
- Enablement requires both an explicit flag and a local, test, or dev environment. Production identities, registrations, `FormType`, instructions, and XML remain unchanged or unavailable.
- Independent exact-head review found no actionable issues. The full 4,519-test API suite passed. The separate E2E workflow failed before Playwright because the shared API readiness probe timed out identically on consumer main; this did not exercise preview behavior.

---
type: Task
title: Run the banked portable catalog through browser conformance
superbee_progress_status: todo
priority: P0
description: >-
  Generate real-frontend browser and lifecycle conformance for the expected
  35-form SGG bank.
actor: Codex
timestamp: '2026-08-23T22:26:31.124Z'
---
# Goal

Generate and run a browser-conformance matrix for the expected 35-form SGG bank through the real SGG frontend.

# Coverage

For each applicable form capability, exercise:

- initial load and complete field rendering;
- minimal and maximal valid submissions;
- conditional visibility and requirement changes;
- repeaters, attachments, and calculations;
- save and reload behavior;
- locked/read-only and print surfaces;
- accessibility checks, including automated axe coverage and essential keyboard interaction.

# Acceptance criteria

- The matrix is generated from manifests, schema annotations, and declared capabilities rather than a hand-maintained list of per-form branches.
- Every banked form produces an attributable pass/fail receipt with skipped capabilities explained.
- Failures identify whether the defect belongs to portable content, the adapter, or the shared SGG runtime.
- The suite is suitable as a promotion/release gate without requiring production registration.

[depends on](add-portable-form-preview-registration.md)

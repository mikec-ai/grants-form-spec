---
type: Task
title: Automate cross-repository form promotion
priority: P0
assignee: codex
description: >-
  Create a configurable, consumer-owned supervised workflow that promotes an
  immutable producer artifact revision into an unregistered SGG banking PR,
  serializes concurrent updates, runs generic gates, and proves the path with
  SF-424C.
superbee_progress_status: in_progress
generated:
  by: 'process:superbee'
  at: '2026-08-23T21:28:53.074Z'
---
# Goal

Reduce producer-to-consumer coordination to one supervised promotion while preserving immutable provenance and the producer/adapter boundary.

# Acceptance criteria

- Repository coordinates and producer revision are workflow inputs, not hard-coded architectural assumptions.
- Concurrent promotions are serialized.
- Existing selection is preserved and requested forms are added deterministically.
- Producer artifacts and required official XSDs are verified before atomic replacement.
- The workflow opens or updates an unregistered consumer PR with test and provenance receipts.
- SF-424C proves the path without changing production registration.

[depends on](grants-form-pin-update-automation.md)

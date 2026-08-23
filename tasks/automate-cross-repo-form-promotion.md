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
superbee_progress_status: done
generated:
  by: 'process:superbee'
  at: '2026-08-23T22:04:59.655Z'
superbee_updated_by: codex
---
# Goal

Reduce producer-to-consumer coordination to one supervised promotion while preserving immutable provenance and the producer/adapter boundary.

# Delivered

- SGG PR #48 (`0b5e9613`) added deterministic additive promotion, immutable producer coordinates, serialized execution, a machine-readable receipt, and the unregistered-PR boundary.
- SF-424C was promoted from producer `825ee6b1dc3c038e4dbacbb38ffab52e4b4f6100`: 29 selected forms, 324 selected artifacts, bundle SHA-256 `3c58f0d8006054f425402f99e36019f23d9675e2c159c8ac49ff7fd83fd350b6`. Runtime identity, compatibility projection, calculations, and exact official-XSD validation landed without production registration.
- SGG PR #49 (`d65deacb`) removed the sync tool's accidental dependency on the full API runtime.
- SGG PR #50 (`a3f7143`) installed producer XML validation dependencies and made consumer digest/XSD verification dependency-free.
- Hosted run `32669278105` passed from merged `main` in 1m50s and correctly no-op'd because SF-424C was already banked. It ran producer preflight, bundle build and verification, consumer digest/XSD gates, and registration isolation.

# Verification

- 218 practical non-DB consumer tests passed for the main delivery.
- Focused integrity/provenance/sync/updater suites passed after portability hardening.
- Ruff, mypy, repository workflow lint, and hosted promotion passed.
- DB-backed gates remain separate because the local `grants-db` fixture was unavailable; the workflow never registers forms.

[depends on](grants-form-pin-update-automation.md)

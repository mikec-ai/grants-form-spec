---
type: Task
title: Close R&R SF-424 Multi-Project Cover technical gates
description: >-
  Exact XML/XSD and bounded Simpler lifecycle/browser closure for the portable
  Multi-Project Cover.
superbee_updated_by: multiproject_cover_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T08:30:52.916Z'
---
# Objective

Move the already-banked R&R SF-424 Multi-Project Cover from adapter canary to technical human-review handoff while preserving source-specific optionality and keeping human gates separate.

# Technical result

- Producer PR [#106](https://github.com/mikec-ai/grants-form-spec/pull/106), commit `4ccabcbb8539a747f0dee85c60da7bdb9016e362`, pins the official 4.0 root XSD at SHA-256 `5d5599068d721e6554fa442df88711f8d9386a5fafc18b01cb1d1becc41f84e7`.
- The XML profile composes the existing R&R SF-424 mapping with a generic build-time `$rename`/`$overlay`; the only source-backed wire delta is `GGTrackingID` to `GrantsTrackingNumber`.
- The common projection now uses the existing declarative `container` mechanism for Congressional District, preventing a phantom empty wrapper when this all-optional form has no response.
- Exact-XSD tests prove an empty response, a representative lifecycle response, ordering, and the 13-character lower bound for the tracking number.
- Full producer preflight passed: 34/34 XSD fixtures, 320 blocks, 1,708 artifacts, 125 TypeScript tests, 367 Python tests, a verified 1,186-artifact bundle, and zero unclassified fields.
- Consumer PR [#112](https://github.com/mikec-ai/simpler-grants-gov/pull/112), commit `496d07979e09a80dbcb980a574028a60d73ec221`, vendors the exact XSD and profile and adds generic preview, validation, submission, and XML/XSD lifecycle proof.
- Consumer focused result: 20 lifecycle/provenance/integrity tests passed; Ruff, mypy, artifact integrity, and exact-XSD integrity passed.

# Pending receipt

Bounded hosted browser run [#32826954842](https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32826954842) is queued for `rr-sf424-multi-project-cover`. Do not merge the consumer PR until that receipt is green and the coordinating agent approves.

# Explicit boundaries

The form remains unregistered. Semantic mappings remain proposed. Policy, accessibility, human acceptance, and production release are not claimed by this task.

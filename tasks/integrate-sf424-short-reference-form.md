---
type: Task
title: Integrate the existing SF-424 Short reference form
priority: P1
assignee: mikec-ai
description: >-
  Delivered Billy's existing SF-424 Short artifact through the generic Simpler
  adapter. UI schema, rule schema, rendered fields, and conditional requiredness
  match the existing implementation. Across 517 generated behavioral payloads
  there were zero validation differences. The only consumer-specific
  declarations are one legacy field rename and three legacy read-only
  annotations, each stored as data with a required rationale; no form-specific
  Python branch was added. Sixty-five available form and adapter tests passed,
  with two database-backed population tests excluded because grants-db was
  unavailable. Public fork PR #4 is merged.
superbee_progress_status: done
superbee_updated_by: mikec-ai
generated:
  by: 'process:superbee'
  at: '2026-08-22T16:13:21.968Z'
---


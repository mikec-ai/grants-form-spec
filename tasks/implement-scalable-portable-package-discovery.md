---
type: Task
title: Replace static demo imports with scalable portable package discovery
priority: P1
description: >-
  Completed in grants-form-workbench PR #3 (merge
  7f69264debfd8c1b0df9f6c0d3e5d11cbe25fc0f). The portal now consumes an
  environment-owned portable-catalog-index/v1 and has no static production form
  imports. The catalog builder discovers all checked-in cohorts, retains
  verified bytes, rejects unsafe locators and output paths, handles races and
  rollback, and serves five forms without application changes. Catalog freshness
  and standalone HTTP receipts were verified.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T04:14:59.660Z'
assignee: Codex-discovery-agent
---
[depends on](close-workbench-multi-form-proof.md)

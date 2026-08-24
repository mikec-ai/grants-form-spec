---
type: Task
title: Design and enforce the parity-delta ledger contract
priority: P0
assignee: parity_delta_contract
description: >-
  Define the portable declarative delta record, validate evidence/review state
  and exact targets, reject stale or blanket allowances, and wire the consumer
  comparator without adapter control flow.
superbee_progress_status: in_progress
superbee_updated_by: parity_delta_contract
generated:
  by: 'process:superbee'
  at: '2026-08-24T18:59:13.218Z'
---
Producer contract merged through PR #84 at 5a374664e100551e900b041866f56ca0fe86af28. The ledger contains 50 atomic targets: all remain proposed; 16 have verified source support and 34 remain unverified. Consumer PR #79 consumes the ledger through the digest-pinned artifact promotion path and reports 1 exact-parity gate pass, 6 mechanically bounded proposed gate blocks, and 0 unexplained failures. Final steps: merge consumer PR after checks, then correct the proof-package claim and reconcile durable board language.

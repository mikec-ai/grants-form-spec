---
type: Task
title: Design and enforce the parity-delta ledger contract
priority: P0
assignee: parity_delta_contract
description: >-
  Define the portable declarative delta record, validate evidence/review state
  and exact targets, reject stale or blanket allowances, and wire the consumer
  comparator without adapter control flow.
superbee_progress_status: done
superbee_updated_by: parity_delta_contract
generated:
  by: 'process:superbee'
  at: '2026-08-24T19:23:23.766Z'
---
Producer PRs 82 through 85 define and harden the portable parity-delta ledger through merge `2a316a832a343f3830c4b6a8948fd746c3dd8c56`. Consumer PR 79 merged at `29fafef5c1f1032b559b519d73387475932297fd` and consumes the exact producer pin generically. The ledger has 50 exact targets: 16 source-verified, 34 unverified, all 50 proposed, and 0 accepted. One form passes because all supported dimensions match exactly; six forms remain blocked because their mechanically bounded differences are proposed and unaccepted; zero unexplained failures remain. Schema validation, offline evidence receipt joins, stale and unused entry detection, and the independent decision-artifact boundary all fail closed. Producer PR 86 merged at `884936fe89f95757ce9435eabf73757144252709` and corrects the public proof-package claim to these governed results.

Post-merge consumer PR 80 merged at `eb15d0fa87b8f5ee2764e51f9bf4b8a2d8b08bf9` and applies the repository's exact isort and Black output to the PR 79 files. This is a mechanical formatter correction with no behavioral change. The full local isort and Black checks, 26 focused tests, Ruff, mypy, and diff check pass.

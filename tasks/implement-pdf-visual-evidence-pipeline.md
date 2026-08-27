---
type: Task
title: Implement PDF visual evidence pipeline
priority: P0
assignee: Codex
description: >-
  Create a form-neutral design-time pipeline that pins official PDFs, renders
  and hashes every page, extracts page text, requires complete agent
  visual-review observations, reconciles those observations to existing exact
  field and behavior evidence without accepting mappings, and exposes
  page-referenced evidence in human review packets. Pilot it with the official
  PHS Additional Indirect Costs sample and read-only PDFs; keep unavailable
  instructions as an explicit gap.
superbee_progress_status: done
superbee_updated_by: Codex
generated:
  by: 'process:superbee'
  at: '2026-08-27T17:44:50.631Z'
---
[depends on](redesign-agent-review-packets.md)

## Outcome

Implemented and merged a reusable, page-complete PDF visual evidence pipeline in `mikec-ai/grants-form-workbench` PR #32. The design-time tool pins official PDF URLs and SHA-256 receipts, renders and hashes every page, extracts page and positioned text, requires every page to be reviewed or explicitly unavailable, binds proposed visual observations to exact review-overlay decisions, rejects form/evidence drift, and embeds verified page images in the standalone human review packet. No PDF-derived observation is automatically accepted or added to runtime packages.

## PHS Additional Indirect Costs pilot

- Official read-only PDF: both pages visually reviewed.
- Official sample PDF: one XFA shell page explicitly unavailable because standard rendering exposes only the Adobe Reader compatibility message.
- 9 proposed page observations, 0 conflicts, and 4 explicit gaps.
- Missing form-specific instructions, invisible calculation formulas/read-only state, and dynamic repetition controls remain unable to verify.
- Refreshed decision packet: `/Users/michaelcollier/Documents/ChatGPT/Smarter-grants-management/deliverables/phs-additional-indirect-costs-review.html`.

## Receipts

- PR: https://github.com/mikec-ai/grants-form-workbench/pull/32
- Merge commit: `9c07bf6b228f6578daf1c557efa4057e9448f3c0`
- Implementation commit: `2408f64bbe7a385299dcfa6744f7047a87cb458b`
- PDF review SHA-256: `2843ca59e3b44c5150e84cc257934cd2ea6a3c598da6738505d84eb3afac5015`
- Packet SHA-256: `690f4ae2677a27d6ee2ff95a46fcdf75b1c60f960a5f6a60b3ce2f7f55331776`
- Verification: typecheck and build passed; initial full suite passed 340 tests with 1 skipped; agent-tool suite passed 65 tests; browser inspection confirmed embedded evidence beside the human calculation decision. A later full parallel run had one unrelated existing 5-second UI timeout, which passed alone in 2.48 seconds. GitHub CI failed before executing any steps and produced no logs, consistent with the account-level Actions condition.

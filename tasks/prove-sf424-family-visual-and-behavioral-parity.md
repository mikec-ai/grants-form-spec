---
type: Task
title: Prove SF-424 family visual and behavioral parity
priority: P0
assignee: codex-root
description: >-
  SF-424 portable browser canary is delivered in fork PR 71. Current claimed
  increment: add a deterministic Playwright recording that compares the existing
  and portable SF-424 through the real Simpler frontend, publishes generated
  media and a pinned receipt outside git, and becomes reusable for SF-424 Short
  and SF-424A.
superbee_progress_status: in_progress
superbee_updated_by: codex-root
generated:
  by: 'process:superbee'
  at: '2026-08-24T13:56:32.075Z'
---
# Goal

Produce deep, reviewable compatibility evidence for SF-424, SF-424 Short, and SF-424A through the real Simpler runtime.

# Scope

- Render each portable and existing implementation side by side using the lower-environment preview seam.
- Compare applicant-visible fields, ordering, grouping, labels, instructions, navigation, conditional presentation, locked state, and print state.
- Run the same representative payload corpus through both schemas and runtime rule processors.
- Compare validation verdicts, calculations, prepopulation behavior, save/reload behavior, and representative XML output where applicable.
- Classify each observed difference as parity, evidence-backed intentional departure, unresolved review item, or defect.

# Acceptance criteria

- Each form has a pinned producer revision, consumer revision, payload corpus, automated receipt, and manual visual receipt.
- SF-424 and SF-424A receive the deepest coverage because they exercise broad application and budget behavior; SF-424 Short explicitly proves reuse across a close sibling.
- Screenshots or a short recording show how to reproduce the side-by-side comparison.
- No claim of pixel or behavioral parity is made beyond the evidence actually obtained.
- Any portable correction remains declarative or generic; no form-specific adapter branch is introduced.

# Boundary

Existing behavior is a compatibility oracle rather than semantic authority. Source-supported intentional differences remain explicit and require review before production cutover.

[depends on](reconcile-sf424-family-portable-cutover-deltas.md)

[depends on](add-portable-form-preview-registration.md)

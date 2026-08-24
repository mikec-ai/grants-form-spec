---
type: Task
title: Prove SF-424 family visual and behavioral parity
priority: P0
assignee: codex-root
description: >-
  SF-424 portable browser canary and a deterministic side-by-side recording are
  delivered in fork PR 71. The recording compares the existing and portable
  SF-424 through the real Simpler frontend, keeps generated evidence outside
  git, and provides a reusable pattern for SF-424 Short and SF-424A.
superbee_progress_status: in_progress
superbee_updated_by: codex-sf424-video
generated:
  by: 'process:superbee'
  at: '2026-08-24T14:38:32.427Z'
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

# Delivered increment: SF-424 comparison recording

- Fork PR 71 head: `3890fd8fe036f2382e6af5823ab148c627aef122`
- Producer revision: `4e69e3fb25f8ee9554ee5e40ad84348ec99599dc`
- A gated Playwright scenario creates separate existing and portable applications through the real Simpler frontend, then records synchronized render, conditional interaction, incomplete-payload validation, save/reload persistence, and print checkpoints.
- `ffmpeg` combines the two browser recordings into a labeled 1920x1080 MP4. The verified local run completed in 59.6 seconds; the generated video is 28.92 seconds.
- The pinned JSON receipt and generated media remain under ignored `frontend/test-results/portable-comparison/` and are not checked into either repository.
- Visual inspection confirmed readable synchronized form, validation, persisted-state, and print-view frames.
- This evidence does not establish semantic acceptance, accessibility approval, policy approval, or production registration.

[depends on](reconcile-sf424-family-portable-cutover-deltas.md)

[depends on](add-portable-form-preview-registration.md)

---
type: Task
title: Close PHS 398 Research Plan technical gates
priority: P0
assignee: codex_phs398_research_plan_closure
description: >-
  Add dedicated consumer/API lifecycle, exact XML/XSD, and bounded four-browser
  evidence without changing shared runtime or fabricating cross-form semantics.
superbee_progress_status: in_progress
superbee_updated_by: codex_phs398_research_plan_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:18:46.585Z'
---
# Goal

Close the PHS 398 Research Plan technical handoff gates in the private Simpler fork using the already-merged generic attachment mechanism.

# Fixed scope

- Add dedicated consumer/API lifecycle and exact XML/XSD coverage for `phs398-research-plan`.
- Run a bounded four-browser portable catalog receipt for Apply, save/reload, attachment persistence, accessibility, and print.
- Preserve the applicant Appendix cap of 10 even though the official XSD container permits 100.
- Preserve Introduction, renewal-publication-list, and vertebrate-animal requirements as explicit unresolved cross-form gates; do not fabricate local response paths or semantic equivalence.
- Add no form-specific compiler, adapter, renderer, or production registration branch.
- Do not touch NIFA, shared Boolean mapping, or read-only ancestry files.

# Coordination boundary

This technical closure builds on the merged producer and banking tasks and the merged generic attachment-persistence fix. Human semantic, policy, instruction, accessibility approval, production registration, and release approval remain separate gates.

# Evidence to record

- Exact producer and consumer revisions.
- Dedicated API and XML/XSD test results.
- Four-browser bounded receipt URL and per-browser outcome.
- Any unresolved or not-applicable cross-form behavior.
- Confirmation that production registration is unchanged.

[depends on](author-integrate-phs398-research-plan.md)

[depends on](bank-phs398-research-plan-in-sgg.md)

[depends on](close-attachment-form-release-gates.md)

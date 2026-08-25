---
type: Task
title: Close PHS 398 Research Plan technical gates
priority: P0
assignee: codex_phs398_research_plan_closure
description: >-
  Add dedicated consumer/API lifecycle, exact XML/XSD, and bounded four-browser
  evidence without changing shared runtime or fabricating cross-form semantics.
superbee_progress_status: done
superbee_updated_by: codex_phs398_research_plan_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:58:08.863Z'
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

# Evidence recorded

- Consumer PR: https://github.com/mikec-ai/simpler-grants-gov/pull/123.
- Final reviewed head: `67e0108aadfe31b76536d1398e2350b715523c92`; merged private-main revision: `68ac65ab1d7a4874ad517eae92536c61b899938e`.
- Dedicated API/browser-plan evidence: 35 focused tests passed locally; isort and Ruff passed. Independent re-review was clean.
- All 12 scalar attachment roles plus 10 Appendix items execute through the shared attachment validator, generic submit lifecycle, generic XML generation, exact element/filename assertions, and the pinned official XSD.
- The applicant schema pins `maxItems: 10`; the hashed official form and Attachments XSDs structurally prove `AttachmentGroupMin0Max100DataType` and `maxOccurs: 100`.
- The ordered nine-source XSD/DAT/PDF/instructions URI and digest set plus the exact crosswalk extraction receipt are asserted.
- Four-browser bounded run: https://github.com/mikec-ai/simpler-grants-gov/actions/runs/32879527396. Chrome, Firefox, Mobile Chrome, and WebKit all passed preview registration, adapter preflight, render, save/reload, accessibility, and print. Each recorded only the known attachment harness timeout as `harness_inconclusive`, with no failed form request and no page error; offline execution closes the attributable attachment validation/XML/XSD boundary.
- No shared runtime, adapter, compiler, renderer, registration, Boolean, read-only, or NIFA file changed. Production registration remains unchanged.
- Introduction eligibility, renewal-publication-list eligibility, vertebrate-animal cross-form requirements, semantic acceptance, policy/instruction review, assistive-technology review, UAT, registration, and release approval remain open outside this technical task.

[depends on](author-integrate-phs398-research-plan.md)

[depends on](bank-phs398-research-plan-in-sgg.md)

[depends on](close-attachment-form-release-gates.md)

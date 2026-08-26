---
type: Reference
title: Agent form-usability protocol
description: >-
  Claimable manual agent-use loop from exact form build through shared-fix
  verification.
superbee_updated_by: codex
---
# Purpose

Use this loop to learn whether an applicant can understand and complete a form in the real Simpler
interface. It complements automated artifact, adapter, XML/XSD, browser-conformance, and
accessibility checks; it does not replace them or convert their passes into human-usability claims.

# Operating loop

1. Create one `Form Usability Run` for an exact form, scenario, environment, runtime commit, and
   producer/artifact pin when available.
2. Claim it atomically by setting `progress_status: in_progress` and `assignee` together. Agents
   work on distinct run records so browser work can proceed in parallel without editing the same
   canonical record.
3. Confirm the form loads through the ordinary application route. Record the exact URL only when
   it is safe to preserve; never treat ambient browser state as proof.
4. Execute the scenario as an applicant: read instructions, navigate, enter representative data,
   exercise applicable conditions/repeaters/attachments/calculations, save, reload, recover from
   errors, and inspect the printable result.
5. Preserve concise evidence for each material observation: step, expected behavior, observed
   behavior, stable field/path when available, screenshot or trace reference, browser, and build.
6. Create one `Usability Finding` per reproducible applicant-facing symptom and link the run to it
   with `discovers`. Leave `affected_layer: unknown` until triage supports attribution.
7. Triage findings across forms. Create a `Shared Defect` only when multiple findings or direct
   technical evidence support a common root cause. Link findings with `attributed to`.
8. Create or link an ordinary `Task` for the reusable fix and connect the defect with
   `implemented by`. File an issue only in the private fork, and only after triage makes the scope
   actionable.
9. Mark a merged defect `fixed`; schedule a later run with `verifies`. Only that later manual run
   may mark the shared defect `verified`.

# Execution topology

The primary agent owns the desktop in-app-browser lane. Browser runs are serial because delegated
subagents do not inherit control of that desktop browser session. Do not delegate a browser run and
then record its inability to access the browser as a product result.

Parallel agents remain useful for bounded work around an observed run: preparing source-backed
scenarios, inspecting exact artifacts, clustering findings, diagnosing reusable fixes, adding tests,
and reviewing evidence. Introduce that parallel work after the primary browser observation exists;
do not spend coordination effort merely to duplicate the scarce browser lane.

# Required scenario coverage

Every scenario must name its applicant goal and declare which of these are applicable: orientation
and instructions, navigation, data entry, requiredness and validation, conditional behavior,
repeaters, attachments, calculations/read-only output, save/reload, error recovery, keyboard use,
and print/review. Mark capabilities not applicable with evidence; do not silently skip them.

# Result rules

- `pass`: the goal was completed without a material finding.
- `pass_with_findings`: the goal was completed, but one or more material findings were recorded.
- `fail`: the applicant goal could not be completed because of a product or content problem.
- `inconclusive`: environment, authentication, unavailable evidence, or harness problems prevented
  a defensible result. Inconclusive never counts as a pass.

# Portfolio views

The live `Form usability loop` View shows the claimable queue, open findings, and shared defects.
Prioritize defects by demonstrated cross-form impact and severity, not by the number of speculative
forms that might be affected. Keep exact source/version provenance and agent-proposed semantic
interpretations separate; only reviewed mappings contribute to published coverage metrics.

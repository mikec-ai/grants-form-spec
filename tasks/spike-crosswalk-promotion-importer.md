---
type: Task
title: Spike reusable crosswalk-to-form-spec promotion importer
priority: P0
assignee: codex
description: >-
  Design and prove a reusable, review-gated development-time promotion path from
  crosswalk evidence into grants-form-spec staging artifacts, using Performance
  Site as the spike form.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-22T19:26:46.757Z'
---
# Objective

Build a reusable, design-time promotion protocol between `grants-question-crosswalk` and `grants-form-spec`, using Project/Performance Site Location(s) as the proving form. The crosswalk should export neutral, source-pinned evidence; `grants-form-spec` should own the importer that creates reviewable draft authoring material. There must be no runtime dependency between the repositories.

# Hypothesis

Deterministic extraction and provenance already present in the crosswalk can eliminate repeated source discovery, transcription, constraint reconstruction, XML-path bookkeeping, and fixture setup. Semantic identity and reusable-component decisions must remain explicit review gates.

# Spike outputs

- A versioned, output-neutral promotion-packet contract.
- A deterministic crosswalk export for Performance Site containing source identity, hashes, XSD paths and types, cardinality, constraints, classifications, extracted behaviors, candidate mappings, conflicts, and review status.
- A `grants-form-spec` design-time importer that produces staging-only evidence and TypeSpec scaffolding from that packet.
- Proposed references to existing questions clearly separated from accepted semantic mappings.
- XML-projection and parity-fixture scaffolding where deterministic evidence supports it.
- A short findings report measuring generated coverage, remaining manual decisions, edits required to compile, and whether the approach should be used for R&R SF-424.

# Guardrails

- Preserve exact source and version provenance for every promoted record.
- Never treat similar labels, paths, types, or shapes as proof of semantic equivalence.
- Generated semantic mappings remain proposed until reviewed; they do not contribute to published coverage.
- Do not generate canonical question identities automatically.
- Do not add a production or runtime dependency on the research repository.
- Do not add form-specific compiler or adapter branches.
- Keep applicant questions, calculated outputs, technical fields, static content, attachments, and capture mechanisms distinct.

# Acceptance criteria

- The same pinned Performance Site inputs reproduce the same promotion packet and staging output.
- Every generated field or behavior links back to its source evidence and review state.
- The importer fails closed on unsupported or conflicting evidence and reports actionable review gates.
- Generated staging material can be reviewed and promoted into a compiling form specification without manual retranscription of deterministic facts.
- Existing producer preflight remains green.
- Findings state whether the reusable importer saves enough effort to apply to R&R SF-424 and subsequent forms.

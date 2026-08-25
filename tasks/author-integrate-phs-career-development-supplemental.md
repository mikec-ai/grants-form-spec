---
type: Task
title: Author and integrate PHS Career Development Supplemental
priority: P2
assignee: root_phs_career
description: >-
  Create the currently absent Career Development Supplemental through
  source-evidenced composition of proven PHS capabilities.
superbee_progress_status: done
superbee_updated_by: root_phs_career
generated:
  by: 'process:superbee'
  at: '2026-08-25T05:55:54.581Z'
---
# Goal

Author PHS 398 Career Development Award Supplemental as a source-evidenced portable form after the current foundation work, composing existing PHS capabilities only where their semantic meaning is supported.

# Verified starting state

The form is absent from the current 39-form producer catalog and consumer bank. No completion or partial implementation is claimed on this board.

# Acceptance criteria

- Pin exact official XSD, DAT, PDF/XFA, instruction, and applicable policy sources with versions and digests.
- Keep deterministic extraction separate from proposed semantic mappings.
- Evaluate reuse of people, organizations, research, attachment, budget, human-subjects, and policy concepts without treating similar labels or paths as equivalence.
- Compile through the generic producer and Simpler adapter with no form-specific compiler or adapter branch.
- Prove schema/UI/rules, representative XML/XSD, and applicable lifecycle behavior.
- Bank the immutable package without implying registration, accessibility approval, policy acceptance, or production release.
- Record genuinely new capabilities and marginal implementation effort.

# Completion evidence

- Producer PR 103 merged as `a19b2dd2bd93bc195c1be0af808a0bc13504b65f`.
- Consumer banking PR 109 merged as `b2078013c9d8696e59a954bb46795ec9ee491ff0`.
- Consumer canary PR 110 merged as `a886ebb90fbec5d792d268e1c0d977febcdca9e0`.
- Exact source set pins FID 799 version 6.0 XSD, DAT, read-only PDF, XFA PDF, and NIH Forms I career instructions.
- The form composes 12 proposed research-plan identities and adds 8 portable semantic question blocks. Proposed mappings remain excluded from published coverage.
- The generic producer emits 20 top-level prompts and 22 leaf response fields. Two source-local citizenship conditions compile; three application-package conditions remain explicitly source-bound and uncompiled.
- Producer full preflight passed: 125 TypeSpec tests, 361 Python tests with 10 skips, exact-XSD and artifact validation, classification gates, and packaging.
- The Simpler fork now banks 41 portable forms and 520 selected artifacts. Registration remains unchanged.
- Focused consumer verification passed 30 tests and proves generic loading, browser capability discovery, conditional projection, and exact-XSD-valid XML without form-specific adapter code.

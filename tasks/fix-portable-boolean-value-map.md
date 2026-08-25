---
type: Task
title: Fix portable boolean XML value-map canonicalization
priority: P1
assignee: codex_nifa_closure
description: >-
  Repair the generic XML mapper so typed booleans match JSON-canonical portable
  value-map keys without changing non-boolean semantics.
superbee_progress_status: done
superbee_updated_by: codex_nifa_closure
generated:
  by: 'process:superbee'
  at: '2026-08-25T17:37:54.434Z'
---
# Goal

Make the generic XML `map_values` transformer honor JSON-canonical boolean keys so typed portable-form boolean responses can reach exact Grants.gov XML.

# Defect evidence

- NIFA Supplemental provides typed Python booleans from its JSON Schema.
- Its portable XML profile correctly serializes the value map keys as `true` and `false`.
- The generic transformer currently uses `str(value)`, producing `True` and `False`, and fails closed with `Value 'True' not found in mappings`.

# Fixed scope

- Canonicalize only Python `bool` lookup values to JSON lowercase `true`/`false`.
- Preserve every existing non-boolean mapping lookup and failure behavior.
- Add focused positive and negative unit regressions.
- Prove the repair end to end with representative NIFA XML against the exact pinned official XSD.
- Add no form-specific transformer or adapter branch.

# Open gates

This generic defect repair does not accept NIFA semantic mappings, register the form, or close any human semantic, visual, accessibility, agency, instruction, privacy/security, policy, operational, UAT, or release gate.

## Closure receipt

Merged private-fork PR #121 as `cfb57f79915b50980f9d11f880dbf87dac78e7ef`. Focused transformer regressions preserve legacy and non-boolean behavior, and representative NIFA `true` and `false` XML validates against the exact pinned official XSD.

---
type: Context Note
title: Portable Grants.gov XML progress and 10-year XSD hash discrepancy
timestamp: '2026-08-24T01:01:08Z'
description: >-
  Historical architecture handoff with the completed merge receipt and the
  still-preserved R&R Budget 10-year XSD provenance discrepancy.
tags:
  - architecture
  - grants-gov-xml
  - provenance
  - handoff
superbee_updated_by: codex
---
# Summary

The portable Grants.gov XML work now follows the intended shared-kernel architecture. `grants-form-spec` owns declarative form-to-wire semantics as an optional target profile, while `simpler-grants-gov` owns only generic artifact loading, legacy-name projection, and XML runtime execution. The two implementation PRs are clean and mergeable; merge the producer before the consumer.

## Architectural decision

- Canonical questions and response shapes remain portable JSON Schema and TypeSpec definitions.
- `targets/grants-gov-xml/` owns the target-specific root element, namespaces, XSD identity, static attributes, and canonical response-to-XML mapping.
- One authored `research-budget-3.0.json` mapping is shared by five thin R&R Budget family profiles. Emitted consumer artifacts are self-contained snapshots, not five independently maintained mappings.
- The SGG adapter owns canonical camelCase-to-legacy field projection and translation of four portable node kinds (`value`, `object`, `array`, and `attachment`) into its existing XML runtime vocabulary.
- The SGG adapter contains no form-name list and no five-year, ten-year, budget, or subaward branching. Budget-specific Python mapping modules were deleted.
- The profile contract now rejects ambiguous nodes that mix incompatible object and array properties.

## Completed merge receipt

- Producer PR [#21](https://github.com/mikec-ai/grants-form-spec/pull/21), reviewed at head `efb956c94fa72451255a7411a130fe9d62dac940`, merged as `fe8461f944394d604e5644fe029ccb3474498af0` on 2026-08-22.
- Consumer PR [#15](https://github.com/mikec-ai/simpler-grants-gov/pull/15), reviewed at head `98b51cd83f15d55532e2410da291f8039fadc0e7`, merged as `e2510ac9df1aeaabab5e3e534cde1384d696bac1` on 2026-08-22.
- Producer preflight passes after synchronization with current `main`: 64 TypeScript tests, 35 Python tests with 3 existing skips, 84 canonical blocks, and 485 emitted artifacts.
- Consumer verification passes: 99 focused portable-adapter and budget-family tests, Ruff, and mypy.
- All five budget-family profiles emit maximal XML that validates against the pinned official Grants.gov XSDs.

## Ten-year XSD hash discrepancy

The standalone R&R Budget 10-year evidence sidecar currently records:

- URI: `https://apply07.grants.gov/apply/forms/schemas/RR_Budget10_3_0-V3.0.xsd`
- SHA-256: `cccce03554424d59b5958e4443a54db12a5a10780fbdc5df2ec25955d443fc9d`
- Extraction revision: `dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef`
- Extracted at: `2026-08-18T19:43:18.348859Z`

The currently served official XSD, the 10-year subaward evidence, the portable target profile, and the SGG-pinned XSD instead use:

- SHA-256: `e9d004c15ffcbae04b65087cb0eff7e87b8eb8ba0ffd6bfb6aba5542e04708cc`

Do not silently replace the older evidence hash. It may identify an earlier upstream byte representation and is tied to a specific extraction run. The portable profile deliberately pins the currently served and XSD-tested hash. A separate provenance reconciliation should retrieve or locate the older bytes, determine whether Grants.gov changed the file or the extraction normalized it, and record the result as timestamped evidence rather than overwriting history.

## Remaining provenance action

The hash discrepancy was non-blocking for the merged PRs because the runtime contract is pinned and validated, but it remains an explicit provenance follow-up.

[supports](../decisions/canonical-form-architecture.md)

[informs](../tasks/harden-rr-budget-production.md)

[informs](../tasks/author-integrate-rr-budget.md)

# Grants Form Spec

A portable, declarative question bank and form composition system for grants applications.

The project defines reusable semantic questions, composes them recursively into forms, and emits standard JSON Schema plus separate presentation and behavior artifacts. The emitted artifact graph is the contract. TypeSpec is the first typed authoring tool, but consumers do not depend on TypeSpec or its compiler model.

## Current proof

The repository currently includes 33 reference forms, spanning:

- Key Contacts
- SF-424
- SF-424A
- SF-424 Short
- Project Narrative Attachment
- Budget Narrative Attachment
- Other Narrative Attachments
- R&R Budget 3.0
- R&R Budget 10YR 3.0
- R&R Subaward Budget 3.0
- R&R Subaward Budget 5 YR 30 ATT 3.0
- R&R Subaward Budget 10YR/30
- Project Abstract Summary
- R&R SF-424 and Multi-Project Cover
- R&R Senior/Key Person Profile (Expanded)
- Project/Performance Site Locations
- R&R Other Project Information
- PHS 398 Modular Budget
- PHS Assignment Request
- Attachment Form
- PHS 398 Research Plan
- SF-LLL, CD-511, and Grants.gov Lobbying Form
- the SF-424B and SF-424D profile families
- SF-424C and R&R SF-424B

The reference implementation proves applicant-visible rendering and validation parity against existing implementations. SF-424 Short adds no new questions to the bank and shares 91 percent of its questions with SF-424, demonstrating the intended reuse model.

## Architecture

```text
Question bank + form specifications
                 |
                 v
       producer-neutral artifacts
       schema, UI, rules, indexes
                 |
        +--------+---------+
        |                  |
        v                  v
  Simpler adapter     other consumers
```

Canonical artifacts remain independent of delivery targets. Consumer-specific projections,
legacy field names, and runtime rule mappings belong in consumer adapters. Optional portable
wire targets are isolated under `targets/` and may be ignored by consumers that do not need
them.

Read the [architecture](documentation/architecture.md), [worked authoring model](documentation/authoring-model.md), [delivery-target runtime identity boundary](documentation/runtime-target-identity.md), [attachment semantics](documentation/attachment-semantics.md), [form analysis export](documentation/analysis-export.md), [Grants.gov XML target](documentation/grants-gov-xml-target.md), and [deferred design boundaries](documentation/deferred-designs.md) before changing the contract.

The [PHS 398 Research Plan status](documentation/phs398-research-plan-status.md) records how thirteen
semantic attachment roles reuse one capture mechanism while preserving cross-form applicability and
the Appendix 10-versus-100 source boundary.

The [lifecycle field ownership decision](documentation/lifecycle-field-ownership.md) records why
externally assigned values, attestations, and workflow controls do not automatically become
semantic questions.

## Development

Requirements:

- Node.js 22
- Python 3.11 or newer for analysis scripts

```shell
npm ci
npm run preflight
```

Useful commands:

```shell
npm run build
npm run emit
npm test
npm run analyze
python3 scripts/analyze.py --json --output-dir build/analysis
npm run check-classified-fields
```

`npm run validate-artifacts` validates emitted questions, forms, presentation trees,
catalogue indexes, and package manifests against `contract/v1`. It also checks the artifact
graph for resolvable `$ref` targets, valid UI scopes, matching block identities, and declared
package members. The same command accepts artifacts produced without TypeSpec through
`--dist <path>`.

Source evidence is authored as a separate sidecar under `evidence/` and projected beside its
block with `npm run project-evidence`. Each record pins public source URIs, versions, hashes,
and deterministic extraction provenance. Semantic mappings carry an explicit review state;
unreviewed or proposed mappings are never eligible for published coverage metrics.

Every emitted form index includes path-qualified canonical field lineage and explicitly authored
response roles. CI requires zero fields without canonical question lineage or a declared
non-question role. Any temporary exception must carry evidence, an owner, a reason, and a bounded
removal condition; see [the classified form-field gate](documentation/classified-form-field-gate.md).

The [SF-424 cover cluster note](documentation/sf424-cover-question-clusters.md) records the
conservative 50-occurrence partition, source boundary, and unpublished review status.

Generated `dist/` output is intentionally ignored. Build reports, large parity oracles, resolved snapshots, and analysis workbooks are CI artifacts rather than runtime source.

## Project boundaries

This repository owns the portable question bank, form definitions, artifact contracts, compiler checks, and implementation-derived reuse analysis. It does not own the Simpler.Grants.gov runtime or CommonGrants.

The project was extracted from [Billy Daly's declarative form authoring proposal](https://github.com/mikec-ai/simpler-grants-form-runtime/pull/44). The filtered Git history preserves the authorship of that work.

## Status

This is an active architectural prototype. Semantic mappings remain proposed until reviewed. Similar wording or validation shape is never treated as proof that two questions have the same meaning.

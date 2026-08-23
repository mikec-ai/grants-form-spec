---
type: Task
title: Factor reusable Grants.gov XML mapping fragments
priority: P1
description: >-
  Use the existing JSON reference resolver to remove repeated, source-identical
  wire mappings.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T15:34:46.627Z'
assignee: rr_budget_semantic_review
---
# Goal

Factor repeated Grants.gov XML mapping structures into reusable JSON fragments using the target projector's existing relative `$ref` and JSON Pointer support.

# Acceptance criteria

- Extract only source-identical structures supported by exact path, type, namespace, and version evidence; similar labels do not establish reuse.
- Start with the repeated person-name, address, organization/contact, and attachment structures in the R&R SF-424 and research-budget mappings.
- Resolved XML target profiles remain byte-equivalent where ordering is contractual, or semantically equivalent with an explicit reviewed diff where serialization order is not contractual.
- XSD validation and all target-profile tests remain green.
- Record the reduction in duplicated mapping entries and identify which forthcoming forms can consume each fragment.

# Design constraint

Use the existing target-local `$ref` mechanism. Do not move Grants.gov wire semantics into the canonical question bank or add form-specific projector code.

# Result

Merged as `mikec-ai/grants-form-spec` PR #32 at commit `b992a9ee9c5811ef565f3b0cecaf72f53d5ce08c` after independent source/provenance review. Three exact `HumanNameDataType` occurrences and four exact `AddressDataTypeV3` occurrences now use target-local JSON references, eliminating 34 duplicate mapping nodes while keeping resolved R&R SF-424 output byte-identical. Non-identical contact, organization, budget-name, and attachment structures were deliberately left separate. Native-source version normalization remains the separate `normalize-native-source-version-provenance` task.

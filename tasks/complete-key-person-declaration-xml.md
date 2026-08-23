---
type: Task
title: Complete Key Person declaration and XML target
priority: P0
assignee: key_person_xml_agent
description: >-
  Correct pinned DAT behaviors and author the source-bound Grants.gov XML/XSD
  target for R&R Key Person Expanded.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:38:55.380Z'
---
---
type: Task
title: Complete Key Person declaration and XML target
priority: P0
assignee: key_person_xml_agent
description: >-
  Correct pinned DAT behaviors and author the source-bound Grants.gov XML/XSD target
  for R&R Key Person Expanded.
superbee_progress_status: in_progress
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T16:06:54.785Z'
---
# Goal

Close source-bound declaration gaps and produce representative official XML for R&R Key Person Expanded.

# Acceptance criteria

- Add DAT-backed US ZIP minimum and PD/PI project-role default with exact evidence references.
- Resolve state/province XML safety without inventing semantics.
- Compose reusable reviewed name, address, attachment, and research-person XML fragments.
- Generate PI, multiple-person, and attachment XML and validate it against pinned RR_KeyPersonExpanded_4_0-V4.0.xsd.
- Add tests and preserve semantic review gates.

# Boundary

Do not implement overflow attachment boolean gating here and do not enable production registration.

# Result

Delivered and merged in mikec-ai/grants-form-spec PR #38, merge commit 46e71d58516f3c5250702b1de30d8fc27e9ed95a.

- DAT-backed US ZIP minimum and PD/PI default are declared with exact source evidence.
- Reusable Global Library name/address and attachment fragments are composed with one new research-person profile.
- A narrow leaf-only container mapping models the official per-person attachment wrappers without a form branch.
- Parsed XML assertions prove one PI, two repeated people, nested bio/support attachments, all three overflow wrappers, exact element order, namespaces, attributes, and data before mandatory XSD validation.
- Exact pinned XSD validation passes and rejects simultaneous State plus Province.
- Full preflight and CI passed: 79 TypeScript tests, 67 Python tests, 118 blocks, and 660 artifacts.

The new semantic mappings remain proposed/source-bound-unreviewed. State/Province stale-value safety and human semantic acceptance remain explicit consumer/release gates. Production registration is disabled. The separate SGG projection task owns consumer integration.

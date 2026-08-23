---
type: Task
title: Author and integrate Project/Performance Site Locations
priority: P1
assignee: codex
description: >-
  Use the deterministic promotion spike to author the next high-value repeating
  organization and location foundation, then prove it through the public Simpler
  adapter without form-specific runtime code.
superbee_progress_status: done
superbee_updated_by: codex
generated:
  by: 'process:superbee'
  at: '2026-08-23T00:17:37.835Z'
---
# Objective

Author Project/Performance Site Location(s) from pinned deterministic evidence as a reusable repeating organization and location foundation.

# Completed result

- Producer PR #25 added the declarative form and project-site question block.
- Adapter PR #22 pinned integrated producer revision 82bf2bf016eff4ea2320298eb29a6039aaa5d55a and proved the form loads without form-specific adapter code.
- The form composes one primary site, up to 299 additional sites, and one overflow attachment.
- It emits 25 fields and four typed address conditions; repeated-site conditions use item scope and row-relative pointers.
- The overflow attachment is explicitly a capture mechanism rather than a semantic question.
- Deterministic evidence is pinned to crosswalk revision 4312f6504b060e2b9ffdbd2307fc41130c3123a0 and source-set hash ba3348472c48a2fac951308c9a8f44fc078c5b014771d7e9d1a4b0521a00d879.
- No semantic mapping is accepted. XML, human semantic review, accessibility, and production release remain explicit gates.

# Validation

The integrated producer preflight passed with 568 artifacts, 66 TypeScript tests, 41 Python tests, and reproducible packaging. The rebased public-fork adapter passed 83 form-spec tests before merge and 21 focused integration, maintenance, XML-profile, lint, and typing checks after restacking.

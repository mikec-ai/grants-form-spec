---
type: Convention
title: Form Usability Run
governs: Form Usability Run
path: usability-runs/
description: >-
  A claimable, evidence-backed attempt by an agent to complete a named applicant
  scenario in one exact form build.
links:
  discovers: Usability Finding
  verifies: Shared Defect
  validates: Task
link_descriptions:
  discovers: A concrete usability finding observed during this run.
  verifies: A previously identified shared defect that this later run retests.
  validates: Implementation work whose outcome this run exercises.
fields:
  required:
    - title
    - superbee_progress_status
    - form_id
    - scenario
    - environment
    - runtime_commit
  optional:
    - assignee
    - producer_commit
    - artifact_manifest_digest
    - browser_scope
    - result
  values:
    superbee_progress_status:
      - queued
      - in_progress
      - complete
      - inconclusive
      - canceled
    result:
      - pass
      - pass_with_findings
      - fail
      - not_run
  terminal:
    superbee_progress_status:
      - complete
      - inconclusive
      - canceled
  descriptions:
    title: A concise label naming the form and applicant scenario.
    superbee_progress_status: >-
      The persisted run lifecycle; complete requires evidence in every required
      body section.
    form_id: The exact portable form identifier under test.
    scenario: 'The named, versioned applicant workflow being attempted.'
    environment: The exact local or lower-environment runtime used for the attempt.
    runtime_commit: The exact consumer runtime commit under test.
    assignee: >-
      The agent currently responsible; claim with an atomic status and assignee
      update.
    producer_commit: The exact producer commit when known.
    artifact_manifest_digest: The exact selected artifact manifest digest when known.
    browser_scope: Browser and viewport coverage for this run.
    result: >-
      Overall result; not_run is valid only before execution or when the run is
      canceled.
sections:
  - Intent
  - Preconditions and provenance
  - Scenario steps
  - Evidence
  - Outcome and follow-up
---
# Form Usability Run

This is manual agent-use evidence, not an automated conformance receipt. A run is claimable work:
one agent owns one form/scenario/build tuple, records exact provenance, executes every declared
step, preserves screenshots or traces, and creates findings without guessing their root cause.

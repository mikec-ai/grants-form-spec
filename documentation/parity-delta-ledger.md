# Parity delta ledger

The parity delta ledger is the portable, declarative source of truth for every observed
difference between a compiled form and an existing Simpler form. It does not make the Simpler
adapter decide whether a difference is acceptable.

Each record binds one exact comparator key to a stable semantic target in the emitted form
artifacts. A positional UI key therefore also names the canonical field or stable UI section it
affects. Blanket form-level allowances are invalid. The producer validates every semantic target
after compilation and rejects duplicate targets.

Comparison evidence and semantic source support are separate. The checked-in verification receipt
records the SHA-256 digest of each consumer file at one pinned consumer revision, so ordinary builds
fail closed without fetching another repository. Source support remains `unverified`, `partial`, or
`verified` independently of whether the differential harness observed the key.

Review is also explicit. Proposed records are not accepted differences. An accepted record requires
an accountable reviewer, review timestamp, and durable decision evidence. Unresolved mismatches are
classified separately and cannot be accepted.

Classification and source support describe what evidence currently says; neither is acceptance.
For example, an `authoritative_source_correction` with verified source support still remains proposed
until its review record is accepted. Rule-path targets are reserved by the schema but fail validation
until the compiler can resolve them exactly against emitted rule artifacts.

Consumers vendor the exact producer ledger, pin its producer revision and SHA-256 digest, and use a
generic comparator to join observed `(formId, dimension, differenceKey)` tuples to ledger records.
Unexpected observations, unused records, absent semantic targets, unreviewed proposals, and
unresolved mismatches remain visible and fail the comparison gate.

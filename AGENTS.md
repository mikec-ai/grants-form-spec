# Working agreement

- Preserve exact source and version provenance for every extracted record.
- Never treat similar wording or validation shape as proof of semantic equivalence.
- Keep deterministic extraction separate from agent-proposed semantic mappings.
- Only reviewed mappings contribute to published coverage metrics.
- Treat the emitted artifact graph as the contract. Consumers must not depend on a TypeSpec AST.
- Keep canonical question and form artifacts independent of Simpler or any other target.
- Put consumer-specific legacy projections and rule names in consumer adapters. Keep optional
  wire targets outside canonical form artifacts; portable Grants.gov XML profiles live under
  `targets/` and consumers provide only generic execution.
- Add or update tests with every behavior change.

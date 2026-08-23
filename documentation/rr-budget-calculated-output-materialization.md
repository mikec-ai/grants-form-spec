# R&R Budget calculated-output materialization

## Decision

R&R Budget calculations whose authoritative DAT rule says the output is required only when source
data is entered use `@Validation.materializeWhenAnySourcePresent`.

- If every declared source value is absent or null, the calculated output remains absent. A stale
  calculated value is removed.
- An explicitly entered numeric zero is present, so the calculated output is materialized as zero.
- Calculations without this annotation retain the target runtime's existing behavior.

This annotation controls materialization only. It does not infer requiredness, change a formula, or
claim semantic review.

## Source boundary

The decision is bound to the official R&R Budget 3.0 sources already pinned in
`evidence/forms/rr-budget/evidence.json`:

- XSD: `https://apply07.grants.gov/apply/forms/schemas/RR_Budget_3_0-V3.0.xsd`, SHA-256
  `d474010f85819549990de65fc51292bed08ba98ac0895d0dde9513fbe855cdbc`.
- DAT workbook: `https://apply07.grants.gov/apply/forms/sample/RR_Budget_3_0-V3.0_F770.xls`,
  SHA-256 `c85158ce7ddcc756d6e8a55a050e00b4a95cdfc8d9a2d91b7bd94c7f8bdb1035`.

The DAT has 20 calculated fields with a non-empty condition stating that the output is required if
data was entered in the corresponding row, section, budget periods, or cost category. Five of those
rules also state explicitly that the result may equal zero. The declarative annotation is applied to
those 20 fields only. Similar wording elsewhere is not treated as evidence of equivalence.

## Runtime contract

The SGG rule projection emits:

```json
{
  "rule": "sum_monetary",
  "fields": ["@THIS.left", "@THIS.right"],
  "materialize": "when_any_source_present"
}
```

The adapter interprets this generically for monetary sums, integer sums, and subtraction. The policy
works at the form root and inside repeatable subaward contexts without a budget-family branch.

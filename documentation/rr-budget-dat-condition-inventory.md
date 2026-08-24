# R&R Budget DAT condition inventory

This inventory reconciles the exact condition records in the official R&R Budget 3.0 F770 DAT
projection before extending the portable condition vocabulary. It does not use labels or similar
wording to infer behavior, and it does not accept any semantic mapping.

## Count reconciliation

The often-repeated number **56** is the number of calculated DAT behavior records. It is not the
number of non-empty conditions:

| Measure | Exact count |
| --- | ---: |
| All extracted DAT behavior occurrences | 159 |
| Calculated behavior occurrences | 56 |
| Calculated behaviors with non-empty conditions | 20 |
| All non-empty condition occurrences | 64 |
| Unique condition records | 46 |
| Unique condition texts | 27 |

The difference between 64 occurrences and 46 unique records is deterministic array expansion. The
same F-8-1 description rule and F-8-2 funds rule each bind to ten distinct Other Direct Cost paths.
Those 20 path occurrences represent two source records, not twenty independent source decisions.

The machine-readable inventory is
[`analysis/rr-budget-dat-conditions.v1.json`](../analysis/rr-budget-dat-conditions.v1.json). It pins
the DAT URI and SHA-256, the extraction repository and revision, the enriched JSONL digest, every
exact condition string, behavior key, DAT field number, XSD occurrence path, classification, and
unreviewed disposition. Regenerate it from the pinned extraction checkout with:

```shell
python3 scripts/classify_rr_budget_dat_conditions.py \
  --input /path/to/artifacts/proof/grantsgov-RRBudget-enriched.jsonl \
  --out analysis/rr-budget-dat-conditions.v1.json
```

## Current representation

Fifty condition occurrences are already represented without another condition primitive:

- 20 calculated-output presence rules use the existing source-bound materialization declaration;
- 16 Other Personnel row rules use optional row objects whose applicable members are required once
  the row exists; and
- 14 equipment, participant/trainee, and Other Direct Cost pair rules use optional objects with
  required member pairs.

These are implementation dispositions, not accepted semantic mappings.

## Precise unresolved boundary

Ten occurrences of the single F-8-1 cross-section rule now compile through the bounded,
target-neutral `atLeastOnePathWhenPresent` contract. Presence of the Participant/Trainee `Other`
object conditionally requires at least one of the ten exact Other Direct Cost description paths.
The portable emitter expresses this as ordinary JSON Schema `if` plus `then.anyOf`; the rule stays
visible and active, as the source requires, and remains unreviewed for semantic acceptance.

Four occurrences remain source-bound and uncompiled:

- Four attachment/total rules are two bidirectional pairs. Each pair combines presence with a
  strict greater-than-zero comparison over an XSD decimal represented portably as a string. A
  presence-only rule would weaken the source condition, while ordinary numeric JSON Schema keywords
  do not apply to the wire string.
The current portable vocabulary still cannot express that numeric-string boundary exactly. A
presence-only approximation would weaken the official rule. Those four occurrences therefore stay
explicitly unreviewed and uncompiled pending a generic numeric-string comparison contract and
consumer conformance.

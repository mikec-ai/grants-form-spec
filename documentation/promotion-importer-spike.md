# Review-gated crosswalk promotion spike

This spike tests a reusable development-time seam between the research repository and canonical
portable form authoring. It does not create a runtime dependency and it does not let extracted or
agent-proposed identities silently become canonical questions.

## Boundary

`scripts/promote_crosswalk.py export` reads tracked crosswalk artifacts at an explicit Git revision
and produces `grants-form-promotion/v1`. It reads through `git show`, so an agent's uncommitted work
cannot alter a packet pinned to the same revision. The packet preserves deterministic records,
source behavior evidence, proposed runtime rules, component proposals, source hashes, and open
review gates.

`scripts/promote_crosswalk.py import` consumes that neutral packet and writes staging-only material:

- a source-evidence sidecar;
- a TypeSpec source-shape scaffold;
- a semantic and behavior review queue; and
- a measurable import report.

The importer never edits `specs/main.tsp`, never creates canonical question IDs, and records zero
accepted semantic mappings. A human or reviewing agent must reconcile the staging scaffold with the
existing question bank before promotion into canonical authoring.

## Performance Site result

The pinned Performance Site run transcribed all 34 XSD records, preserved all 33 raw behavior
records and nine proposed executable conditions, assembled six exact source identities, and carried
34 component proposals into a review queue. The promotion layer also reconciled a potentially
confusing count: the authoring contract's 25 source behavior records are the 25 applicant-entered
records, while the raw artifact additionally preserves eight presentation records such as headings,
OMB and expiration text, the burden statement, and navigation buttons. These classifications remain
distinct rather than being collapsed or discarded.

This establishes that the reusable seam saves deterministic transcription and provenance work. It
does not establish semantic equivalence, policy correctness, accessibility, runtime parity, or
production readiness. Performance Site remains a spike until its review gates are resolved and its
source scaffold is deliberately composed from accepted question-bank blocks.

## Reproduction

```sh
python3 scripts/promote_crosswalk.py export \
  --crosswalk ../Smarter-grants-management \
  --form PerformanceSite \
  --revision dfe9e47ffd6a25c967b8ed38703480ccdc15a8ef \
  --out build/promotion/PerformanceSite.promotion.json

node scripts/validate_promotion.mjs build/promotion/PerformanceSite.promotion.json

python3 scripts/promote_crosswalk.py import \
  --packet build/promotion/PerformanceSite.promotion.json \
  --out spikes/crosswalk-promotion/performance-site
```

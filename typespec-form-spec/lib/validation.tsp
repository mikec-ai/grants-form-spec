// The JS that implements the `extern dec` declarations below. Imported here rather than
// only from `main.tsp` so that this file type-checks on its own -- an editor opens one
// file, not an entry point, and an unimplemented `extern dec` is an error.
import "../dist/src/index.js";
import "./types.tsp";

using TypeSpec.Reflection;

namespace SimplerForms.Validation;

/** Apply source-specific limits to this use of a reusable question without changing its identity. */
extern dec constraints(target: ModelProperty, patch: valueof ValidationConstraints);

extern dec requiredWhen(target: ModelProperty, source: ModelProperty, equals: valueof unknown);

/** Require a field from a condition on a nested sibling path, relative to the containing model. */
extern dec requiredWhenPath(target: ModelProperty, sourcePath: valueof string, equals: valueof unknown);

/** `operator` rather than `op`: `op` is a TypeSpec keyword and breaks the parser. */
extern dec computed(target: ModelProperty, operator: valueof Op, ...refs: ModelProperty[]);

/**
 * Compute a value from canonical data paths that cross a repeatable boundary.
 *
 * Paths are relative to the reusable block that owns the calculation. `[*]` selects every
 * entry in a list. This is the declarative equivalent of a cross-period total such as
 * `budgetYear[*].travel.totalTravelCost`; a target adapter may translate the spelling but
 * must not reinterpret the relationship.
 */
extern dec computedFrom(target: ModelProperty, operator: valueof Op, ...paths: valueof string[]);

/** Preserve an authoritative calculation's evaluation position when the source defines one. */
extern dec evaluationOrder(target: ModelProperty, order: valueof int32);

/**
 * This block totals the same block found in each of `sources`, field by field.
 *
 * A source is either a repeatable list -- in which case the corresponding block is found
 * inside each entry -- or a peer property holding the same block. Either way one
 * declaration stands for a sum per field, which is what makes a twelve-row budget column
 * one statement rather than twelve.
 */
extern dec totals(target: ModelProperty, ...sources: ModelProperty[]);

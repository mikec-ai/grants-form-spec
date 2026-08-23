// The JS that implements the `extern dec` declaration below. Imported here rather than
// only from `main.tsp` so this file type-checks independently in editors and CI.
import "../dist/src/index.js";
import "./types.tsp";

using TypeSpec.Reflection;

namespace SimplerForms.Response;

/**
 * Classify why a block or field exists in a response. This is deliberately separate from
 * semantic question identity, capture mechanism, UI behavior, and delivery targets.
 */
extern dec role(
  target: Model | Scalar | ModelProperty,
  role: valueof ResponseRole,
);

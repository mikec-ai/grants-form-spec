import type {
  DecoratorContext, Enum, EnumMember, Model, ModelProperty, Scalar, Type, Value,
} from "@typespec/compiler";
import { isArrayModelType, serializeValueAsJson, $summary } from "@typespec/compiler";
import { $id as $jsonSchemaId } from "@typespec/json-schema";
import { reportDiagnostic, stateKeys } from "./lib.js";
import { rememberConditionSourceModel } from "./model.js";

/**
 * `valueof <Model>` arrives as a TypeSpec ObjectValue with parent back-references,
 * so it cannot be serialized directly. Convert to plain JS at the boundary.
 */
function plain(ctx: DecoratorContext, value: unknown): unknown {
  const v = value as Value;
  if (v && typeof v === "object" && "entityKind" in v && (v as any).entityKind === "Value") {
    return serializeValueAsJson(ctx.program, v, (v as any).type);
  }
  return value;
}

type Ctx = DecoratorContext;

function resolvedArgumentProperty(ctx: Ctx, index: number): ModelProperty | undefined {
  const target = ctx.getArgumentTarget(index);
  if (!target || (target as any).entityKind) return undefined;
  const node = target as Parameters<typeof ctx.program.checker.getTypeForNode>[0];
  const resolved = ctx.program.checker.getTypeForNode(node);
  return resolved.kind === "ModelProperty" ? resolved : undefined;
}

/** Store a single value keyed by target. */
function set(ctx: Ctx, key: symbol, target: Type, value: unknown): void {
  ctx.program.stateMap(key).set(target, value);
}

/** Append to a list keyed by target. */
function push(ctx: Ctx, key: symbol, target: Type, value: unknown): void {
  const map = ctx.program.stateMap(key);
  const existing = (map.get(target) as unknown[] | undefined) ?? [];
  existing.push(value);
  map.set(target, existing);
}

// --- identity -------------------------------------------------------------

/**
 * A block's `$id`, relative to the bank's base URI. The base is declared once with
 * `@jsonSchema("<base>")` on the bank namespace, so it is a publishing decision in
 * the specs rather than a constant in this library — mirroring
 * `SharedSchemaConfig.shared_schema_base_uri` on the Python side.
 */
export const blockSchemaRef = (id: string) => `${id}/schema.json`;

/**
 * Delegate to the stock JSON Schema library, which resolves this relative id
 * against the namespace base and uses it for both `$id` and every `$ref` target.
 */
function publishAs(ctx: Ctx, target: Model | Scalar, id: string): void {
  $jsonSchemaId(ctx as any, target as any, blockSchemaRef(id));
}

export const $questionMeta = (ctx: Ctx, target: Model | Scalar, meta: unknown) => {
  const m = plain(ctx, meta) as { id: string; classification?: unknown };
  if (m.classification !== undefined) m.classification = enumName(m.classification);
  set(ctx, stateKeys.questionMeta, target, m);
  publishAs(ctx, target, m.id);
};

export const $formMeta = (ctx: Ctx, target: Model, meta: unknown) => {
  const m = plain(ctx, meta) as { id: string };
  set(ctx, stateKeys.formMeta, target, m);
  publishAs(ctx, target, m.id);
};

// --- catalogue ------------------------------------------------------------

export const $tag = (ctx: Ctx, target: Model | Scalar, ...tags: unknown[]) =>
  set(ctx, stateKeys.tags, target, tags.map((t) => enumName(t)));

export const $entity = (ctx: Ctx, target: Model | Scalar, entity: unknown) =>
  set(ctx, stateKeys.entity, target, enumName(entity));

// --- response semantics --------------------------------------------------

/** Keep response ownership orthogonal to question identity and presentation. */
export const $responseRole = (
  ctx: Ctx,
  target: Model | Scalar | ModelProperty,
  role: unknown,
) => set(ctx, stateKeys.responseRole, target, enumName(role));

/** An enum member argument arrives as the member; take its name. */
function enumName(v: unknown): string {
  const m = unwrap(v);
  if (m && typeof m === "object" && "name" in (m as any)) return String((m as any).name);
  return String(m);
}

/** Peel one layer of TypeSpec value wrapping. */
function unwrap(v: unknown): unknown {
  const o = v as any;
  if (o && typeof o === "object" && "entityKind" in o && o.entityKind === "Value" && "value" in o) {
    return o.value;
  }
  return v;
}

/**
 * Resolve a decorator argument to a plain JSON literal. Enum members yield their
 * wire value, so a comparison in an emitted schema is a string rather than a
 * compiler object with parent back-references.
 */
function literal(v: unknown): string | number | boolean | null {
  const u = unwrap(v) as any;
  if (u === null || u === undefined) return null;
  if (typeof u !== "object") return u;
  if (u.kind === "EnumMember" || ("name" in u && "enum" in u)) {
    return (u.value ?? u.name) as string | number;
  }
  if ("value" in u) return literal(u.value);
  if ("name" in u) return String(u.name);
  return String(u);
}

// --- presentation ---------------------------------------------------------

export const $sections = (ctx: Ctx, target: Model, sections: Enum) =>
  set(ctx, stateKeys.sections, target, sections);

/**
 * `valueof EnumMember` arrives as a value, not the member type, so resolve the
 * member's name and label here rather than in the emitters.
 */
export const $section = (ctx: Ctx, target: ModelProperty, section: unknown) =>
  set(ctx, stateKeys.section, target, sectionRef(section));

function sectionRef(v: unknown): { name: string; label?: string } {
  const m = v as any;
  if (m && typeof m === "object") {
    if (m.name) return { name: String(m.name), label: m.value ? String(m.value) : undefined };
    if (m.value?.name) return { name: String(m.value.name), label: m.value.value ? String(m.value.value) : undefined };
  }
  return { name: String(v) };
}

function overridePlain(value: unknown): unknown {
  const candidate = value as any;
  if (
    candidate
    && typeof candidate === "object"
    && candidate.entityKind === "Value"
  ) return literal(candidate);
  if (Array.isArray(value)) return value.map(overridePlain);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([key, nested]) => [key, overridePlain(nested)]),
    );
  }
  return value;
}

export const $overrides = (ctx: Ctx, target: Model | ModelProperty, patch: unknown) =>
  set(ctx, stateKeys.overrides, target, overridePlain(plain(ctx, patch)));

/**
 * A field label. Also delegated to `@summary`, which the JSON Schema emitter maps to
 * `title` — so the canonical schema carries the label without this library emitting
 * any schema keyword itself.
 */
export const $label = (ctx: Ctx, target: Model | Scalar | ModelProperty, text: string) => {
  set(ctx, stateKeys.label, target, text);
  $summary(ctx as any, target as any, text);
};

/**
 * Secondary guidance shown with the field. Distinct from the doc comment, which is the
 * question's own description: help text is what a form says *about asking it here*.
 */
export const $helpText = (ctx: Ctx, target: ModelProperty, text: string) =>
  set(ctx, stateKeys.helpText, target, text);

export const $widget = (ctx: Ctx, target: ModelProperty, widget: unknown) =>
  set(ctx, stateKeys.widget, target, enumName(widget));

export const $encodedCheckboxGroup = (
  ctx: Ctx,
  target: ModelProperty,
  contract: unknown,
) => {
  set(ctx, stateKeys.widget, target, "EncodedCheckboxGroup");
  set(ctx, stateKeys.encodedCheckboxGroup, target, plain(ctx, contract));
};

export const $order = (ctx: Ctx, target: Model, ...props: ModelProperty[]) =>
  set(ctx, stateKeys.order, target, props.map((p) => p.name));

export const $omit = (ctx: Ctx, target: ModelProperty) =>
  set(ctx, stateKeys.omit, target, true);

export const $readOnly = (ctx: Ctx, target: ModelProperty) =>
  set(ctx, stateKeys.readOnly, target, true);

// --- conditional logic ----------------------------------------------------

/**
 * `source` is a ModelProperty passed as `Model.prop` at the call site. It is reduced
 * to plain data here so no emitter ever handles a compiler object.
 */
function condition(source: ModelProperty, equals: unknown) {
  const t = source.type as any;
  return {
    operator: "equals" as const,
    sourcePath: [source.name],
    sourceIsArray: t?.kind === "Model" && !!t.indexer,
    value: literal(equals),
  };
}

export const $visibleWhen = (ctx: Ctx, target: ModelProperty, source: ModelProperty, equals: unknown) =>
  push(ctx, stateKeys.visibleWhen, target, condition(source, equals));

export const $enabledWhen = (ctx: Ctx, target: ModelProperty, source: ModelProperty, equals: unknown) =>
  push(ctx, stateKeys.enabledWhen, target, condition(source, equals));

export const $enabledWhenAny = (
  ctx: Ctx,
  target: ModelProperty,
  source: ModelProperty,
  ...equals: unknown[]
) => {
  const base = condition(source, null);
  push(ctx, stateKeys.enabledWhen, target, {
    operator: "in",
    sourcePath: base.sourcePath,
    sourceIsArray: base.sourceIsArray,
    values: equals.map(literal),
  });
};

function countCondition(
  ctx: Ctx,
  target: ModelProperty,
  source: ModelProperty,
  minimum: number,
) {
  let valid = true;
  const resolvedSource = resolvedArgumentProperty(ctx, 0) ?? source;
  if (resolvedSource.model && target.model && resolvedSource.model !== target.model) {
    reportDiagnostic(ctx.program, {
      code: "condition-source-not-sibling",
      target,
      format: { source: resolvedSource.name, target: target.name },
    });
    valid = false;
  }
  if (source.type.kind !== "Model" || !isArrayModelType(source.type)) {
    reportDiagnostic(ctx.program, {
      code: "condition-count-source-not-array",
      target,
      format: { source: source.name },
    });
    valid = false;
  }
  const normalizedMinimum = Number(literal(minimum));
  if (!Number.isInteger(normalizedMinimum) || normalizedMinimum <= 0) {
    reportDiagnostic(ctx.program, {
      code: "condition-count-minimum-invalid",
      target,
      format: { minimum: String(normalizedMinimum) },
    });
    valid = false;
  }
  if (!valid) return undefined;
  const condition = {
    operator: "countAtLeast" as const,
    sourcePath: [source.name],
    sourceIsArray: true,
    minimum: normalizedMinimum,
  };
  rememberConditionSourceModel(condition, resolvedSource.model);
  return condition;
}

export const $enabledWhenCount = (
  ctx: Ctx,
  target: ModelProperty,
  source: ModelProperty,
  minimum: number,
) => {
  const count = countCondition(ctx, target, source, minimum);
  if (count) push(ctx, stateKeys.enabledWhen, target, count);
};

/**
 * Enable a field once a sibling list reaches capacity, while keeping an already-saved value
 * operable if the list later falls below that threshold. This is the narrow disjunction needed
 * by overflow attachment controls; it deliberately does not expose an arbitrary expression AST.
 */
export const $enabledWhenCountOrPresent = (
  ctx: Ctx,
  target: ModelProperty,
  source: ModelProperty,
  minimum: number,
) => {
  const count = countCondition(ctx, target, source, minimum);
  if (!count) return;
  push(ctx, stateKeys.enabledWhen, target, {
    operator: "any",
    predicates: [
      count,
      {
        operator: "present",
        sourcePath: [target.name],
        sourceIsArray: false,
      },
    ],
  });
};

export const $readOnlyWhen = (ctx: Ctx, target: ModelProperty, source: ModelProperty, equals: unknown) =>
  push(ctx, stateKeys.readOnlyWhen, target, condition(source, equals));

export const $requiredWhen = (ctx: Ctx, target: ModelProperty, source: ModelProperty, equals: unknown) =>
  push(ctx, stateKeys.requiredWhen, target, condition(source, equals));

export const $requiredWhenPath = (
  ctx: Ctx,
  target: ModelProperty,
  sourcePath: unknown,
  equals: unknown,
) =>
  push(ctx, stateKeys.requiredWhen, target, {
    operator: "equals",
    sourcePath: String(literal(sourcePath)).split("."),
    sourceIsArray: false,
    value: literal(equals),
  });

export const $notBefore = (ctx: Ctx, target: ModelProperty, source: ModelProperty) =>
  set(ctx, stateKeys.notBefore, target, source);

export const $validationConstraints = (ctx: Ctx, target: ModelProperty, patch: unknown) =>
  set(ctx, stateKeys.validationConstraints, target, plain(ctx, patch));

export const $validationConstraintsWhen = (
  ctx: Ctx,
  target: ModelProperty,
  source: ModelProperty,
  equals: unknown,
  patch: unknown,
) =>
  push(ctx, stateKeys.validationConstraintsWhen, target, {
    condition: condition(source, equals),
    patch: plain(ctx, patch),
  });

export const $requiredPaths = (
  ctx: Ctx,
  target: Model | ModelProperty,
  ...paths: unknown[]
) => set(ctx, stateKeys.requiredPaths, target, paths.map((path) => String(literal(path))));

export const $requiredPathWhen = (
  ctx: Ctx,
  target: Model | ModelProperty,
  targetPath: unknown,
  sourcePath: unknown,
  equals: unknown,
) => push(ctx, stateKeys.requiredPathWhen, target, {
  targetPath: String(literal(targetPath)),
  sourcePath: String(literal(sourcePath)),
  value: literal(equals),
});

/** Record a bounded conditional choice over descendant paths. */
export const $atLeastOnePathWhenPresent = (
  ctx: Ctx,
  target: Model | ModelProperty,
  sourcePath: unknown,
  ...targetPaths: unknown[]
) => {
  const source = String(literal(sourcePath));
  const paths = [...new Set(targetPaths.map((path) => String(literal(path))))];
  if (!source || paths.length < 2 || paths.some((path) => !path)) {
    reportDiagnostic(ctx.program, {
      code: "conditional-at-least-one-path-invalid",
      target,
      format: {
        model: target.name || "an anonymous model",
        paths: paths.join(", ") || "none",
      },
    });
    return;
  }
  push(ctx, stateKeys.atLeastOnePathWhenPresent, target, {
    sourcePath: source,
    targetPaths: paths,
  });
};

export const $requiredPathWhenPositiveDecimalString = (
  ctx: Ctx,
  target: Model | ModelProperty,
  targetPath: unknown,
  sourcePath: unknown,
) => push(ctx, stateKeys.requiredPathWhenPositiveDecimalString, target, {
  targetPath: String(literal(targetPath)),
  sourcePath: String(literal(sourcePath)),
});

export const $positiveDecimalStringWhenPathPresent = (
  ctx: Ctx,
  target: Model | ModelProperty,
  targetPath: unknown,
  sourcePath: unknown,
) => push(ctx, stateKeys.positiveDecimalStringWhenPathPresent, target, {
  targetPath: String(literal(targetPath)),
  sourcePath: String(literal(sourcePath)),
});

/** Record a portable JSON Schema any-of-required constraint on sibling properties. */
export const $atLeastOneOf = (
  ctx: Ctx,
  target: Model,
  ...properties: ModelProperty[]
) => {
  const names = [...new Set(properties.map((property) => property.name))];
  if (
    names.length < 2 ||
    properties.some((property) => property.model !== target)
  ) {
    reportDiagnostic(ctx.program, {
      code: "at-least-one-invalid",
      target,
      format: {
        model: target.name || "an anonymous model",
        properties: names.join(", ") || "none",
      },
    });
    return;
  }
  push(ctx, stateKeys.atLeastOneOf, target, names);
};

export const $computed = (
  ctx: Ctx,
  target: ModelProperty,
  operator: unknown,
  ...refs: ModelProperty[]
) =>
  set(ctx, stateKeys.computed, target, {
    operator: enumName(operator),
    refs: refs.map((r) => r.name),
  });

export const $computedFrom = (
  ctx: Ctx,
  target: ModelProperty,
  operator: unknown,
  ...paths: unknown[]
) =>
  set(ctx, stateKeys.computedFrom, target, {
    operator: enumName(operator),
    paths: paths.map((path) => String(literal(path))),
  });

export const $materializeWhenAnySourcePresent = (ctx: Ctx, target: ModelProperty) =>
  set(ctx, stateKeys.calculationMaterialization, target, "when_any_source_present");

export const $evaluationOrder = (ctx: Ctx, target: ModelProperty, order: number) =>
  set(ctx, stateKeys.evaluationOrder, target, order);

/**
 * Field-by-field totalling. Only the source properties are recorded; which field of the
 * block pairs with which is worked out at emission, where the type graph is in view.
 */
export const $totals = (ctx: Ctx, target: ModelProperty, ...sources: ModelProperty[]) =>
  set(ctx, stateKeys.totals, target, sources);

// --- SGG target vocabulary ------------------------------------------------

/** The rule name is the enum member's *value*, which is SGG's wire spelling. */
export const $multiField = (ctx: Ctx, target: Model, section: unknown, widget: unknown) =>
  push(ctx, stateKeys.multiField, target, {
    section: sectionRef(section).name,
    widget: enumName(widget),
  });

export const $fieldList = (ctx: Ctx, target: ModelProperty, options: unknown) =>
  set(ctx, stateKeys.fieldList, target, plain(ctx, options));

/**
 * The rule name is each entry's enum *value*, which is SGG's wire spelling. Marshalled here
 * so the emitter sees a plain `path -> rule` map (D11).
 */
export const $prePopulate = (ctx: Ctx, target: Model, rules: unknown) => {
  const table = plain(ctx, rules) as Record<string, unknown>;
  const out: Record<string, string> = {};
  for (const [path, rule] of Object.entries(table ?? {})) {
    out[path] = String(literal(rule));
  }
  set(ctx, stateKeys.prePopulate, target, out);
};

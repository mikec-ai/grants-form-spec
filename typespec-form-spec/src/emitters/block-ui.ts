import type { Program } from "@typespec/compiler";
import { getDoc } from "@typespec/compiler";
import {
  AtomicCondition, Block, Condition, childBlock, orderedProps, propEnabledWhen, propLabel, propReadOnly, propReadOnlyWhen, propVisibleWhen, propWidget,
} from "../model.js";

const conditionSchema = (condition: AtomicCondition): Record<string, unknown> =>
  condition.operator === "in"
    ? { enum: condition.values }
    : condition.operator === "countAtLeast"
      ? { type: "array", minItems: condition.minimum }
      : condition.operator === "present"
        ? {
            not: {
              anyOf: [
                { type: "null" },
                { const: "" },
                { type: "array", maxItems: 0 },
              ],
            },
          }
        : { const: condition.value };

/** A condition over the block root, used only for the bounded cross-field disjunction. */
const rootConditionSchema = (condition: AtomicCondition): Record<string, unknown> => {
  let schema = conditionSchema(condition);
  for (const step of [...condition.sourcePath].reverse()) {
    schema = { properties: { [step]: schema }, required: [step] };
  }
  return schema;
};

const jsonFormsCondition = (condition: Condition): Record<string, unknown> =>
  condition.operator === "any"
    ? {
        scope: "#",
        schema: { anyOf: condition.predicates.map(rootConditionSchema) },
      }
    : {
        scope: `#/${condition.sourcePath.map((step) => `properties/${step}`).join("/")}`,
        schema: conditionSchema(condition),
      };

export interface UiNode {
  type: string;
  scope?: string;
  label?: string;
  elements?: UiNode[];
  options?: Record<string, unknown>;
  rule?: Record<string, unknown>;
}

/** Re-prefix every Control scope so a child's tree sits under `propName`. */
export function rescopeUi(node: UiNode, propName: string): UiNode {
  const out: UiNode = { ...node };
  if (typeof out.scope === "string" && out.scope.startsWith("#/")) {
    out.scope = `#/properties/${propName}/${out.scope.slice(2)}`;
  }
  const condition = out.rule?.condition as { scope?: unknown; schema?: unknown } | undefined;
  if (typeof condition?.scope === "string" && condition.scope.startsWith("#/")) {
    out.rule = {
      ...out.rule,
      condition: {
        ...condition,
        scope: `#/properties/${propName}/${condition.scope.slice(2)}`,
      },
    };
  } else if (condition?.scope === "#" && condition.schema !== undefined) {
    out.rule = {
      ...out.rule,
      condition: {
        ...condition,
        schema: {
          properties: { [propName]: condition.schema },
          required: [propName],
        },
      },
    };
  }
  if (out.elements) out.elements = out.elements.map((c) => rescopeUi(c, propName));
  return out;
}

/**
 * The canonical UI artifact for one block. Scopes are relative to this block's own
 * root, so it renders standalone; children are incorporated and re-scoped.
 */
export function emitBlockUi(program: Program, block: Block): UiNode {
  // A single-value question renders as one Control at its own root.
  if (block.scalar) {
    const node: UiNode = { type: "Control", scope: "#" };
    if (block.label) node.label = block.label;
    return node;
  }

  const elements: UiNode[] = [];

  for (const prop of orderedProps(program, block)) {
    const child = childBlock(program, prop);
    if (child && !child.scalar) {
      elements.push(rescopeUi(emitBlockUi(program, child), prop.name));
      continue;
    }

    const node: UiNode = { type: "Control", scope: `#/properties/${prop.name}` };
    const label = propLabel(program, prop);
    if (label) node.label = label;

    const widget = propWidget(program, prop);
    if (widget) node.options = { ...(node.options ?? {}), widget };
    if (propReadOnly(program, prop)) node.options = { ...(node.options ?? {}), readonly: true };

    const conds = propVisibleWhen(program, prop);
    if (conds.length === 1) {
      const c = conds[0];
      node.rule = {
        effect: "SHOW",
        condition: jsonFormsCondition(c),
      };
    } else {
      const enabled = propEnabledWhen(program, prop);
      if (enabled.length === 1) {
        const c = enabled[0];
        node.rule = {
          effect: "ENABLE",
          condition: jsonFormsCondition(c),
        };
      } else {
        const readOnly = propReadOnlyWhen(program, prop);
        if (readOnly.length === 1) {
          const c = readOnly[0];
          node.rule = {
            effect: "DISABLE",
            condition: jsonFormsCondition(c),
          };
        }
      }
    }

    elements.push(node);
  }

  const group: UiNode = { type: "Group", elements };
  if (block.label) group.label = block.label;
  else if (block.doc) group.label = block.doc;
  return group;
}

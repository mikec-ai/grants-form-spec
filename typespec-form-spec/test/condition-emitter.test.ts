import { describe, expect, it } from "vitest";
import { emitBlockUi } from "../src/emitters/block-ui.js";
import { emitSggUi } from "../src/emitters/ui-schema-sgg.js";
import { allBlocks } from "../src/model.js";
import { Tester, form, formMeta } from "./tester.js";

describe("bounded presence conditions", () => {
  it("emits count-or-saved-value behavior without a form-specific generator", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum OverflowSection { people: "People", uploads: "Overflow uploads" }
        ${formMeta("overflow-condition-check")}
        @UI.sections(OverflowSection)
        model OverflowConditionCheck {
          @UI.section(OverflowSection.people)
          @maxItems(99)
          people?: string[];

          @UI.section(OverflowSection.uploads)
          @UI.enabledWhenCountOrPresent(OverflowConditionCheck.people, 99)
          upload?: string;
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "overflow-condition-check",
    );
    expect(block).toBeDefined();

    expect(emitSggUi(instance.program, block!)[1].children[0]).toMatchObject({
      definition: "/properties/upload",
      conditional: {
        when: {
          op: "any",
          predicates: [
            {
              op: "countAtLeast",
              ref: { scope: "root", pointer: "/people" },
              minimum: 99,
            },
            {
              op: "present",
              ref: { scope: "root", pointer: "/upload" },
            },
          ],
        },
        then: { interaction: "enabled" },
        otherwise: { interaction: "disabled" },
      },
    });

    const canonical = emitBlockUi(instance.program, block!);
    expect(canonical.elements?.[1]).toMatchObject({
      scope: "#/properties/upload",
      rule: {
        effect: "ENABLE",
        condition: {
          scope: "#",
          schema: {
            anyOf: [
              {
                properties: { people: { type: "array", minItems: 99 } },
                required: ["people"],
              },
              {
                properties: {
                  upload: {
                    not: {
                      anyOf: [
                        { type: "null" },
                        { const: "" },
                        { type: "array", maxItems: 0 },
                      ],
                    },
                  },
                },
                required: ["upload"],
              },
            ],
          },
        },
      },
    });
  });
});

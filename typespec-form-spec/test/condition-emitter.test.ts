import { describe, expect, it } from "vitest";
import { expectDiagnostics } from "@typespec/compiler/testing";
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

  it("scopes both sides of the disjunction to the current repeated item", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum RepeatedSection { entries: "Entries" }
        model RepeatedOverflow {
          people?: string[];

          @UI.enabledWhenCountOrPresent(RepeatedOverflow.people, 2)
          upload?: string;
        }

        ${formMeta("repeated-overflow-condition-check")}
        @UI.sections(RepeatedSection)
        model RepeatedOverflowConditionCheck {
          @UI.section(RepeatedSection.entries)
          entries?: RepeatedOverflow[];
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "repeated-overflow-condition-check",
    );
    const upload = emitSggUi(instance.program, block!)[0].children[0];
    const fields = upload.type === "fieldList" ? upload.children : [];

    expect(fields.find((field) => field.definition.endsWith("/upload"))).toMatchObject({
      conditional: {
        when: {
          op: "any",
          predicates: [
            {
              op: "countAtLeast",
              ref: { scope: "item", pointer: "/people" },
              minimum: 2,
            },
            {
              op: "present",
              ref: { scope: "item", pointer: "/upload" },
            },
          ],
        },
      },
    });
  });

  it("rejects a scalar count source for the existing count decorator", async () => {
    expectDiagnostics(
      await Tester.diagnose(
        form(`
          ${formMeta("scalar-count-source")}
          model ScalarCountSource {
            people?: string;
            @UI.enabledWhenCount(ScalarCountSource.people, 1)
            upload?: string;
          }
        `),
      ),
      { code: "@simpler-grants/form-spec/condition-count-source-not-array" },
    );
  });

  it("rejects an indexed record because runtime count semantics are array-only", async () => {
    expectDiagnostics(
      await Tester.diagnose(
        form(`
          ${formMeta("record-count-source")}
          model RecordCountSource {
            people?: Record<string>;
            @UI.enabledWhenCount(RecordCountSource.people, 1)
            upload?: string;
          }
        `),
      ),
      { code: "@simpler-grants/form-spec/condition-count-source-not-array" },
    );
  });

  it("rejects a count source from another model instead of rebinding it by name", async () => {
    expectDiagnostics(
      await Tester.diagnose(
        form(`
          model OtherPeople { people?: string[]; }
          ${formMeta("foreign-count-source")}
          model ForeignCountSource {
            people?: string[];
            @UI.enabledWhenCountOrPresent(OtherPeople.people, 1)
            upload?: string;
          }
        `),
      ),
      { code: "@simpler-grants/form-spec/condition-source-not-sibling" },
    );
  });

  it.each([0, -1])("rejects a non-positive count threshold (%s)", async (minimum) => {
    expectDiagnostics(
      await Tester.diagnose(
        form(`
          ${formMeta(`invalid-count-minimum-${minimum}`)}
          model InvalidCountMinimum {
            people?: string[];
            @UI.enabledWhenCountOrPresent(InvalidCountMinimum.people, ${minimum})
            upload?: string;
          }
        `),
      ),
      { code: "@simpler-grants/form-spec/condition-count-minimum-invalid" },
    );
  });
});

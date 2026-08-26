import { describe, expect, it } from "vitest";
import { expectDiagnostics } from "@typespec/compiler/testing";
import Ajv2020 from "ajv/dist/2020.js";
import { emitBlockUi } from "../src/emitters/block-ui.js";
import { emitFieldOccurrences } from "../src/emitters/field-occurrences.js";
import { emitSggUi } from "../src/emitters/ui-schema-sgg.js";
import { emitSchemaOverlay } from "../src/emitters/overlay.js";
import { allBlocks } from "../src/model.js";
import { Tester, form, formMeta } from "./tester.js";

describe("bounded presence conditions", () => {
  it("preserves interaction conditions on repeatable groups", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum Answer { yes: "Yes", no: "No" }
        enum ConditionalListSection { entries: "Entries" }
        model Entry { value?: string; }

        ${formMeta("conditional-list-check")}
        @UI.sections(ConditionalListSection)
        model ConditionalListCheck {
          @UI.section(ConditionalListSection.entries)
          enabled: Answer;
          @UI.enabledWhen(ConditionalListCheck.enabled, Answer.yes)
          @UI.section(ConditionalListSection.entries)
          entries?: Entry[];
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "conditional-list-check",
    );
    const list = emitSggUi(instance.program, block!)[0].children.find(
      (node) => node.type === "fieldList",
    );
    expect(list).toMatchObject({
      type: "fieldList",
      name: "entries",
      conditional: {
        when: {
          op: "equals",
          ref: { scope: "root", pointer: "/enabled" },
          value: "Yes",
        },
        then: { interaction: "enabled" },
        otherwise: { interaction: "disabled" },
      },
    });
  });

  it("keeps intrinsic cardinality in a published question while preserving occurrence narrowing", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum Country { usa: "USA", other: "Other" }

        /** A reusable address with intrinsic source-backed cardinality. */
        @Question.meta(#{ id: "test/address" })
        @Catalog.tag(TagName.address)
        @Validation.requiredPaths("street", "city", "country")
        @Validation.requiredPathWhen("state", "country", Country.usa)
        model SharedAddress {
          street?: string;
          city?: string;
          country?: Country;
          state?: string;
          suite?: string;
        }

        ${formMeta("shared-cardinality-check")}
        model SharedCardinalityCheck {
          applicant: SharedAddress;

          @Validation.requiredPaths("suite")
          mailing: SharedAddress;
        }
      `),
    );

    const blocks = allBlocks(instance.program);
    const question = blocks.find((candidate) => candidate.id === "test/address");
    const formBlock = blocks.find(
      (candidate) => candidate.id === "shared-cardinality-check",
    );

    expect(emitSchemaOverlay(instance.program, question!)).toMatchObject({
      required: ["street", "city", "country"],
      allOf: [
        {
          if: {
            properties: { country: { const: "USA" } },
            required: ["country"],
          },
          then: { required: ["state"] },
        },
      ],
    });
    expect(emitSchemaOverlay(instance.program, formBlock!)).toEqual({
      properties: {
        mailing: { required: ["suite"] },
      },
    });
  });

  it("emits at-least-one alternatives as portable JSON Schema", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        ${formMeta("alternative-check")}
        @Validation.atLeastOneOf(AlternativeCheck.awardNumber, AlternativeCheck.projectName)
        model AlternativeCheck { awardNumber?: string; projectName?: string; }
      `),
    );
    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "alternative-check",
    );
    const overlay = emitSchemaOverlay(instance.program, block!);
    expect(overlay).toMatchObject({
      allOf: [{
        anyOf: [
          { required: ["awardNumber"] },
          { required: ["projectName"] },
        ],
      }],
    });
  });

  it("emits a presence-triggered choice across nested paths", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        model Trigger { value: string; }
        model Choice { first?: { value: string }; second?: { value: string }; }
        ${formMeta("conditional-alternative-check")}
        @Validation.atLeastOnePathWhenPresent(
          "trigger.value",
          "choices.first.value",
          "choices.second.value"
        )
        model ConditionalAlternativeCheck {
          trigger?: Trigger;
          choices?: Choice;
        }
      `),
    );
    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "conditional-alternative-check",
    );
    const overlay = emitSchemaOverlay(instance.program, block!);
    expect(overlay).toMatchObject({
      allOf: [{
        if: {
          required: ["trigger"],
          properties: {
            trigger: { required: ["value"] },
          },
        },
        then: {
          anyOf: [
            {
              required: ["choices"],
              properties: {
                choices: {
                  required: ["first"],
                  properties: { first: { required: ["value"] } },
                },
              },
            },
            {
              required: ["choices"],
              properties: {
                choices: {
                  required: ["second"],
                  properties: { second: { required: ["value"] } },
                },
              },
            },
          ],
        },
      }],
    });
    const validate = new Ajv2020({ strict: false }).compile(overlay!);
    expect(validate({})).toBe(true);
    expect(validate({ trigger: { value: "entered" } })).toBe(false);
    expect(validate({
      trigger: { value: "entered" },
      choices: { first: { value: "selected" } },
    })).toBe(true);
    expect(validate({
      trigger: { value: "entered" },
      choices: { first: {} },
    })).toBe(false);
    expect(validate({
      trigger: { value: "entered" },
      choices: { second: { value: "non-sequential" } },
    })).toBe(true);
  });

  it("emits bidirectional attachment and positive decimal-string conditions", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        scalar MoneyString extends string;
        ${formMeta("positive-decimal-string-check")}
        @Validation.requiredPathWhenPositiveDecimalString("attachment", "total")
        @Validation.positiveDecimalStringWhenPathPresent("total", "attachment")
        model PositiveDecimalStringCheck {
          attachment?: string;
          total?: MoneyString;
        }
      `),
    );
    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "positive-decimal-string-check",
    );
    const overlay = emitSchemaOverlay(instance.program, block!);
    expect(overlay).toEqual({
      allOf: [
        {
          if: {
            required: ["total"],
            properties: {
              total: { pattern: "^(?=.*[1-9])\\d+(?:\\.\\d+)?$" },
            },
          },
          then: { required: ["attachment"] },
        },
        {
          if: { required: ["attachment"] },
          then: {
            required: ["total"],
            properties: {
              total: { pattern: "^(?=.*[1-9])\\d+(?:\\.\\d+)?$" },
            },
          },
        },
      ],
    });
    const validate = new Ajv2020({ strict: false }).compile(overlay!);
    expect(validate({})).toBe(true);
    expect(validate({ total: "0.00" })).toBe(true);
    expect(validate({ total: "1.00" })).toBe(false);
    expect(validate({ attachment: "file-id" })).toBe(false);
    expect(validate({ attachment: "file-id", total: "0.00" })).toBe(false);
    expect(validate({ attachment: "file-id", total: "0.01" })).toBe(true);
    expect(validate({ attachment: "file-id", total: "000.10" })).toBe(true);
  });

  it("keeps inherited question lineage and sections when a form extends a question", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum FilingSection { filing: "Filing" }
        @Question.meta(#{ id: "test/filing-details" })
        @Catalog.entity(EntityName.application)
        @Catalog.tag(TagName.details)
        model FilingDetails {
          @UI.section(FilingSection.filing)
          kind: string;
          @UI.section(FilingSection.filing)
          details: { value: string };
        }

        ${formMeta("inherited-question-check")}
        @UI.sections(FilingSection)
        model InheritedQuestionCheck extends FilingDetails {}
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "inherited-question-check",
    );
    expect(emitSggUi(instance.program, block!)[0].children[0]).toMatchObject({
      definition: "/properties/kind",
    });
    expect(emitFieldOccurrences(instance.program, block!)).toEqual(expect.arrayContaining([
      { path: "/kind", leaf: true, blockIds: ["test/filing-details"] },
      { path: "/details/value", leaf: true, blockIds: ["test/filing-details"] },
    ]));
  });

  it("carries a top-level object's visibility condition onto its flattened SGG fields", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum Choice { no: "No", yes: "Yes" }
        enum DetailsSection { details: "Details" }
        model Details { name: string; address: string; }

        ${formMeta("conditional-object-check")}
        @UI.sections(DetailsSection)
        model ConditionalObjectCheck {
          @UI.section(DetailsSection.details)
          choice: Choice;

          @UI.section(DetailsSection.details)
          @UI.visibleWhen(ConditionalObjectCheck.choice, Choice.yes)
          details?: Details;
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "conditional-object-check",
    );
    const children = emitSggUi(instance.program, block!)[0].children;
    for (const field of children.slice(1)) {
      expect(field).toMatchObject({
        conditional: {
          when: {
            op: "equals",
            ref: { scope: "root", pointer: "/choice" },
            value: "Yes",
          },
          then: { visible: true },
          otherwise: { visible: false },
        },
      });
    }
  });

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

  it("rescopes a canonical root condition when a question is nested in a form", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        @Question.meta(#{ id: "test/nested-overflow" })
        model NestedOverflow {
          people?: string[];

          @UI.enabledWhenCountOrPresent(NestedOverflow.people, 2)
          upload?: string;
        }

        ${formMeta("nested-overflow-condition-check")}
        model NestedOverflowConditionCheck {
          nested?: NestedOverflow;
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "nested-overflow-condition-check",
    );
    const canonical = emitBlockUi(instance.program, block!);

    expect(canonical.elements?.[0].elements?.[1]).toMatchObject({
      scope: "#/properties/nested/properties/upload",
      rule: {
        effect: "ENABLE",
        condition: {
          scope: "#",
          schema: {
            properties: {
              nested: {
                anyOf: [
                  {
                    properties: { people: { type: "array", minItems: 2 } },
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
            required: ["nested"],
          },
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

  it("rejects a same-named count source from another namespace", async () => {
    expectDiagnostics(
      await Tester.diagnose(`
        import "@simpler-grants/form-spec";
        using SimplerForms;

        namespace Source {
          model Twin { people?: string[]; }
        }

        namespace Target {
          ${formMeta("same-named-foreign-count-source")}
          model Twin {
            people?: string[];
            @UI.enabledWhenCountOrPresent(Source.Twin.people, 1)
            upload?: string;
          }
        }
      `),
      { code: "@simpler-grants/form-spec/condition-source-not-sibling" },
    );
  });

  it("accepts an alias that resolves to the target model", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(`
      import "@simpler-grants/form-spec";
      using SimplerForms;

      alias LocalTwin = Target.Twin;
      namespace Target {
        enum TwinSection { fields: "Fields" }
        ${formMeta("aliased-count-source")}
        @UI.sections(TwinSection)
        model Twin {
          @UI.section(TwinSection.fields)
          people?: string[];
          @UI.section(TwinSection.fields)
          @UI.enabledWhenCountOrPresent(LocalTwin.people, 1)
          upload?: string;
        }
      }
    `);

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "aliased-count-source",
    );
    const upload = emitSggUi(instance.program, block!)
      .flatMap((node) => ("children" in node ? node.children : [node]))
      .find((node) => "definition" in node && node.definition === "/properties/upload");
    expect(upload).toMatchObject({
      definition: "/properties/upload",
      conditional: {
        when: {
          op: "any",
          predicates: [
            { op: "countAtLeast", ref: { pointer: "/people" }, minimum: 1 },
            { op: "present", ref: { pointer: "/upload" } },
          ],
        },
      },
    });
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

describe("field occurrence role precedence", () => {
  it("keeps a direct type role above the owning question default", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(`
      import "@simpler-grants/form-spec";
      using SimplerForms;

      namespace QuestionBank {
        @Question.meta(#{ id: "application/system-identifier" })
        @Response.role(ResponseRole.systemValue)
        @Catalog.tag(TagName.identifier)
        scalar SystemIdentifier extends string;

        @Question.meta(#{ id: "application/mixed-details" })
        @Response.role(ResponseRole.applicantInput)
        @Catalog.tag(TagName.details)
        model MixedDetails {
          identifier?: SystemIdentifier;
          explanation?: string;
        }
      }

      namespace Forms {
        @Form.meta(#{
          id: "mixed-role-check",
          formName: "mixed-role-check",
          shortFormName: "mixed-role-check",
          formVersion: "1.0",
        })
        model MixedRoleCheck {
          ...QuestionBank.MixedDetails;
        }
      }
    `);

    const form = allBlocks(instance.program).find(
      (candidate) => candidate.id === "mixed-role-check",
    );
    expect(form).toBeDefined();
    const occurrences = emitFieldOccurrences(instance.program, form!);
    expect(occurrences.find((row) => row.path === "/identifier")).toMatchObject({
      responseRole: "systemValue",
    });
    expect(occurrences.find((row) => row.path === "/explanation")).toMatchObject({
      responseRole: "applicantInput",
    });
  });
});

describe("form-scoped behavior overrides", () => {
  it("projects presentation overrides through repeated object items", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum OverrideSection { reports: "Reports" }
        model SharedTotals { entered?: int32; total?: int32; }
        model SharedReport { details?: SharedTotals; }

        ${formMeta("repeated-presentation-override-check")}
        @UI.sections(OverrideSection)
        @UI.overrides(#{
          \`reports.details.total\`: #{ readOnly: true, visibleReadOnly: true },
        })
        model RepeatedPresentationOverrideCheck {
          @UI.section(OverrideSection.reports)
          reports: SharedReport[];
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "repeated-presentation-override-check",
    );
    expect(block).toBeDefined();
    expect(emitSchemaOverlay(instance.program, block!)).toEqual({
      properties: {
        reports: {
          allOf: [{
            items: {
              properties: {
                details: { properties: { total: { readOnly: true } } },
              },
            },
          }],
        },
      },
    });
    const fields = emitSggUi(instance.program, block!)[0].children;
    const reports = fields.find((field) => field.definition === "/properties/reports");
    expect(reports).toMatchObject({
      type: "fieldList",
      children: expect.arrayContaining([
        {
          type: "field",
          definition: "/properties/reports/items/properties/details/properties/total",
        },
      ]),
    });
  });

  it("emits an enabled condition without re-declaring the shared question", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum Mode { enabled: "Enabled", disabled: "Disabled" }
        enum OverrideSection { details: "Details" }
        model SharedDetails { mode?: Mode; explanation?: string; }
        @Question.meta(#{ id: "shared/details" })
        model LocalDetails { ...SharedDetails; }

        ${formMeta("behavior-override-check")}
        @UI.sections(OverrideSection)
        @UI.overrides(#{
          \`details.explanation\`: #{
            enabledWhen: #{ path: "details.mode", equals: Mode.enabled }
          },
        })
        model BehaviorOverrideCheck {
          @UI.section(OverrideSection.details)
          details?: LocalDetails;
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "behavior-override-check",
    );
    expect(block).toBeDefined();
    expect(block!.overrides["details.explanation"]).toEqual({
      enabledWhen: { path: "details.mode", equals: "Enabled" },
    });
    const canonical = emitBlockUi(instance.program, block!);
    const findScope = (node: typeof canonical, suffix: string): typeof canonical | undefined =>
      node.scope?.endsWith(suffix)
        ? node
        : node.elements?.map((child) => findScope(child, suffix)).find(Boolean);
    const canonicalExplanation = findScope(canonical, "/explanation");
    expect(canonicalExplanation).toMatchObject({
      scope: "#/properties/details/properties/explanation",
      rule: {
        effect: "ENABLE",
        condition: {
          scope: "#/properties/details/properties/mode",
          schema: { const: "Enabled" },
        },
      },
    });
    const fields = emitSggUi(instance.program, block!)[0].children;
    expect(fields.find((field) => field.definition.endsWith("/explanation"))).toMatchObject({
      conditional: {
        when: {
          op: "equals",
          ref: { scope: "root", pointer: "/details/mode" },
          value: "Enabled",
        },
        then: { interaction: "enabled" },
        otherwise: { interaction: "disabled" },
      },
    });
  });

  it("emits a one-of enabled condition against a nested shared question", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum Mode { first: "First", second: "Second", disabled: "Disabled" }
        enum OverrideSection { details: "Details" }
        model SharedDetails { mode: Mode; }

        ${formMeta("behavior-override-in-check")}
        @UI.sections(OverrideSection)
        @UI.overrides(#{
          \`explanation\`: #{
            enabledWhen: #{ path: "details.mode", in: #[Mode.first, Mode.second] }
          },
        })
        model BehaviorOverrideInCheck {
          @UI.section(OverrideSection.details)
          details: SharedDetails;

          @UI.section(OverrideSection.details)
          explanation?: string;
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "behavior-override-in-check",
    );
    expect(block).toBeDefined();
    const canonical = emitBlockUi(instance.program, block!);
    expect(canonical.elements?.find((field) => field.scope?.endsWith("/explanation"))).toMatchObject({
      rule: {
        effect: "ENABLE",
        condition: {
          scope: "#/properties/details/properties/mode",
          schema: { enum: ["First", "Second"] },
        },
      },
    });
    const fields = emitSggUi(instance.program, block!)[0].children;
    expect(fields.find((field) => field.definition.endsWith("/explanation"))).toMatchObject({
      conditional: {
        when: {
          op: "in",
          ref: { scope: "root", pointer: "/details/mode" },
          values: ["First", "Second"],
        },
        then: { interaction: "enabled" },
        otherwise: { interaction: "disabled" },
      },
    });
  });

  it("fails closed when an enabled override collides with intrinsic behavior", async () => {
    const instance = await Tester.createInstance();
    await instance.compile(
      form(`
        enum Mode { first: "First", second: "Second" }
        enum CollisionSection { details: "Details" }

        ${formMeta("behavior-override-collision")}
        @UI.sections(CollisionSection)
        @UI.overrides(#{
          explanation: #{ enabledWhen: #{ path: "mode", equals: Mode.second } },
        })
        model BehaviorOverrideCollision {
          @UI.section(CollisionSection.details)
          mode: Mode;

          @UI.section(CollisionSection.details)
          @UI.enabledWhen(BehaviorOverrideCollision.mode, Mode.first)
          explanation?: string;
        }
      `),
    );

    const block = allBlocks(instance.program).find(
      (candidate) => candidate.id === "behavior-override-collision",
    );
    expect(block).toBeDefined();
    expect(() => emitBlockUi(instance.program, block!)).toThrow(
      "@UI.overrides enabledWhen collides with intrinsic UI behavior at explanation",
    );
    expect(() => emitSggUi(instance.program, block!)).toThrow(
      "@UI.overrides enabledWhen collides with intrinsic UI behavior at explanation",
    );
  });

  it.each([
    ["visible", "@UI.visibleWhen"],
    ["read-only", "@UI.readOnlyWhen"],
  ])("fails closed when an enabled override collides with intrinsic %s behavior", async (kind, decorator) => {
    const instance = await Tester.createInstance();
    const id = `behavior-override-${kind}-collision`;
    await instance.compile(
      form(`
        enum Mode { first: "First", second: "Second" }
        enum CollisionSection { details: "Details" }

        ${formMeta(id)}
        @UI.sections(CollisionSection)
        @UI.overrides(#{
          explanation: #{ enabledWhen: #{ path: "mode", equals: Mode.second } },
        })
        model BehaviorOverrideCollision {
          @UI.section(CollisionSection.details)
          mode: Mode;

          @UI.section(CollisionSection.details)
          ${decorator}(BehaviorOverrideCollision.mode, Mode.first)
          explanation?: string;
        }
      `),
    );

    const block = allBlocks(instance.program).find((candidate) => candidate.id === id);
    expect(block).toBeDefined();
    expect(() => emitBlockUi(instance.program, block!)).toThrow(
      "@UI.overrides enabledWhen collides with intrinsic UI behavior at explanation",
    );
    expect(() => emitSggUi(instance.program, block!)).toThrow(
      "@UI.overrides enabledWhen collides with intrinsic UI behavior at explanation",
    );
  });
});

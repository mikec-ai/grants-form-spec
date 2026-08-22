import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");

describe("SGG UI emission", () => {
  it("projects nested research-budget lists and all source-resolved sums generically", async () => {
    const root = resolve(packageRoot, "dist/forms/rr-budget");
    const ui = JSON.parse(await readFile(resolve(root, "sgg/ui-schema.json"), "utf8"));
    const rules = JSON.parse(await readFile(resolve(root, "sgg/rule-schema.json"), "utf8"));

    const allObjects = (value: unknown): Record<string, unknown>[] => {
      if (Array.isArray(value)) return value.flatMap(allObjects);
      if (!value || typeof value !== "object") return [];
      const object = value as Record<string, unknown>;
      return [object, ...Object.values(object).flatMap(allObjects)];
    };

    const lists = allObjects(ui).filter((node) => node.type === "fieldList");
    const calculations = allObjects(rules).filter((node) =>
      Object.prototype.hasOwnProperty.call(node, "gg_pre_population")
    );

    expect(lists.map((node) => node.name)).toEqual([
      "budgetYear",
      "equipmentList",
      "indirectCost",
      "keyPerson",
      "other",
    ]);
    expect(calculations).toHaveLength(56);
    expect(
      rules.budgetYear.totalCompensation.gg_pre_population.fields,
    ).toEqual([
      "@THIS.keyPersons.totalFundForKeyPersons",
      "@THIS.otherPersonnel.totalOtherPersonnelFund",
    ]);
    expect(rules.budgetYear.keyPersons.keyPerson.fundsRequested.gg_pre_population.order).toBe(1);
    expect(
      rules.budgetSummary.cumulativeTotalFundsRequestedTravel.gg_pre_population.fields,
    ).toEqual(["budgetYear[*].travel.totalTravelCost"]);
    expect(
      rules.budgetSummary.cumulativeTotalFundsRequestedTravel.gg_pre_population.order,
    ).toBe(51);
    expect(
      calculations
        .map((node) => (node.gg_pre_population as { order?: number }).order)
        .sort((a, b) => (a ?? 0) - (b ?? 0)),
    ).toEqual(Array.from({ length: 56 }, (_, index) => index + 1));
    expect(
      rules.budgetYear.otherPersonnel.otherPersonnelTotalNumber.gg_pre_population.rule,
    ).toBe("sum_integer");
    expect(rules.budgetYear.directCosts.gg_pre_population.fields).toEqual([
      "@THIS.keyPersons.totalFundForKeyPersons",
      "@THIS.otherPersonnel.totalOtherPersonnelFund",
      "@THIS.equipment.totalFund",
      "@THIS.travel.totalTravelCost",
      "@THIS.participantTraineeSupportCosts.totalCost",
      "@THIS.otherDirectCosts.totalOtherDirectCost",
    ]);

    const period = JSON.parse(
      await readFile(
        resolve(packageRoot, "dist/question-bank/budget/research/period/schema.json"),
        "utf8",
      ),
    );
    expect(period.properties.directCosts.readOnly).toBe(true);
    expect(period.$defs.ResearchBudgetDecimal15.pattern).toBe(
      "^-?(?:\\d{1,15}|\\d{1,14}[.]\\d|\\d{1,13}[.]\\d{2})$",
    );
    expect(period.$defs.ResearchBudgetTotalAmount15.pattern).toBe(
      "^(?:\\d{1,15}|\\d{1,14}[.]\\d|\\d{1,13}[.]\\d{2})$",
    );

    const personnel = JSON.parse(
      await readFile(
        resolve(packageRoot, "dist/question-bank/budget/research/other-personnel/schema.json"),
        "utf8",
      ),
    );
    expect(personnel.$defs.ResearchBudgetCount3).toMatchObject({
      type: "integer",
      minimum: 0,
      maximum: 999,
    });
    expect(personnel.$defs.ResearchBudgetCount4).toMatchObject({
      type: "integer",
      minimum: 0,
      maximum: 9999,
    });
  });

  it("reuses the complete research budget inside each subaward with parent-scoped sums", async () => {
    const root = resolve(packageRoot, "dist/forms/rr-subaward-budget");
    const schema = JSON.parse(await readFile(resolve(root, "schema.json"), "utf8"));
    const ui = JSON.parse(await readFile(resolve(root, "sgg/ui-schema.json"), "utf8"));
    const rules = JSON.parse(await readFile(resolve(root, "sgg/rule-schema.json"), "utf8"));

    expect(schema.properties.budgetAttachments).toMatchObject({
      type: "array",
      maxItems: 10,
      items: { $ref: "../../question-bank/budget/research/details/schema.json" },
    });

    const allObjects = (value: unknown): Record<string, unknown>[] => {
      if (Array.isArray(value)) return value.flatMap(allObjects);
      if (!value || typeof value !== "object") return [];
      const object = value as Record<string, unknown>;
      return [object, ...Object.values(object).flatMap(allObjects)];
    };
    expect(allObjects(ui).filter((node) => node.type === "fieldList")).toHaveLength(6);
    expect(
      allObjects(rules).filter((node) =>
        Object.prototype.hasOwnProperty.call(node, "gg_pre_population")
      ),
    ).toHaveLength(56);
    expect(
      rules.budgetAttachments.budgetSummary.cumulativeDomesticTravelCosts.gg_pre_population.fields,
    ).toEqual(["@PARENT.budgetYear[*].travel.domesticTravelCost"]);
  });

  it("inherits the complete rule graph in the ten-year subaward profile", async () => {
    const root = resolve(packageRoot, "dist/forms/rr-subaward-budget-10yr-30");
    const ui = JSON.parse(await readFile(resolve(root, "sgg/ui-schema.json"), "utf8"));
    const rules = JSON.parse(await readFile(resolve(root, "sgg/rule-schema.json"), "utf8"));

    const allObjects = (value: unknown): Record<string, unknown>[] => {
      if (Array.isArray(value)) return value.flatMap(allObjects);
      if (!value || typeof value !== "object") return [];
      const object = value as Record<string, unknown>;
      return [object, ...Object.values(object).flatMap(allObjects)];
    };

    expect(allObjects(ui).filter((node) => node.type === "fieldList")).toHaveLength(6);
    expect(
      allObjects(rules).filter((node) =>
        Object.prototype.hasOwnProperty.call(node, "gg_pre_population")
      ),
    ).toHaveLength(56);
    expect(
      rules.budgetAttachments.budgetSummary.cumulativeDomesticTravelCosts.gg_pre_population.fields,
    ).toEqual(["@PARENT.budgetYear[*].travel.domesticTravelCost"]);
  });

  it("keeps Key Contacts field-list presentation parity declarative", async () => {
    const ui = JSON.parse(
      await readFile(
        resolve(packageRoot, "dist/forms/key-contacts/sgg/ui-schema.json"),
        "utf8",
      ),
    );
    const section = ui.find((node: { name?: string }) => node.name === "keyContacts");
    const list = section.children.find(
      (node: { type?: string; name?: string }) =>
        node.type === "fieldList" && node.name === "keyContacts",
    );

    expect(section).not.toHaveProperty("description");
    expect(list.hideFieldListHeading).toBe(true);
  });

  it("emits SF-424A source guidance without changing Column G semantics", async () => {
    const root = resolve(packageRoot, "dist/forms/sf424a");
    const schema = JSON.parse(await readFile(resolve(root, "schema.json"), "utf8"));
    const ui = JSON.parse(await readFile(resolve(root, "sgg/ui-schema.json"), "utf8"));
    const rules = JSON.parse(await readFile(resolve(root, "sgg/rule-schema.json"), "utf8"));
    const budgetSummary = JSON.parse(
      await readFile(
        resolve(packageRoot, "dist/question-bank/budget/summary/schema.json"),
        "utf8",
      ),
    );

    expect(ui[0]).toMatchObject({
      name: "SectionA",
      label: "Section A - Budget summary",
    });
    expect(ui[0].description).toContain("Column G is entered manually");
    expect(schema.$defs.ActivityLineItem.properties.activityTitle).toMatchObject({
      title: "Grant program, function, or activity",
    });
    expect(schema.properties.activityLineItems.items.properties.activityTitle).toMatchObject({
      description: expect.stringContaining("Assistance Listing title"),
    });
    expect(budgetSummary.properties.totalAmount).toMatchObject({
      title: "Total",
      description: "Enter the total budgeted amount for this row. This value is not calculated automatically.",
    });
    expect(rules.activityLineItems).not.toHaveProperty("budgetSummary.totalAmount");
    expect(
      rules.totalBudgetSummary.totalAmount.gg_pre_population.fields,
    ).toEqual(["activityLineItems[*].budgetSummary.totalAmount"]);
    expect(JSON.stringify({ schema, ui, rules })).not.toMatch(/(?:is|equals) the sum of (?:Columns? )?C(?: through|-)[ ]?F/i);
  });

  it.each([
    [
      "project-narrative-attachments",
      "Project Narrative Files",
      "projectNarrativeFiles",
      "1. Project Narrative File(s)",
      "project/narrative",
    ],
    [
      "budget-narrative-attachments",
      "Budget Narrative Files",
      "budgetNarrativeFiles",
      "1. Budget Narrative File(s)",
      "budget/narrative",
    ],
    [
      "other-narrative-attachments",
      "Other Narrative Files",
      "otherNarrativeFiles",
      "1. Other Narrative File(s)",
      "application/other-narrative",
    ],
  ])(
    "emits %s as a role-specific use of the shared attachment question",
    async (formId, title, sectionName, sectionLabel, questionId) => {
      const root = resolve(packageRoot, `dist/forms/${formId}`);
      const schema = JSON.parse(await readFile(resolve(root, "schema.json"), "utf8"));
      const ui = JSON.parse(
        await readFile(resolve(root, "sgg/ui-schema.json"), "utf8"),
      );
      const rules = JSON.parse(
        await readFile(resolve(root, "sgg/rule-schema.json"), "utf8"),
      );

      expect(schema.properties.attachments).toMatchObject({
        type: "array",
        title,
        description: "At least one file must be attached",
        minItems: 1,
        maxItems: 100,
        items: { $ref: `../../question-bank/${questionId}/schema.json` },
      });

      const semanticIndex = JSON.parse(
        await readFile(resolve(packageRoot, `dist/question-bank/${questionId}/index.json`), "utf8"),
      );
      expect(semanticIndex).toMatchObject({
        classification: "semanticQuestion",
        composes: ["generics/attachment"],
      });
      const mechanismIndex = JSON.parse(
        await readFile(resolve(packageRoot, "dist/question-bank/generics/attachment/index.json"), "utf8"),
      );
      expect(mechanismIndex).toMatchObject({
        classification: "captureMechanism",
        composes: [],
      });
      expect(ui).toEqual([
        {
          type: "section",
          name: sectionName,
          label: sectionLabel,
          children: [
            {
              type: "field",
              definition: "/properties/attachments",
              widget: "AttachmentArray",
            },
          ],
        },
      ]);
      expect(rules).toEqual({
        attachments: { gg_validation: { rule: "attachment" } },
      });
    },
  );
});

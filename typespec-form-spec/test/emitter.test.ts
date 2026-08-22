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
    expect(calculations).toHaveLength(30);
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
    ).toBe(15);

    const period = JSON.parse(
      await readFile(
        resolve(packageRoot, "dist/question-bank/budget/research/period/schema.json"),
        "utf8",
      ),
    );
    expect(period.properties.directCosts.readOnly).toBe(true);
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

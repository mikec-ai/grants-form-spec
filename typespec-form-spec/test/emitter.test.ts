import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");

describe("SGG UI emission", () => {
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
    ],
    [
      "budget-narrative-attachments",
      "Budget Narrative Files",
      "budgetNarrativeFiles",
      "1. Budget Narrative File(s)",
    ],
    [
      "other-narrative-attachments",
      "Other Narrative Files",
      "otherNarrativeFiles",
      "1. Other Narrative File(s)",
    ],
  ])(
    "emits %s as a role-specific use of the shared attachment question",
    async (formId, title, sectionName, sectionLabel) => {
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
        items: { $ref: "../../question-bank/generics/attachment/schema.json" },
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

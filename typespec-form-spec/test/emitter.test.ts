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
});

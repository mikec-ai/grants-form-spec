import Ajv2020, { type ValidateFunction } from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { readdir, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { beforeAll, describe, expect, it } from "vitest";

const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const contractRoot = resolve(packageRoot, "contract/v1");
const emittedQuestionsRoot = resolve(packageRoot, "dist/question-bank");
const emittedFormsRoot = resolve(packageRoot, "dist/forms");

async function json(path: string): Promise<unknown> {
  return JSON.parse(await readFile(path, "utf8"));
}

async function schemaArtifacts(root: string): Promise<string[]> {
  const found: string[] = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) found.push(...(await schemaArtifacts(path)));
    if (entry.isFile() && entry.name === "schema.json") found.push(path);
  }
  return found;
}

async function namedArtifacts(root: string, name: string): Promise<string[]> {
  const found: string[] = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) found.push(...(await namedArtifacts(path, name)));
    if (entry.isFile() && entry.name === name) found.push(path);
  }
  return found;
}

describe("artifact contract v1", () => {
  let validateQuestion: ValidateFunction;
  let validateForm: ValidateFunction;
  let validateUi: ValidateFunction;
  let validateIndex: ValidateFunction;
  let validatePackage: ValidateFunction;
  let validateEvidence: ValidateFunction;
  let validateGrantsGovXmlProfile: ValidateFunction;
  let validatePolicyContent: ValidateFunction;
  let validatePolicyBinding: ValidateFunction;

  beforeAll(async () => {
    const ajv = new Ajv2020({ allErrors: true, strict: true });
    addFormats(ajv);
    validateQuestion = ajv.compile(
      await json(resolve(contractRoot, "question.schema.json")),
    );
    validateForm = ajv.compile(await json(resolve(contractRoot, "form.schema.json")));
    validateUi = ajv.compile(await json(resolve(contractRoot, "ui-schema.schema.json")));
    validateIndex = ajv.compile(await json(resolve(contractRoot, "block-index.schema.json")));
    validatePackage = ajv.compile(await json(resolve(contractRoot, "form-package.schema.json")));
    validateEvidence = ajv.compile(await json(resolve(contractRoot, "evidence.schema.json")));
    validateGrantsGovXmlProfile = ajv.compile(
      await json(resolve(contractRoot, "grants-gov-xml-profile.schema.json")),
    );
    validatePolicyContent = ajv.compile(
      await json(resolve(contractRoot, "policy-content.schema.json")),
    );
    validatePolicyBinding = ajv.compile(
      await json(resolve(contractRoot, "policy-binding.schema.json")),
    );
  });

  it("accepts a hand-authored question artifact without TypeSpec", async () => {
    const fixture = await json(
      resolve(contractRoot, "conformance/question.valid.json"),
    );

    expect(validateQuestion(fixture), JSON.stringify(validateQuestion.errors)).toBe(
      true,
    );
  });

  it("rejects an otherwise valid schema without portable question identity", async () => {
    const fixture = await json(
      resolve(contractRoot, "conformance/question.invalid.json"),
    );

    expect(validateQuestion(fixture)).toBe(false);
    expect(validateQuestion.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ keyword: "required", params: { missingProperty: "$id" } }),
      ]),
    );
  });

  it("accepts every emitted question schema through the same artifact contract", async () => {
    const artifacts = await schemaArtifacts(emittedQuestionsRoot);

    expect(artifacts.length).toBeGreaterThan(0);
    for (const artifact of artifacts) {
      const candidate = await json(artifact);
      expect(
        validateQuestion(candidate),
        `${artifact}: ${JSON.stringify(validateQuestion.errors)}`,
      ).toBe(true);
    }
  });

  it.each([
    ["form", validateFixture("form", () => validateForm)],
    ["ui-schema", validateFixture("ui-schema", () => validateUi)],
    ["block-index", validateFixture("block-index", () => validateIndex)],
    ["form-package", validateFixture("form-package", () => validatePackage)],
    ["evidence", validateFixture("evidence", () => validateEvidence)],
    [
      "grants-gov-xml-profile",
      validateFixture("grants-gov-xml-profile", () => validateGrantsGovXmlProfile),
    ],
  ])("distinguishes the valid and poisoned %s fixtures", async (_name, run) => {
    await run();
  });

  it("accepts all emitted form, UI, index, and package artifacts", async () => {
    const groups: [string[], () => ValidateFunction][] = [
      [await schemaArtifacts(emittedFormsRoot), () => validateForm],
      [
        [
          ...(await namedArtifacts(emittedQuestionsRoot, "ui.json")),
          ...(await namedArtifacts(emittedFormsRoot, "ui.json")),
        ],
        () => validateUi,
      ],
      [
        [
          ...(await namedArtifacts(emittedQuestionsRoot, "index.json")),
          ...(await namedArtifacts(emittedFormsRoot, "index.json")),
        ],
        () => validateIndex,
      ],
      [await namedArtifacts(emittedFormsRoot, "manifest.json"), () => validatePackage],
      [await namedArtifacts(emittedFormsRoot, "evidence.json"), () => validateEvidence],
      [
        await namedArtifacts(emittedFormsRoot, "grants-gov-xml.json"),
        () => validateGrantsGovXmlProfile,
      ],
      [
        await namedArtifacts(emittedFormsRoot, "policy-content.json"),
        () => validatePolicyContent,
      ],
      [
        await namedArtifacts(emittedFormsRoot, "policy-binding.json"),
        () => validatePolicyBinding,
      ],
    ];

    for (const [artifacts, getValidator] of groups) {
      expect(artifacts.length).toBeGreaterThan(0);
      const validator = getValidator();
      for (const artifact of artifacts) {
        const candidate = await json(artifact);
        expect(validator(candidate), `${artifact}: ${JSON.stringify(validator.errors)}`).toBe(true);
      }
    }
  });

  it("keeps delivery-target runtime identity out of every portable manifest", async () => {
    const manifests = await namedArtifacts(emittedFormsRoot, "manifest.json");

    expect(manifests.length).toBeGreaterThan(0);
    for (const artifact of manifests) {
      const candidate = (await json(artifact)) as { form: Record<string, unknown> };
      expect(candidate.form, artifact).not.toHaveProperty("formId");
      expect(candidate.form, artifact).not.toHaveProperty("formType");
      expect(candidate.form, artifact).not.toHaveProperty("sggVersion");
    }
  });

  it("rejects ambiguous Grants.gov XML mapping nodes", async () => {
    const valid = (await json(
      resolve(contractRoot, "conformance/grants-gov-xml-profile.valid.json"),
    )) as {
      mapping: {
        fields: Record<string, Record<string, unknown>>;
      };
    };
    const arrayProfile = structuredClone(valid);
    arrayProfile.mapping.fields.files.fields = {
      stray: { element: "Stray", kind: "value" },
    };

    expect(validateGrantsGovXmlProfile(arrayProfile)).toBe(false);

    const objectProfile = structuredClone(valid);
    objectProfile.mapping.fields.title = {
      element: "Title",
      kind: "object",
      fields: { value: { element: "Value", kind: "value" } },
      items: { fields: { value: { element: "Value", kind: "value" } } },
    };

    expect(validateGrantsGovXmlProfile(objectProfile)).toBe(false);

    const objectContainer = structuredClone(valid);
    objectContainer.mapping.fields.title = {
      element: "Title",
      kind: "object",
      fields: { value: { element: "Value", kind: "value" } },
      container: { element: "Container", namespace: "default" },
    };
    expect(validateGrantsGovXmlProfile(objectContainer)).toBe(false);

    const incompleteContainer = structuredClone(valid);
    incompleteContainer.mapping.fields.title = {
      element: "Title",
      kind: "value",
      container: { element: "Container" },
    };
    expect(validateGrantsGovXmlProfile(incompleteContainer)).toBe(false);

    const groupContainer = structuredClone(valid);
    groupContainer.mapping.fields.title = {
      element: "TitleGroup",
      kind: "group",
      fields: { value: { element: "Title", kind: "value", source: "/title" } },
      container: { element: "Container", namespace: "default" },
    };
    expect(validateGrantsGovXmlProfile(groupContainer)).toBe(false);

    const leafRepeatMode = structuredClone(valid);
    leafRepeatMode.mapping.fields.title.repeatElementPerItem = true;
    expect(validateGrantsGovXmlProfile(leafRepeatMode)).toBe(false);

    const repeatWithoutItemElement = structuredClone(valid);
    repeatWithoutItemElement.mapping.fields.files.repeatElementPerItem = true;
    expect(validateGrantsGovXmlProfile(repeatWithoutItemElement)).toBe(false);

    const repeatedOuter = structuredClone(valid);
    repeatedOuter.mapping.fields.files.itemElement = "FileItem";
    repeatedOuter.mapping.fields.files.repeatElementPerItem = true;
    expect(
      validateGrantsGovXmlProfile(repeatedOuter),
      JSON.stringify(validateGrantsGovXmlProfile.errors),
    ).toBe(true);
  });

  it("accepts a portable form package before a legacy consumer id is assigned", async () => {
    const fixture = structuredClone(
      await json(resolve(contractRoot, "conformance/form-package.valid.json")),
    ) as { form: { legacyFormId?: number } };
    delete fixture.form.legacyFormId;

    expect(validatePackage(fixture), JSON.stringify(validatePackage.errors)).toBe(true);
  });

  it("keeps canonical form and native source versions distinct in evidence", async () => {
    const fixture = structuredClone(
      await json(resolve(contractRoot, "conformance/evidence.valid.json")),
    ) as {
      block: { formVersion?: string };
      sources: Array<{ uri: string; nativeVersion?: string | null; version?: string }>;
    };

    fixture.sources[0].uri = "https://example.gov/forms/unversioned-source.xsd";
    fixture.sources[0].nativeVersion = null;
    expect(validateEvidence(fixture), JSON.stringify(validateEvidence.errors)).toBe(true);

    delete fixture.block.formVersion;
    expect(validateEvidence(fixture)).toBe(false);

    fixture.block.formVersion = "2.0";
    delete fixture.sources[0].nativeVersion;
    fixture.sources[0].version = "2.0";
    expect(validateEvidence(fixture)).toBe(false);
  });
});

function validateFixture(name: string, getValidator: () => ValidateFunction) {
  return async () => {
    const validator = getValidator();
    const valid = await json(resolve(contractRoot, `conformance/${name}.valid.json`));
    const invalid = await json(resolve(contractRoot, `conformance/${name}.invalid.json`));
    expect(validator(valid), JSON.stringify(validator.errors)).toBe(true);
    expect(validator(invalid)).toBe(false);
  };
}

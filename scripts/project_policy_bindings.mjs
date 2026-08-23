#!/usr/bin/env node

import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const POLICY_ROOT = resolve(ROOT, "policies");
const BINDING_ROOT = resolve(ROOT, "policy-bindings/forms");
const DIST_FORMS = resolve(ROOT, "dist/forms");

const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

async function jsonFiles(root) {
  try {
    return (await readdir(root)).filter((name) => name.endsWith(".json")).sort();
  } catch (error) {
    if (error.code === "ENOENT") return [];
    throw error;
  }
}

function compile(schema) {
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  addFormats(ajv);
  return ajv.compile(schema);
}

function assertValid(validate, document, path) {
  if (validate(document)) return;
  const detail = validate.errors
    .map((error) => `${error.instancePath || "/"} ${error.message}`)
    .join("; ");
  throw new Error(`${relative(ROOT, path)}: ${detail}`);
}

function assertUnique(values, label, path) {
  const seen = new Set();
  for (const value of values) {
    if (seen.has(value)) throw new Error(`${relative(ROOT, path)}: duplicate ${label} ${value}`);
    seen.add(value);
  }
}

function sectionDescription(section) {
  const parts = [];
  if (section.preamble) parts.push(section.preamble);
  if (section.text) parts.push(section.text);
  if (section.items) {
    parts.push(...section.items.map((item) => `${item.ordinal ?? item.label ?? ""}. ${item.text}`.replace(/^\. /, "")));
  }
  if (section.note) parts.push(section.note);
  return parts.join("\n\n");
}

function projectSggPresentation(ui, policy, binding, path) {
  if (!Array.isArray(ui)) throw new Error(`${relative(ROOT, path)}: SGG UI artifact must be a list`);
  const sections = new Map(policy.sections.map((section) => [section.id, section]));
  const projected = [...ui];
  for (const placement of binding.presentation.sections) {
    const section = sections.get(placement.sectionId);
    if (!section) {
      throw new Error(`${relative(ROOT, path)}: unknown policy section ${placement.sectionId}`);
    }
    const node = {
      type: "section",
      name: placement.name,
      label: placement.label ?? section.title,
      description: sectionDescription(section),
      children: [],
    };
    const index = placement.before
      ? projected.findIndex((candidate) => candidate?.type === "section" && candidate.name === placement.before)
      : -1;
    if (placement.before && index < 0) {
      throw new Error(`${relative(ROOT, path)}: insertion target ${placement.before} does not exist`);
    }
    projected.splice(index < 0 ? projected.length : index, 0, node);
  }
  return projected;
}

async function main() {
  const policyValidate = compile(await readJson(resolve(ROOT, "contract/v1/policy-content.schema.json")));
  const bindingValidate = compile(await readJson(resolve(ROOT, "contract/v1/policy-binding.schema.json")));
  const policies = new Map();

  for (const name of await jsonFiles(POLICY_ROOT)) {
    const path = resolve(POLICY_ROOT, name);
    const policy = await readJson(path);
    assertValid(policyValidate, policy, path);
    assertUnique(policy.sources.map((source) => source.id), "source id", path);
    assertUnique(policy.sections.map((section) => section.id), "section id", path);
    const sourceIds = new Set(policy.sources.map((source) => source.id));
    for (const section of policy.sections) {
      for (const ref of [...section.sourceRefs, ...(section.items ?? []).flatMap((item) => item.sourceRefs)]) {
        if (!sourceIds.has(ref.sourceId)) {
          throw new Error(`${relative(ROOT, path)}: unknown source reference ${ref.sourceId}`);
        }
      }
    }
    const key = `${policy.id}@${policy.version}`;
    if (policies.has(key)) throw new Error(`duplicate policy identity ${key}`);
    policies.set(key, policy);
  }

  let count = 0;
  for (const name of await jsonFiles(BINDING_ROOT)) {
    const path = resolve(BINDING_ROOT, name);
    const binding = await readJson(path);
    assertValid(bindingValidate, binding, path);
    const key = `${binding.policy.id}@${binding.policy.version}`;
    const policy = policies.get(key);
    if (!policy) throw new Error(`${relative(ROOT, path)}: policy ${key} does not exist`);
    const sectionIds = new Set(policy.sections.map((section) => section.id));
    assertUnique(binding.presentation.sections.map((section) => section.sectionId), "placement", path);
    assertUnique(binding.acceptance.fields.map((field) => field.role), "acceptance role", path);
    for (const sectionId of binding.acceptance.attestsTo) {
      if (!sectionIds.has(sectionId)) throw new Error(`${relative(ROOT, path)}: unknown attested section ${sectionId}`);
    }

    const formRoot = resolve(DIST_FORMS, binding.formId);
    const manifestPath = resolve(formRoot, "manifest.json");
    const manifest = await readJson(manifestPath);
    if (manifest.form?.id !== binding.formId) {
      throw new Error(`${relative(ROOT, path)}: formId does not match emitted package`);
    }
    const schema = await readJson(resolve(formRoot, "schema.json"));
    for (const field of binding.acceptance.fields) {
      const segments = field.pointer.slice(1).split("/").map((part) => part.replaceAll("~1", "/").replaceAll("~0", "~"));
      let node = schema;
      for (const segment of segments) {
        if (!node?.properties || !(segment in node.properties)) {
          throw new Error(`${relative(ROOT, path)}: acceptance pointer ${field.pointer} does not resolve`);
        }
        node = node.properties[segment];
      }
    }

    const policyPath = resolve(formRoot, "policy-content.json");
    const bindingPath = resolve(formRoot, "policy-binding.json");
    await mkdir(formRoot, { recursive: true });
    await writeFile(policyPath, `${JSON.stringify(policy, null, 2)}\n`);
    await writeFile(bindingPath, `${JSON.stringify(binding, null, 2)}\n`);

    const uiPath = resolve(formRoot, "sgg/ui-schema.json");
    const ui = projectSggPresentation(await readJson(uiPath), policy, binding, uiPath);
    await writeFile(uiPath, `${JSON.stringify(ui, null, 2)}\n`);
    manifest.artifacts["policy-content.json"] = "generated";
    manifest.artifacts["policy-binding.json"] = "generated";
    await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
    count += 1;
  }

  process.stdout.write(`policy-bindings:\n  status: projected\n  forms: ${count}\n`);
}

await main();

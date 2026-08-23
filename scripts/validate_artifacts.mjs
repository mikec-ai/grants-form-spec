#!/usr/bin/env node

import Ajv2020 from "ajv/dist/2020.js";
import { readFile, readdir } from "node:fs/promises";
import { dirname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const VERSION = "0.1.0";
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CONTRACT = resolve(ROOT, "contract/v1");

class UsageError extends Error {}
class ArtifactError extends Error {
  constructor(message, path) {
    super(message);
    this.path = path;
  }
}

async function readJson(path) {
  try {
    return JSON.parse(await readFile(path, "utf8"));
  } catch (error) {
    throw new ArtifactError(`cannot read JSON: ${error.message}`, path);
  }
}

async function filesBelow(root) {
  const found = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) found.push(...(await filesBelow(path)));
    if (entry.isFile()) found.push(path);
  }
  return found.sort();
}

const formatAjv = (errors) =>
  (errors ?? []).map((error) => `${error.instancePath || "/"} ${error.message}`).join("; ");

function decodePointer(fragment) {
  if (!fragment || fragment === "#") return [];
  if (!fragment.startsWith("#/")) throw new Error(`unsupported JSON Pointer ${fragment}`);
  return fragment.slice(2).split("/").map(
    (part) => decodeURIComponent(part).replaceAll("~1", "/").replaceAll("~0", "~"),
  );
}

function inside(root, path) {
  const rel = relative(root, path);
  return rel !== ".." && !rel.startsWith(`..${sep}`) && !rel.startsWith(sep);
}

function refTarget(from, ref, dist) {
  const [location, rawFragment = ""] = ref.split("#", 2);
  if (/^[a-z][a-z0-9+.-]*:/i.test(location)) return undefined;
  const path = location ? resolve(dirname(from), location) : from;
  if (!inside(dist, path)) throw new ArtifactError(`reference escapes the artifact root: ${ref}`, from);
  return { path, fragment: rawFragment ? `#${rawFragment}` : "#" };
}

async function dereference(state, dist, cache, seen) {
  const { value, path } = state;
  if (!value || typeof value !== "object" || typeof value.$ref !== "string") return state;
  const target = refTarget(path, value.$ref, dist);
  if (!target) return state;
  return resolvePointer(target.path, target.fragment, dist, cache, seen, true);
}

async function resolveSteps(state, steps, dist, cache, seen) {
  for (const step of steps) {
    state = await dereference(state, dist, cache, seen);
    const { value, path } = state;
    if (value && typeof value === "object" && step in value) {
      state = { value: value[step], path };
      continue;
    }
    if (value && typeof value === "object" && Array.isArray(value.allOf)) {
      let found;
      for (const branch of value.allOf) {
        try {
          found = await resolveSteps({ value: branch, path }, [step], dist, cache, new Set(seen));
          break;
        } catch {
          // Try the next composed branch.
        }
      }
      if (found !== undefined) {
        state = found;
        continue;
      }
    }
    throw new ArtifactError(`schema path does not contain ${step}`, path);
  }
  return state;
}

async function resolvePointer(path, fragment, dist, cache, seen = new Set(), returnState = false) {
  const key = `${path}${fragment}`;
  if (seen.has(key)) throw new ArtifactError(`reference cycle while resolving ${fragment}`, path);
  seen.add(key);
  const doc = cache.get(path) ?? (await readJson(path));
  cache.set(path, doc);
  let state = await resolveSteps({ value: doc, path }, decodePointer(fragment), dist, cache, seen);
  state = await dereference(state, dist, cache, seen);
  return returnState ? state : state.value;
}

function walk(value, visit) {
  visit(value);
  if (Array.isArray(value)) {
    for (const item of value) walk(item, visit);
  } else if (value && typeof value === "object") {
    for (const child of Object.values(value)) walk(child, visit);
  }
}

async function validators() {
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  const out = new Map();
  for (const name of [
    "question",
    "form",
    "ui-schema",
    "block-index",
    "form-package",
    "evidence",
    "grants-gov-xml-profile",
  ]) {
    out.set(name, ajv.compile(await readJson(resolve(CONTRACT, `${name}.schema.json`))));
  }
  return out;
}

export async function validateArtifactGraph(inputDist) {
  const dist = resolve(inputDist);
  const allFiles = await filesBelow(dist);
  const jsonFiles = allFiles.filter((path) => path.endsWith(".json"));
  const validate = await validators();
  const cache = new Map();
  const indexes = jsonFiles.filter((path) => path.endsWith(`${sep}index.json`));
  const indexById = new Map();
  for (const path of indexes) {
    const index = await readJson(path);
    if (indexById.has(index.id)) {
      throw new ArtifactError(`duplicate block id ${index.id}`, path);
    }
    indexById.set(index.id, { index, path });
  }

  for (const indexPath of indexes) {
    const dir = dirname(indexPath);
    const index = await readJson(indexPath);
    const schemaPath = resolve(dir, "schema.json");
    const uiPath = resolve(dir, "ui.json");
    const schema = await readJson(schemaPath);
    const ui = await readJson(uiPath);
    cache.set(indexPath, index);
    cache.set(schemaPath, schema);
    cache.set(uiPath, ui);

    const location = inside(resolve(dist, "forms"), indexPath) ? "form" : "question";
    const expectedRoot = resolve(dist, location === "form" ? "forms" : "question-bank");
    const expectedId = relative(expectedRoot, dir).split(sep).join("/");

    const indexValidator = validate.get("block-index");
    if (!indexValidator(index)) {
      throw new ArtifactError(`block index contract failed: ${formatAjv(indexValidator.errors)}`, indexPath);
    }
    if (index.kind !== location || index.id !== expectedId) {
      throw new ArtifactError(`block identity ${index.kind}:${index.id} does not match ${location}:${expectedId}`, indexPath);
    }
    if (location === "question") {
      for (const composedId of index.composes) {
        const composed = indexById.get(composedId);
        if (!composed || composed.index.kind !== "question") {
          throw new ArtifactError(`composes unknown question ${composedId}`, indexPath);
        }
      }
    }

    const schemaValidator = validate.get(location);
    if (!schemaValidator(schema)) {
      throw new ArtifactError(`${location} schema contract failed: ${formatAjv(schemaValidator.errors)}`, schemaPath);
    }
    if (schema.$id !== `${index.id}/schema.json`) {
      throw new ArtifactError(`schema $id ${schema.$id} does not match block ${index.id}`, schemaPath);
    }

    const uiValidator = validate.get("ui-schema");
    if (!uiValidator(ui)) {
      throw new ArtifactError(`UI schema contract failed: ${formatAjv(uiValidator.errors)}`, uiPath);
    }
    const scopes = [];
    walk(ui, (node) => {
      if (node && typeof node === "object" && typeof node.scope === "string") scopes.push(node.scope);
    });
    for (const scope of scopes) await resolvePointer(schemaPath, scope, dist, cache);

    const refs = [];
    walk(schema, (node) => {
      if (node && typeof node === "object" && typeof node.$ref === "string") refs.push(node.$ref);
    });
    for (const ref of refs) {
      const target = refTarget(schemaPath, ref, dist);
      if (target) await resolvePointer(target.path, target.fragment, dist, cache);
    }

    const evidencePath = resolve(dir, "evidence.json");
    if (jsonFiles.includes(evidencePath)) {
      const evidence = await readJson(evidencePath);
      const evidenceValidator = validate.get("evidence");
      if (!evidenceValidator(evidence)) {
        throw new ArtifactError(`evidence contract failed: ${formatAjv(evidenceValidator.errors)}`, evidencePath);
      }
      if (evidence.block.id !== index.id || evidence.block.kind !== index.kind) {
        throw new ArtifactError("evidence block identity does not match its index", evidencePath);
      }
      const sourceIds = new Set(evidence.sources.map((source) => source.id));
      if (sourceIds.size !== evidence.sources.length) {
        throw new ArtifactError("evidence source ids must be unique", evidencePath);
      }
      for (const mapping of evidence.semanticReview.mappings) {
        if (!sourceIds.has(mapping.sourceId)) {
          throw new ArtifactError(`semantic mapping names unknown source ${mapping.sourceId}`, evidencePath);
        }
        await resolvePointer(schemaPath, mapping.canonicalPointer, dist, cache);
      }
    }

    if (location === "form") {
      const manifestPath = resolve(dir, "manifest.json");
      const manifest = await readJson(manifestPath);
      const manifestValidator = validate.get("form-package");
      if (!manifestValidator(manifest)) {
        throw new ArtifactError(`form package contract failed: ${formatAjv(manifestValidator.errors)}`, manifestPath);
      }
      if (manifest.form.id !== index.id) {
        throw new ArtifactError(`manifest form id ${manifest.form.id} does not match ${index.id}`, manifestPath);
      }
      for (const artifact of Object.keys(manifest.artifacts)) {
        const target = resolve(dir, artifact);
        if (!inside(dir, target) || !jsonFiles.includes(target)) {
          throw new ArtifactError(`manifest artifact does not exist: ${artifact}`, manifestPath);
        }
      }

      const xmlProfilePath = resolve(dir, "targets/grants-gov-xml.json");
      if (jsonFiles.includes(xmlProfilePath)) {
        const profile = await readJson(xmlProfilePath);
        const profileValidator = validate.get("grants-gov-xml-profile");
        if (!profileValidator(profile)) {
          throw new ArtifactError(
            `Grants.gov XML profile contract failed: ${formatAjv(profileValidator.errors)}`,
            xmlProfilePath,
          );
        }
        if (profile.formId !== index.id) {
          throw new ArtifactError("Grants.gov XML profile formId does not match its form", xmlProfilePath);
        }
        if (manifest.artifacts["targets/grants-gov-xml.json"] !== "generated") {
          throw new ArtifactError(
            "Grants.gov XML profile is not declared as a generated package artifact",
            manifestPath,
          );
        }
        const nodes = [...mappingNodes(profile.mapping.fields)];
        for (const node of nodes) {
          if (node.namespace && !(node.namespace in profile.namespaces)) {
            throw new ArtifactError(`mapping names unknown namespace ${node.namespace}`, xmlProfilePath);
          }
          if (node.itemNamespace && !(node.itemNamespace in profile.namespaces)) {
            throw new ArtifactError(
              `mapping names unknown item namespace ${node.itemNamespace}`,
              xmlProfilePath,
            );
          }
          if (node.container?.namespace && !(node.container.namespace in profile.namespaces)) {
            throw new ArtifactError(
              `mapping container names unknown namespace ${node.container.namespace}`,
              xmlProfilePath,
            );
          }
        }
        if (nodes.some((node) => node.kind === "attachment") && !profile.attachment) {
          throw new ArtifactError(
            "XML profile maps attachments without declaring their wire fields",
            xmlProfilePath,
          );
        }
        for (const field of Object.values(profile.attachment?.fields ?? {})) {
          if (!(field.namespace in profile.namespaces)) {
            throw new ArtifactError(
              `attachment wire field names unknown namespace ${field.namespace}`,
              xmlProfilePath,
            );
          }
        }
        if (!(profile.root.namespacePrefix in profile.namespaces)) {
          const rootNamespace = profile.namespaces.default;
          if (!rootNamespace) {
            throw new ArtifactError("XML profile has no root namespace", xmlProfilePath);
          }
        }
        await validateMappingCoverage(
          profile.mapping.fields,
          { value: schema, path: schemaPath },
          dist,
          cache,
          xmlProfilePath,
        );
      }
    }
  }

  if (!indexes.length) throw new ArtifactError("no block index artifacts found", dist);
  return { blocks: indexes.length, artifacts: jsonFiles.length };
}

function* mappingNodes(fields) {
  for (const node of Object.values(fields ?? {})) {
    yield node;
    if (node.kind === "object" || node.kind === "group") yield* mappingNodes(node.fields);
    if (node.kind === "array") {
      if (node.items?.fields) yield* mappingNodes(node.items.fields);
      if (node.items?.node) yield node.items.node;
    }
  }
}

async function schemaProperties(state, dist, cache, seen = new Set()) {
  if (Array.isArray(state)) {
    const combined = new Map();
    for (const branch of state) {
      for (const [name, children] of await schemaProperties(branch, dist, cache, seen)) {
        combined.set(name, [...(combined.get(name) ?? []), ...children]);
      }
    }
    return combined;
  }
  const { value, path } = state;
  if (!value || typeof value !== "object") return new Map();
  const marker = `${path}:${JSON.stringify(value.$ref ?? Object.keys(value.properties ?? {}))}`;
  if (seen.has(marker)) return new Map();
  const nextSeen = new Set([...seen, marker]);
  const out = new Map();

  if (typeof value.$ref === "string") {
    const target = refTarget(path, value.$ref, dist);
    if (target) {
      const resolved = await resolvePointer(
        target.path,
        target.fragment,
        dist,
        cache,
        new Set(),
        true,
      );
      for (const [name, children] of await schemaProperties(resolved, dist, cache, nextSeen)) {
        out.set(name, [...(out.get(name) ?? []), ...children]);
      }
    }
  }
  for (const branch of value.allOf ?? []) {
    const branchState = { value: branch, path };
    for (const [name, children] of await schemaProperties(branchState, dist, cache, nextSeen)) {
      out.set(name, [...(out.get(name) ?? []), ...children]);
    }
  }
  for (const [name, child] of Object.entries(value.properties ?? {})) {
    out.set(name, [...(out.get(name) ?? []), { value: child, path }]);
  }
  return out;
}

async function schemaItems(state, dist, cache, seen = new Set()) {
  if (Array.isArray(state)) {
    const combined = [];
    for (const branch of state) {
      const found = await schemaItems(branch, dist, cache, seen);
      if (found) combined.push(...(Array.isArray(found) ? found : [found]));
    }
    return combined.length ? combined : undefined;
  }
  const { value, path } = state;
  if (!value || typeof value !== "object") return undefined;
  const marker = `${path}:items:${value.$ref ?? "inline"}`;
  if (seen.has(marker)) return undefined;
  const nextSeen = new Set([...seen, marker]);
  if (value.items && typeof value.items === "object") return { value: value.items, path };
  if (typeof value.$ref === "string") {
    const target = refTarget(path, value.$ref, dist);
    if (target) {
      const resolved = await resolvePointer(
        target.path,
        target.fragment,
        dist,
        cache,
        new Set(),
        true,
      );
      const found = await schemaItems(resolved, dist, cache, nextSeen);
      if (found) return found;
    }
  }
  for (const branch of value.allOf ?? []) {
    const found = await schemaItems({ value: branch, path }, dist, cache, nextSeen);
    if (found) return found;
  }
  return undefined;
}

async function validateSourcePointer(source, rootSchemaState, dist, cache, profilePath) {
  if (typeof source !== "string" || !source.startsWith("/")) {
    throw new ArtifactError(`XML mapping source is not an absolute JSON pointer: ${source}`, profilePath);
  }
  let states = [rootSchemaState];
  for (const step of decodePointer(`#${source}`)) {
    const next = [];
    for (const state of states) {
      const properties = await schemaProperties(state, dist, cache);
      next.push(...(properties.get(step) ?? []));
    }
    if (!next.length) {
      throw new ArtifactError(`XML mapping source does not resolve: ${source}`, profilePath);
    }
    states = next;
  }
}

async function groupSources(fields, rootSchemaState, dist, cache, profilePath) {
  const sources = [];
  for (const node of Object.values(fields)) {
    if (node.kind === "group") {
      sources.push(...await groupSources(node.fields, rootSchemaState, dist, cache, profilePath));
    } else if (node.source) {
      await validateSourcePointer(node.source, rootSchemaState, dist, cache, profilePath);
      sources.push(node.source);
    } else {
      throw new ArtifactError("XML group child must declare an absolute source", profilePath);
    }
  }
  return sources;
}

function sourcePropertyAt(source, at) {
  const sourceSteps = decodePointer(`#${source}`);
  const atSteps = at ? at.replaceAll("[*]", "").split(".") : [];
  if (!atSteps.every((step, index) => sourceSteps[index] === step)) return undefined;
  return sourceSteps[atSteps.length];
}

async function validateMappingCoverage(
  fields,
  schemaState,
  dist,
  cache,
  profilePath,
  at = "",
  rootSchemaState = schemaState,
) {
  const properties = await schemaProperties(schemaState, dist, cache);
  const mapped = new Set(Object.entries(fields)
    .filter(([, node]) => node.kind !== "group")
    .map(([name]) => name));
  for (const node of Object.values(fields).filter((candidate) => candidate.kind === "group")) {
    for (const source of await groupSources(
      node.fields, rootSchemaState, dist, cache, profilePath,
    )) {
      const property = sourcePropertyAt(source, at);
      if (property) mapped.add(property);
    }
  }
  const available = new Set(properties.keys());
  const missing = [...available].filter((name) => !mapped.has(name)).sort();
  const unknown = [...mapped].filter((name) => !available.has(name)).sort();
  if (missing.length || unknown.length) {
    throw new ArtifactError(
      `XML mapping coverage mismatch at ${at || "<root>"}; missing=${JSON.stringify(missing)} unknown=${JSON.stringify(unknown)}`,
      profilePath,
    );
  }
  for (const [name, node] of Object.entries(fields)) {
    const child = properties.get(name);
    const childPath = at ? `${at}.${name}` : name;
    if (node.kind === "object") {
      await validateMappingCoverage(
        node.fields, child, dist, cache, profilePath, childPath, rootSchemaState,
      );
    }
    if (node.kind === "array") {
      const items = await schemaItems(child, dist, cache);
      if (!items) {
        throw new ArtifactError(`XML array mapping has no schema items at ${childPath}`, profilePath);
      }
      if (node.items.fields) {
        await validateMappingCoverage(
          node.items.fields,
          items,
          dist,
          cache,
          profilePath,
          `${childPath}[*]`,
          rootSchemaState,
        );
      } else if (node.items.node.kind === "object") {
        await validateMappingCoverage(
          node.items.node.fields,
          items,
          dist,
          cache,
          profilePath,
          `${childPath}[*]`,
          rootSchemaState,
        );
      }
    }
  }
}

function parseArgs(argv) {
  let dist = resolve(ROOT, "dist");
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (["-v", "-V", "--version"].includes(arg) && argv.length === 1) return { version: true };
    if (arg === "--help") return { help: true };
    if (arg === "--dist") {
      if (!argv[i + 1] || argv[i + 1].startsWith("-")) throw new UsageError("--dist requires a path");
      dist = resolve(argv[++i]);
      continue;
    }
    throw new UsageError(`unknown argument ${arg}`);
  }
  return { dist };
}

const help = () =>
  "usage:\n  command: node scripts/validate_artifacts.mjs [--dist <path>]\nflags[3]{name,description}:\n  --dist,Artifact directory (default: dist)\n  --help,Show this help\n  -v | -V | --version,Show the validator version";

async function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    if (args.version) {
      process.stdout.write(`${VERSION}\n`);
      return 0;
    }
    if (args.help) {
      process.stdout.write(`${help()}\n`);
      return 0;
    }
    const result = await validateArtifactGraph(args.dist);
    process.stdout.write(`validation:\n  status: passed\n  blocks: ${result.blocks}\n  artifacts: ${result.artifacts}\n`);
    return 0;
  } catch (error) {
    const usage = error instanceof UsageError;
    const path = error.path ? `\n  path: ${JSON.stringify(relative(ROOT, error.path))}` : "";
    process.stdout.write(`error:\n  code: ${usage ? "usage_error" : "artifact_invalid"}\n  message: ${JSON.stringify(error.message)}${path}\nhelp[1]: ${usage ? "Run node scripts/validate_artifacts.mjs --help" : "Fix the named artifact and rerun validation"}\n`);
    return usage ? 2 : 1;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = await main();
}

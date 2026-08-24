#!/usr/bin/env node

import Ajv2020 from "ajv/dist/2020.js";
import { createHash } from "node:crypto";
import { readFile, readdir, writeFile } from "node:fs/promises";
import { dirname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const VERSION = "0.1.0";
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CONTRACT = resolve(ROOT, "contract/v1/response-normalization.schema.json");

class UsageError extends Error {}

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function jsonFiles(root) {
  const found = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) found.push(...await jsonFiles(path));
    if (entry.isFile() && entry.name.endsWith(".json")) found.push(path);
  }
  return found.sort();
}

function inside(root, path) {
  const rel = relative(root, path);
  return rel !== ".." && !rel.startsWith(`..${sep}`) && !rel.startsWith(sep);
}

function decodePointer(pointer) {
  if (!pointer.startsWith("/") || pointer === "/") {
    throw new Error(`normalization path must be a non-root RFC 6901 pointer: ${pointer}`);
  }
  return pointer.slice(1).split("/").map((token) => {
    if (/~(?![01])/u.test(token)) throw new Error(`normalization path has invalid escape: ${pointer}`);
    return token.replaceAll("~1", "/").replaceAll("~0", "~");
  });
}

function decodeFragment(fragment, reference) {
  if (!fragment.startsWith("/")) throw new Error(`unsupported schema reference: ${reference}`);
  return fragment.slice(1).split("/").map((token) =>
    decodeURIComponent(token).replaceAll("~1", "/").replaceAll("~0", "~"));
}

function referenceTarget(fromPath, reference, dist) {
  const [location, fragment = ""] = reference.split("#", 2);
  if (/^[a-z][a-z0-9+.-]*:/iu.test(location)) {
    throw new Error(`external schema reference is not supported: ${reference}`);
  }
  const path = location ? resolve(dirname(fromPath), location) : fromPath;
  if (!inside(dist, path)) throw new Error(`schema reference escapes artifact root: ${reference}`);
  return { path, tokens: fragment ? decodeFragment(fragment, reference) : [] };
}

async function referenceState(state, dist, cache) {
  const target = referenceTarget(state.path, state.value.$ref, dist);
  let value = cache.get(target.path);
  if (!value) {
    value = await json(target.path);
    cache.set(target.path, value);
  }
  for (const token of target.tokens) {
    if (!value || typeof value !== "object" || !(token in value)) {
      throw new Error(`schema reference does not resolve: ${state.value.$ref}`);
    }
    value = value[token];
  }
  return { value, path: target.path };
}

async function schemaLayers(states, dist, cache) {
  const out = [];
  const queue = [...states];
  const seen = new Set();
  while (queue.length) {
    const state = queue.shift();
    if (!state?.value || typeof state.value !== "object" || Array.isArray(state.value)) continue;
    const identity = `${state.path}:${JSON.stringify(state.value)}`;
    if (seen.has(identity)) continue;
    seen.add(identity);
    if (typeof state.value.$ref === "string") queue.push(await referenceState(state, dist, cache));
    for (const branch of state.value.allOf ?? []) queue.push({ value: branch, path: state.path });
    out.push(state);
  }
  return out;
}

function assertNoAmbiguousComposition(layers, pointer) {
  for (const { value } of layers) {
    if (value.anyOf || value.oneOf || value.not || value.if || value.then || value.else) {
      throw new Error(`${pointer} uses unsupported conditional or alternative schema composition`);
    }
  }
}

async function validateTarget(schemaPath, pointer, dist, cache) {
  const tokens = decodePointer(pointer);
  let root = cache.get(schemaPath);
  if (!root) {
    root = await json(schemaPath);
    cache.set(schemaPath, root);
  }
  let states = [{ value: root, path: schemaPath }];

  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    const layers = await schemaLayers(states, dist, cache);
    assertNoAmbiguousComposition(layers, pointer);
    if (layers.some(({ value }) => value.type === "array" || value.items)) {
      throw new Error(`${pointer} traverses an array; v1 accepts exact object-property paths only`);
    }
    if (index === tokens.length - 1 && layers.some(({ value }) =>
      Array.isArray(value.required) && value.required.includes(token))) {
      throw new Error(`${pointer} targets a required property`);
    }
    const properties = layers.flatMap(({ value, path }) =>
      value.properties && Object.hasOwn(value.properties, token)
        ? [{ value: value.properties[token], path }]
        : []);
    if (!properties.length) throw new Error(`${pointer} does not resolve to an exact schema property`);
    states = properties;
  }

  const leaf = await schemaLayers(states, dist, cache);
  assertNoAmbiguousComposition(leaf, pointer);
  if (leaf.some(({ value }) => value.type === "array" || value.items)) {
    throw new Error(`${pointer} targets an array, not a scalar string`);
  }
  const types = leaf.flatMap(({ value }) => value.type === undefined
    ? []
    : Array.isArray(value.type) ? value.type : [value.type]);
  if (!types.includes("string") || types.some((type) => type !== "string")) {
    throw new Error(`${pointer} must resolve to a non-null scalar string`);
  }
  const minima = leaf.flatMap(({ value }) =>
    Number.isInteger(value.minLength) ? [value.minLength] : []);
  if (!minima.length || Math.max(...minima) < 1) {
    throw new Error(`${pointer} must reject a present empty string in the canonical schema`);
  }
}

export async function validateResponseNormalization(
  document,
  { schemaPath, evidence, dist, cache = new Map(), context = "response-normalization.json" },
) {
  const evidenceById = new Map();
  for (const record of evidence.responseNormalizationEvidence ?? []) {
    if (evidenceById.has(record.id)) {
      throw new Error(`${context}: duplicate normalization evidence id ${record.id}`);
    }
    evidenceById.set(record.id, record);
  }
  const sourcesById = new Map();
  for (const source of evidence.sources ?? []) {
    if (sourcesById.has(source.id)) {
      throw new Error(`${context}: duplicate evidence source id ${source.id}`);
    }
    sourcesById.set(source.id, source);
  }
  const paths = new Set();
  for (const operation of document.operations) {
    if (paths.has(operation.path)) {
      throw new Error(`${context}: duplicate normalization path ${operation.path}`);
    }
    paths.add(operation.path);
    const evidenceRecord = evidenceById.get(operation.evidenceRef);
    if (!evidenceRecord) throw new Error(`${context}: unresolved evidenceRef ${operation.evidenceRef}`);
    if (evidenceRecord.reviewStatus !== "reviewed" ||
        evidenceRecord.canonicalPath !== operation.path ||
        evidenceRecord.operation !== operation.operation) {
      throw new Error(`${context}: evidenceRef ${operation.evidenceRef} ` +
        "does not exactly review this path and operation");
    }
    for (const citation of evidenceRecord.sourceEvidence) {
      const source = sourcesById.get(citation.sourceId);
      if (!source) {
        throw new Error(`${context}: response normalization ${evidenceRecord.id} ` +
          `names missing source ${citation.sourceId}`);
      }
      if (evidenceRecord.authority === "official_source" && source.type === "implementation") {
        throw new Error(`${context}: response normalization ${evidenceRecord.id} ` +
          `claims official_source authority from implementation source ${citation.sourceId}`);
      }
    }
    await validateTarget(schemaPath, operation.path, resolve(dist), cache);
  }
}

const sha256 = (value) => createHash("sha256").update(value).digest("hex");

export async function projectResponseNormalizations({ normalizationRoot, dist }) {
  normalizationRoot = resolve(normalizationRoot);
  dist = resolve(dist);
  const formRoot = resolve(dist, "forms");
  const contract = await json(CONTRACT);
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  const validate = ajv.compile(contract);
  const files = await jsonFiles(normalizationRoot);
  const cache = new Map();
  const declarations = [];
  const formIds = new Map();
  for (const sourcePath of files) {
    const document = await json(sourcePath);
    if (!validate(document)) {
      const detail = validate.errors.map((error) =>
        `${error.instancePath || "/"} ${error.message}`).join("; ");
      throw new Error(`${relative(ROOT, sourcePath)}: ${detail}`);
    }
    const prior = formIds.get(document.form.id);
    if (prior) {
      throw new Error(
        `duplicate response normalization declarations for ${document.form.id}: ` +
        `${relative(ROOT, prior)} and ${relative(ROOT, sourcePath)}`,
      );
    }
    formIds.set(document.form.id, sourcePath);
    declarations.push({ sourcePath, document });
  }

  for (const { sourcePath, document } of declarations) {
    const formDir = resolve(formRoot, document.form.id);
    if (!inside(formRoot, formDir)) throw new Error(`${sourcePath}: form id escapes artifact root`);
    const manifestPath = resolve(formDir, "manifest.json");
    const schemaPath = resolve(formDir, "schema.json");
    const evidencePath = resolve(formDir, "evidence.json");
    const [manifest, evidence] = await Promise.all([json(manifestPath), json(evidencePath)]);
    if (manifest.form.id !== document.form.id ||
        manifest.form.formVersion !== document.form.formVersion) {
      throw new Error(`${relative(ROOT, sourcePath)}: form identity does not match emitted package`);
    }
    await validateResponseNormalization(document, {
      schemaPath,
      evidence,
      dist,
      cache,
      context: relative(ROOT, sourcePath),
    });

    const bytes = `${JSON.stringify(document, null, 2)}\n`;
    await writeFile(resolve(formDir, "response-normalization.json"), bytes);
    manifest.artifacts["response-normalization.json"] = {
      origin: "passthrough",
      sha256: sha256(bytes),
    };
    await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
  }
  if (!files.length) throw new Error(`no response normalization declarations found under ${normalizationRoot}`);
  return { forms: files.length };
}

function parse(argv) {
  const args = {
    normalizationRoot: resolve(ROOT, "normalizations/forms"),
    dist: resolve(ROOT, "dist"),
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (["-v", "-V", "--version"].includes(arg) && argv.length === 1) return { version: true };
    if (arg === "--help" && argv.length === 1) return { help: true };
    if (arg === "--normalizations" || arg === "--dist") {
      if (!argv[index + 1] || argv[index + 1].startsWith("-")) {
        throw new UsageError(`${arg} requires a path`);
      }
      args[arg === "--normalizations" ? "normalizationRoot" : "dist"] = resolve(argv[++index]);
      continue;
    }
    throw new UsageError(`unknown argument ${arg}`);
  }
  return args;
}

const help = () =>
  "usage:\n  command: node scripts/project_response_normalizations.mjs [--normalizations <path>] [--dist <path>]\n" +
  "flags[4]{name,description}:\n  --normalizations,Authored normalization directory (default: normalizations/forms)\n" +
  "  --dist,Emitted artifact directory (default: dist)\n  --help,Show this help\n" +
  "  -v | -V | --version,Show the projector version";

async function main() {
  try {
    const args = parse(process.argv.slice(2));
    if (args.version) return void process.stdout.write(`${VERSION}\n`);
    if (args.help) return void process.stdout.write(`${help()}\n`);
    const result = await projectResponseNormalizations(args);
    process.stdout.write(`response_normalization:\n  status: projected\n  forms: ${result.forms}\n`);
  } catch (error) {
    const usage = error instanceof UsageError;
    process.stdout.write(`error:\n  code: ${usage ? "usage_error" : "normalization_invalid"}\n` +
      `  message: ${JSON.stringify(error.message)}\n` +
      `help[1]: ${usage ? "Run node scripts/project_response_normalizations.mjs --help" : "Fix the named normalization declaration and rerun projection"}\n`);
    process.exitCode = usage ? 2 : 1;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await main();

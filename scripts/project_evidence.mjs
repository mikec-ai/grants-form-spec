#!/usr/bin/env node

import Ajv2020 from "ajv/dist/2020.js";
import { readFile, readdir, writeFile } from "node:fs/promises";
import { dirname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const VERSION = "0.1.0";
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

class UsageError extends Error {}

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function evidenceFiles(root) {
  const found = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) found.push(...(await evidenceFiles(path)));
    if (entry.isFile() && entry.name === "evidence.json") found.push(path);
  }
  return found.sort();
}

function nativeVersionFromUri(source, rel) {
  if (source.type !== "xsd") return null;
  const filename = new URL(source.uri).pathname.split("/").at(-1) ?? "";
  const match = /-V([0-9]+\.[0-9]+)\.xsd$/i.exec(filename);
  if (match) return match[1];
  if (/V[0-9]/i.test(filename)) {
    throw new Error(
      `${rel}: source ${source.id} uses unsupported version-looking XSD URI ${source.uri}; ` +
      "expected a filename ending in -V<major>.<minor>.xsd",
    );
  }
  return null;
}

function mountCanonicalPath(mountPath, canonicalPath) {
  return mountPath ? `${mountPath}.${canonicalPath}` : canonicalPath;
}

function canonicalOccurrence(path) {
  return path
    .split("/")
    .filter(Boolean)
    .map((part) => part === "[]" ? "[*]" : part)
    .join(".")
    .replaceAll(".[*]", "[*]");
}

function canonicalUiDefinition(definition, context) {
  if (typeof definition !== "string" || !definition.startsWith("/properties/")) {
    throw new Error(`${context}: conditional target has unsupported definition ${JSON.stringify(definition)}`);
  }
  const tokens = definition.split("/").slice(1);
  const path = [];
  for (let i = 0; i < tokens.length;) {
    if (tokens[i] === "properties" && tokens[i + 1]) {
      path.push(tokens[i + 1]);
      i += 2;
      continue;
    }
    if (tokens[i] === "items") {
      if (!path.length) throw new Error(`${context}: ambiguous conditional target ${definition}`);
      path[path.length - 1] += "[*]";
      i += 1;
      continue;
    }
    throw new Error(`${context}: ambiguous conditional target ${definition}`);
  }
  return path.join(".");
}

function prePopulationKind(prePopulation, context) {
  if (!prePopulation || typeof prePopulation !== "object" || Array.isArray(prePopulation)) {
    throw new Error(`${context}: gg_pre_population must be an object`);
  }
  if (typeof prePopulation.rule !== "string" || !prePopulation.rule) {
    throw new Error(`${context}: gg_pre_population requires a non-empty rule name`);
  }

  const keys = Object.keys(prePopulation);
  if (keys.length === 1) return "external_lookup";

  const metadata = new Set(["materialize", "order", "presence_fields", "rule"]);
  const hasFields = Object.hasOwn(prePopulation, "fields");
  const hasAmount = Object.hasOwn(prePopulation, "amount");
  const hasPercentage = Object.hasOwn(prePopulation, "percentage");
  let operands;
  if (
    hasFields &&
    !hasAmount &&
    !hasPercentage &&
    Array.isArray(prePopulation.fields) &&
    prePopulation.fields.length > 0 &&
    prePopulation.fields.every((field) => typeof field === "string" && field)
  ) {
    operands = new Set(["fields"]);
  } else if (
    !hasFields &&
    hasAmount &&
    hasPercentage &&
    typeof prePopulation.amount === "string" &&
    prePopulation.amount &&
    typeof prePopulation.percentage === "string" &&
    prePopulation.percentage
  ) {
    operands = new Set(["amount", "percentage"]);
  } else {
    throw new Error(
      `${context}: unsupported gg_pre_population operand shape; expected fields or amount+percentage`,
    );
  }
  const unsupported = keys.filter((key) => !metadata.has(key) && !operands.has(key));
  if (unsupported.length) {
    throw new Error(
      `${context}: unsupported gg_pre_population keys ${unsupported.sort().join(", ")}`,
    );
  }
  return "calculation";
}

function collectCalculationTargets(node, path = [], targets = [], context = "rule schema") {
  if (!node || typeof node !== "object" || Array.isArray(node)) return targets;
  const prePopulation = node.gg_pre_population;
  if (prePopulation && prePopulationKind(prePopulation, `${context}: ${path.join(".")}`) === "calculation") {
    targets.push(path.join("."));
  }
  for (const [key, value] of Object.entries(node)) {
    if (!key.startsWith("gg_")) {
      collectCalculationTargets(value, [...path, key], targets, context);
    }
  }
  return targets;
}

function collectConditionTargets(node, context, targets = []) {
  if (!node || typeof node !== "object") return targets;
  if (node.conditional) targets.push(canonicalUiDefinition(node.definition, context));
  if (Array.isArray(node)) {
    for (const value of node) collectConditionTargets(value, context, targets);
  } else {
    for (const value of Object.values(node)) collectConditionTargets(value, context, targets);
  }
  return targets;
}

function emittedRuleTargets(ruleSchema, uiSchema, occurrences, context) {
  const canonicalOccurrences = [...occurrences].map(canonicalOccurrence);
  const byRulePath = new Map();
  for (const path of canonicalOccurrences) {
    const normalized = path.replaceAll("[*]", "");
    const candidates = byRulePath.get(normalized) ?? [];
    candidates.push(path);
    byRulePath.set(normalized, candidates);
  }
  const targets = [];
  for (const rawPath of collectCalculationTargets(ruleSchema, [], [], context)) {
    const candidates = byRulePath.get(rawPath) ?? [];
    if (candidates.length !== 1) {
      throw new Error(
        `${context}: calculation target ${rawPath} has ${candidates.length || "no"} exact occurrence candidates` +
        (candidates.length ? ` (${candidates.join(", ")})` : ""),
      );
    }
    targets.push({ ruleKind: "calculation", canonicalPath: candidates[0] });
  }
  for (const canonicalPath of collectConditionTargets(uiSchema, context)) {
    if (!canonicalOccurrences.includes(canonicalPath)) {
      throw new Error(`${context}: condition target ${canonicalPath} is not an exact emitted occurrence`);
    }
    targets.push({ ruleKind: "condition", canonicalPath });
  }
  const byIdentity = new Map();
  for (const target of targets) {
    const key = `${target.ruleKind}:${target.canonicalPath}`;
    if (byIdentity.has(key)) {
      throw new Error(
        `${context}: duplicate emitted ${target.ruleKind} target ${target.canonicalPath}; ` +
        "stable occurrence identity is required",
      );
    }
    byIdentity.set(key, target);
  }
  return byIdentity;
}

export async function projectEvidence({ evidenceRoot, dist }) {
  evidenceRoot = resolve(evidenceRoot);
  dist = resolve(dist);
  const schema = await json(resolve(ROOT, "contract/v1/evidence.schema.json"));
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  const validate = ajv.compile(schema);
  const files = await evidenceFiles(evidenceRoot);

  const records = await Promise.all(files.map(async (sourcePath) => ({ sourcePath, document: await json(sourcePath) })));
  const byBlock = new Map(records.map((record) => [record.document.block?.id, record]));

  function resolveBehaviorEvidence(record, visiting = new Set()) {
    const id = record.document.block.id;
    if (visiting.has(id)) throw new Error(`behavior evidence inheritance cycle at ${id}`);
    visiting.add(id);
    const sources = [...record.document.sources];
    const behaviorEvidence = [...(record.document.behaviorEvidence ?? [])];
    for (const inheritance of record.document.inheritsBehaviorEvidenceFrom ?? []) {
      const { blockId: inheritedId, mountPath } = inheritance;
      const inherited = byBlock.get(inheritedId);
      if (!inherited) throw new Error(`${id}: inherited behavior evidence block ${inheritedId} does not exist`);
      const resolved = resolveBehaviorEvidence(inherited, new Set(visiting));
      const behaviorSourceIds = new Set(
        resolved.behaviorEvidence.map((entry) => entry.sourceId).filter(Boolean),
      );
      for (const source of resolved.sources.filter((candidate) => behaviorSourceIds.has(candidate.id))) {
        const existing = sources.find((candidate) => candidate.id === source.id);
        if (existing && JSON.stringify(existing) !== JSON.stringify(source)) {
          throw new Error(`${id}: inherited source ${source.id} conflicts with a local source`);
        }
        if (!existing) sources.push(source);
      }
      behaviorEvidence.push(
        ...resolved.behaviorEvidence.map((entry) => ({
          ...entry,
          canonicalPath: mountCanonicalPath(mountPath, entry.canonicalPath),
          inheritedFrom: inheritedId,
        })),
      );
    }
    visiting.delete(id);
    return { sources, behaviorEvidence };
  }

  for (const { sourcePath, document: authoredDocument } of records) {
    if (!validate(authoredDocument)) {
      const detail = validate.errors.map((error) => `${error.instancePath || "/"} ${error.message}`).join("; ");
      throw new Error(`${relative(ROOT, sourcePath)}: ${detail}`);
    }
    const resolvedEvidence = resolveBehaviorEvidence({ sourcePath, document: authoredDocument });
    const document = {
      ...authoredDocument,
      sources: resolvedEvidence.sources,
      behaviorEvidence: resolvedEvidence.behaviorEvidence,
    };
    delete document.inheritsBehaviorEvidenceFrom;
    if (!validate(document)) {
      const detail = validate.errors.map((error) => `${error.instancePath || "/"} ${error.message}`).join("; ");
      throw new Error(`${relative(ROOT, sourcePath)} after behavior inheritance: ${detail}`);
    }
    const sourceById = new Map(document.sources.map((source) => [source.id, source]));
    for (const behavior of document.behaviorEvidence) {
      if (behavior.authority === "unresolved") continue;
      const source = sourceById.get(behavior.sourceId);
      if (!source) {
        throw new Error(
          `${relative(ROOT, sourcePath)}: behavior ${behavior.canonicalPath} names missing source ${behavior.sourceId}`,
        );
      }
      if (behavior.authority === "official_source" && source.type === "implementation") {
        throw new Error(
          `${relative(ROOT, sourcePath)}: ${behavior.ruleKind} target ${behavior.canonicalPath} ` +
          `claims official_source authority from implementation source ${behavior.sourceId}`,
        );
      }
      if (behavior.authority === "implementation_parity" && source.type !== "implementation") {
        throw new Error(
          `${relative(ROOT, sourcePath)}: ${behavior.ruleKind} target ${behavior.canonicalPath} ` +
          `claims implementation_parity authority from ${source.type} source ${behavior.sourceId}`,
        );
      }
    }

    const rel = relative(evidenceRoot, sourcePath);
    for (const source of document.sources) {
      const uriVersion = nativeVersionFromUri(source, rel);
      if (uriVersion !== null && source.nativeVersion !== uriVersion) {
        throw new Error(
          `${rel}: source ${source.id} nativeVersion ${JSON.stringify(source.nativeVersion)} ` +
          `does not match version ${uriVersion} stated by ${source.uri}`,
        );
      }
    }
    const segments = rel.split(sep);
    const kindRoot = segments[0];
    if (!(["forms", "question-bank"].includes(kindRoot))) {
      throw new Error(`${rel}: evidence must be under forms/ or question-bank/`);
    }
    const targetDir = resolve(dist, ...segments.slice(0, -1));
    const indexPath = resolve(targetDir, "index.json");
    const index = await json(indexPath);
    const expectedKindRoot = index.kind === "question" ? "question-bank" : "forms";
    if (index.id !== document.block.id || expectedKindRoot !== kindRoot) {
      throw new Error(`${rel}: evidence block identity does not match ${relative(dist, indexPath)}`);
    }
    const occurrences = new Set((index.fieldOccurrences ?? []).map((entry) => entry.path));
    if (kindRoot === "forms") {
      const ruleTargets = emittedRuleTargets(
        await json(resolve(targetDir, "sgg", "rule-schema.json")),
        await json(resolve(targetDir, "sgg", "ui-schema.json")),
        occurrences,
        rel,
      );
      const dispositions = new Map();
      for (const behavior of document.behaviorEvidence ?? []) {
        const key = `${behavior.ruleKind}:${behavior.canonicalPath}`;
        if (dispositions.has(key)) {
          throw new Error(
            `${rel}: duplicate ${behavior.ruleKind} evidence disposition for target ${behavior.canonicalPath}`,
          );
        }
        if (!ruleTargets.has(key)) {
          throw new Error(
            `${rel}: ${behavior.ruleKind} evidence ${behavior.canonicalPath} is not an exact emitted rule target`,
          );
        }
        dispositions.set(key, behavior);
      }
      for (const [key, target] of ruleTargets) {
        if (!dispositions.has(key)) {
          throw new Error(
            `${rel}: ${target.ruleKind} target ${target.canonicalPath} has no behavior evidence disposition`,
          );
        }
      }
    }

    await writeFile(resolve(targetDir, "evidence.json"), `${JSON.stringify(document, null, 2)}\n`);
    if (kindRoot === "forms") {
      const manifestPath = resolve(targetDir, "manifest.json");
      const manifest = await json(manifestPath);
      if (manifest.form.formVersion !== document.block.formVersion) {
        throw new Error(
          `${rel}: evidence formVersion ${document.block.formVersion} does not match ` +
          `${relative(dist, manifestPath)} formVersion ${manifest.form.formVersion}`,
        );
      }
      manifest.artifacts["evidence.json"] = "passthrough";
      await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
    }
  }
  if (!files.length) throw new Error(`no evidence sidecars found under ${evidenceRoot}`);
  return { sidecars: files.length };
}

function parse(argv) {
  const args = { evidenceRoot: resolve(ROOT, "evidence"), dist: resolve(ROOT, "dist") };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (["-v", "-V", "--version"].includes(arg) && argv.length === 1) return { version: true };
    if (arg === "--help") return { help: true };
    if (arg === "--evidence" || arg === "--dist") {
      if (!argv[i + 1] || argv[i + 1].startsWith("-")) throw new UsageError(`${arg} requires a path`);
      args[arg === "--evidence" ? "evidenceRoot" : "dist"] = resolve(argv[++i]);
      continue;
    }
    throw new UsageError(`unknown argument ${arg}`);
  }
  return args;
}

const help = () =>
  "usage:\n  command: node scripts/project_evidence.mjs [--evidence <path>] [--dist <path>]\nflags[4]{name,description}:\n  --evidence,Source evidence directory (default: evidence)\n  --dist,Emitted artifact directory (default: dist)\n  --help,Show this help\n  -v | -V | --version,Show the projector version";

async function main() {
  try {
    const args = parse(process.argv.slice(2));
    if (args.version) return void process.stdout.write(`${VERSION}\n`);
    if (args.help) return void process.stdout.write(`${help()}\n`);
    const result = await projectEvidence(args);
    process.stdout.write(`evidence:\n  status: projected\n  sidecars: ${result.sidecars}\n`);
  } catch (error) {
    const usage = error instanceof UsageError;
    process.stdout.write(`error:\n  code: ${usage ? "usage_error" : "evidence_invalid"}\n  message: ${JSON.stringify(error.message)}\nhelp[1]: ${usage ? "Run node scripts/project_evidence.mjs --help" : "Fix the named evidence record and rerun projection"}\n`);
    process.exitCode = usage ? 2 : 1;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await main();

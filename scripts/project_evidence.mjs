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
  if (/(?:^|[-_])V[0-9]/i.test(filename)) {
    throw new Error(
      `${rel}: source ${source.id} uses unsupported version-looking XSD URI ${source.uri}; ` +
      "expected a filename ending in -V<major>.<minor>.xsd",
    );
  }
  return null;
}

export async function projectEvidence({ evidenceRoot, dist }) {
  evidenceRoot = resolve(evidenceRoot);
  dist = resolve(dist);
  const schema = await json(resolve(ROOT, "contract/v1/evidence.schema.json"));
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  const validate = ajv.compile(schema);
  const files = await evidenceFiles(evidenceRoot);

  for (const sourcePath of files) {
    const document = await json(sourcePath);
    if (!validate(document)) {
      const detail = validate.errors.map((error) => `${error.instancePath || "/"} ${error.message}`).join("; ");
      throw new Error(`${relative(ROOT, sourcePath)}: ${detail}`);
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

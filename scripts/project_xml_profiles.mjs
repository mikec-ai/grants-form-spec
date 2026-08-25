#!/usr/bin/env node

import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { dirname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const TARGET_ROOT = resolve(ROOT, "targets/grants-gov-xml");
const PROFILE_ROOT = resolve(TARGET_ROOT, "profiles");
const DIST_FORMS = resolve(ROOT, "dist/forms");

const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function inside(root, path) {
  const rel = relative(root, path);
  return rel !== ".." && !rel.startsWith(`..${sep}`) && !rel.startsWith(sep);
}

function pointer(value, fragment, path) {
  if (!fragment || fragment === "#") return value;
  if (!fragment.startsWith("#/")) throw new Error(`${path}: unsupported JSON pointer ${fragment}`);
  return fragment.slice(2).split("/").reduce((node, raw) => {
    const step = decodeURIComponent(raw).replaceAll("~1", "/").replaceAll("~0", "~");
    if (!node || typeof node !== "object" || !(step in node)) {
      throw new Error(`${path}: JSON pointer does not contain ${step}`);
    }
    return node[step];
  }, value);
}

async function resolveRefs(value, from, stack = new Set()) {
  if (Array.isArray(value)) {
    return Promise.all(value.map((item) => resolveRefs(item, from, stack)));
  }
  if (!value || typeof value !== "object") return value;
  if (typeof value.$ref === "string") {
    const members = Object.keys(value);
    const unexpected = members.filter(
      (member) => !["$ref", "$rename", "$overlay"].includes(member),
    );
    if (unexpected.length > 0) {
      throw new Error(`${from}: $ref has unsupported sibling ${unexpected[0]}`);
    }
    const [location, fragment = ""] = value.$ref.split("#", 2);
    if (!location || /^[a-z][a-z0-9+.-]*:/i.test(location)) {
      throw new Error(`${from}: only relative cross-file references are supported`);
    }
    const target = resolve(dirname(from), location);
    if (!inside(TARGET_ROOT, target)) throw new Error(`${from}: reference escapes target root`);
    const key = `${target}#${fragment}`;
    if (stack.has(key)) throw new Error(`${from}: reference cycle at ${value.$ref}`);
    const targetValue = await resolveRefs(
      pointer(await readJson(target), fragment ? `#${fragment}` : "#", target),
      target,
      new Set([...stack, key]),
    );
    if (!("$rename" in value) && !("$overlay" in value)) return targetValue;
    if (!targetValue || Array.isArray(targetValue) || typeof targetValue !== "object") {
      throw new Error(`${from}: $rename and $overlay require an object reference target`);
    }
    const renames = value.$rename ?? {};
    if (!renames || Array.isArray(renames) || typeof renames !== "object") {
      throw new Error(`${from}: $rename must be an object`);
    }
    const destinations = new Set(Object.values(renames));
    if (
      Object.values(renames).some((member) => typeof member !== "string" || !member) ||
      destinations.size !== Object.keys(renames).length
    ) {
      throw new Error(`${from}: $rename destinations must be unique non-empty strings`);
    }
    for (const [member, replacement] of Object.entries(renames)) {
      if (!(member in targetValue)) throw new Error(`${from}: $rename source ${member} is absent`);
      if (replacement in targetValue && !(replacement in renames)) {
        throw new Error(`${from}: $rename destination ${replacement} already exists`);
      }
    }
    const resolved = Object.fromEntries(
      Object.entries(targetValue).map(([member, child]) => [renames[member] ?? member, child]),
    );
    const overlay = value.$overlay ?? {};
    if (!overlay || Array.isArray(overlay) || typeof overlay !== "object") {
      throw new Error(`${from}: $overlay must be an object`);
    }
    for (const [member, replacement] of Object.entries(overlay)) {
      if (replacement === null) delete resolved[member];
      else resolved[member] = replacement;
    }
    return resolved;
  }
  return Object.fromEntries(
    await Promise.all(
      Object.entries(value).map(async ([key, child]) => [key, await resolveRefs(child, from, stack)]),
    ),
  );
}

async function main() {
  const names = (await readdir(PROFILE_ROOT)).filter((name) => name.endsWith(".json")).sort();
  for (const name of names) {
    const source = resolve(PROFILE_ROOT, name);
    const profile = await resolveRefs(await readJson(source), source);
    const formDir = resolve(DIST_FORMS, profile.formId);
    const manifestPath = resolve(formDir, "manifest.json");
    const manifest = await readJson(manifestPath);
    if (manifest.form?.id !== profile.formId) {
      throw new Error(`${source}: profile formId does not match emitted form package`);
    }
    const output = resolve(formDir, "targets/grants-gov-xml.json");
    await mkdir(dirname(output), { recursive: true });
    await writeFile(output, `${JSON.stringify(profile, null, 2)}\n`);
    manifest.artifacts["targets/grants-gov-xml.json"] = "generated";
    await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
  }
  process.stdout.write(`xml-profiles:\n  status: projected\n  profiles: ${names.length}\n`);
}

await main();

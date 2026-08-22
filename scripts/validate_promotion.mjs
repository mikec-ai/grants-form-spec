#!/usr/bin/env node

import Ajv2020 from "ajv/dist/2020.js";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

async function promotionFiles(root) {
  const found = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const path = resolve(root, entry.name);
    if (entry.isDirectory()) found.push(...(await promotionFiles(path)));
    if (entry.isFile() && entry.name === "promotion.json") found.push(path);
  }
  return found.sort();
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 1 && args[0] === "--help") {
    process.stdout.write("usage:\n  command: node scripts/validate_promotion.mjs [packet.json ...]\n");
    return 0;
  }
  if (args.some((arg) => arg.startsWith("-"))) {
    process.stdout.write("error:\n  code: usage_error\n  message: unknown flag; run --help\n");
    return 2;
  }
  try {
    const schema = JSON.parse(await readFile(resolve(ROOT, "contract/v1/promotion-packet.schema.json")));
    const ajv = new Ajv2020({ allErrors: true, strict: true });
    const validate = ajv.compile(schema);
    const paths = args.length ? args.map((path) => resolve(path)) : await promotionFiles(resolve(ROOT, "spikes"));
    if (!paths.length) throw new Error("no promotion packets found");
    let records = 0;
    for (const path of paths) {
      const packet = JSON.parse(await readFile(path));
      if (!validate(packet)) {
        const detail = validate.errors.map((error) => `${error.instancePath || "/"} ${error.message}`).join("; ");
        throw new Error(`${path}: ${detail}`);
      }
      records += packet.records.length;
    }
    process.stdout.write(`promotion_validation:\n  status: passed\n  packets: ${paths.length}\n  records: ${records}\n`);
    return 0;
  } catch (error) {
    process.stdout.write(`error:\n  code: promotion_invalid\n  message: ${JSON.stringify(error.message)}\n`);
    return 1;
  }
}

process.exitCode = await main();

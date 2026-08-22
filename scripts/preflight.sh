#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

npm run build
npm run emit
npm run project-evidence
npm run validate-artifacts
npm run validate-promotion
npm test
npm run test-python
npm run package-artifacts
python3 scripts/package_artifacts.py --verify build/grants-form-artifacts.tar.gz
npm run analyze -- --json >/dev/null

result=0
while IFS= read -r -d '' file; do
  if ! npx tsp compile "$file" --no-emit >/dev/null 2>&1; then
    printf '%s\n' "$file does not compile independently" >&2
    npx tsp compile "$file" --no-emit >&2
    result=1
  fi
done < <(find typespec-form-spec/lib specs spikes -name '*.tsp' -print0)

if [ "$result" -ne 0 ]; then
  exit 1
fi

printf 'preflight:\n  status: passed\n'

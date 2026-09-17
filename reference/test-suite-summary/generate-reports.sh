#!/usr/bin/env bash
# Regenerate reports
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OUT_DIR="$SCRIPT_DIR/reports"
MOCHA="$REPO_ROOT/node_modules/.bin/mocha"

cd "$REPO_ROOT"
mkdir -p "$OUT_DIR"

gen_suite() {
  local title="$1" npm_script="$2" mocha_args="$3" location="$4" out_file="$5"

  local dry_run_cmd="npx mocha $mocha_args --dry-run --reporter spec --no-colors"
  local output
  output="$($MOCHA $mocha_args --dry-run --reporter spec --no-colors)"

  {
    echo "# $title (\`npm run $npm_script\`)"
    echo
    echo "Command: \`mocha $mocha_args\`"
    echo
    echo "Location: \`$location\`"
    echo
    echo "To regenerate this listing without running assertions:"
    echo '```'
    echo "$dry_run_cmd"
    echo '```'
    echo
    echo '```'
    echo "$output"
    echo '```'
  } > "$out_file"

  echo "Wrote $out_file"
}

gen_suite \
  "Unit tests" \
  "test:unit" \
  "--require spec/config/setup --require spec/config/setup-unit spec/unit --recursive" \
  'spec/unit/**/*.spec.js' \
  "$OUT_DIR/unit-tests.md"

gen_suite \
  "Integration tests" \
  "test:integration" \
  "--require spec/config/setup spec/integration --recursive" \
  'spec/integration/**/*.spec.js (uses real fixture files under spec/integration/data/)' \
  "$OUT_DIR/integration-tests.md"

gen_suite \
  "End-to-end tests" \
  "test:end-to-end" \
  "--require spec/config/setup spec/end-to-end --recursive" \
  'spec/end-to-end/**/*.spec.js' \
  "$OUT_DIR/end-to-end-tests.md"

echo
echo "NOTE: reports/jasmine-browser-tests.md is maintained by hand, because it cannot be dry-run like Mocha suites."

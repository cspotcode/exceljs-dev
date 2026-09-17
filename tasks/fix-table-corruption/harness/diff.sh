#!/usr/bin/env bash
# Unzips an original .xlsx and a round-tripped .xlsx side by side and diffs
# their XML parts, to make it easy to spot what this library changed/broke.
#
# Usage:
#   ./diff.sh <original.xlsx> <roundtrip.xlsx> [workdir]

set -euo pipefail

ORIG="$1"
ROUNDTRIP="$2"
WORKDIR="${3:-$(dirname "$0")/out/diff}"

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR/orig" "$WORKDIR/roundtrip"

unzip -o -q "$ORIG" -d "$WORKDIR/orig"
unzip -o -q "$ROUNDTRIP" -d "$WORKDIR/roundtrip"

SCRIPT_DIR="$(dirname "$0")"
find "$WORKDIR/orig" "$WORKDIR/roundtrip" \( -name '*.xml' -o -name '*.rels' \) -print0 \
  | xargs -0 uv run python "$SCRIPT_DIR/prettify-xml.py"

# Attribute order isn't meaningful per the XML spec, so re-order roundtrip's
# attributes to match orig's, keeping diffs focused on real differences.
uv run python "$SCRIPT_DIR/reorder-attrs.py" "$WORKDIR/orig" "$WORKDIR/roundtrip"

echo "=== File listing diff ==="
diff <(cd "$WORKDIR/orig" && find . -type f | sort) \
     <(cd "$WORKDIR/roundtrip" && find . -type f | sort) || true

echo
echo "=== XML content diff (orig vs roundtrip) ==="
diff -ru "$WORKDIR/orig" "$WORKDIR/roundtrip" || true

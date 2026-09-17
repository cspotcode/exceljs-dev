# Comparing exceljs forks on the table-corruption bug — findings

## Setup

Three subdirectories, each with its own `package.json` and the given
package installed via `npm install` (see [idea.md](idea.md)):

| dir               | package                  | version installed   |
|--------------------|--------------------------|----------------------|
| `a-exceljs/`        | `exceljs`                | `4.4.0` (latest on npm) |
| `b-protobi/`        | `@protobi/exceljs`       | `4.4.0-protobi.10` (latest on npm) |
| `c-hyperliskdev/`   | `@hyperliskdev/exceljs`  | `4.4.2` (latest on npm) |
| `d-rmartin93/`      | `@rmartin93/exceljs-fork`| `4.4.4` (latest on npm) |
| `e-sheetjs/`        | `xlsx` (SheetJS)         | `0.18.5` (latest on npm registry) |
| `f-exceljs-community/` | `exceljs-community`  | `5.1.1` (latest on npm) |

Note: none of `protobi/exceljs`, `hyperliskdev/exceljs`, or
`rmartin93/exceljs-fork` are published to npm under the bare name `exceljs`
(and this environment's npm config has git dependency fetching disabled —
`EALLOWGIT`), so each is installed from its own scoped npm package instead
of `github:` or a local clone.

For SheetJS, [docs.sheetjs.com](https://docs.sheetjs.com/) recommends
installing the latest build from their own CDN
(`npm i --save https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`), but
this environment's npm config also has remote-tarball fetching disabled
(`EALLOWREMOTE`), so the older `xlsx@0.18.5` from the public npm registry
was used instead. `xlsx@0.18.5` is the free/community SheetJS build; table
(`!tables`) read/write is documented as a SheetJS Pro feature not included
in the community build, which is very relevant to the result below.

`roundtrip.js` (in this directory) is a small variant of
`dev/tasks/fix-table-corruption/harness/roundtrip.js` that `require()`s
whichever package name is installed in a given subdirectory, loads
`BookWithTable.xlsx`, and writes it back out with that fork.

The reused harness is `dev/tasks/fix-table-corruption/harness/diff.sh`,
which unzips + pretty-prints + attribute-reorders the original vs.
round-tripped `.xlsx` so the XML diffs are readable. Ran once per fork:

```
node dev/tasks/compare-forks/roundtrip.js dev/tasks/compare-forks/a-exceljs exceljs \
  dev/tasks/compare-forks/BookWithTable.xlsx dev/tasks/compare-forks/a-exceljs/out
dev/tasks/fix-table-corruption/harness/diff.sh \
  dev/tasks/compare-forks/BookWithTable.xlsx \
  dev/tasks/compare-forks/a-exceljs/out/roundtrip-BookWithTable.xlsx \
  dev/tasks/compare-forks/a-exceljs/out/diff
```
(repeated for `b-protobi`/`@protobi/exceljs`,
`c-hyperliskdev`/`@hyperliskdev/exceljs`, and
`d-rmartin93`/`@rmartin93/exceljs-fork`).

SheetJS has a different API (`XLSX.readFile`/`XLSX.writeFile`, not
`Workbook.xlsx.readFile`/`writeFile`), so `e-sheetjs/roundtrip-sheetjs.js`
is a separate, standalone script rather than a `roundtrip.js` variant. Same
`diff.sh` harness reused for the XML diff afterward.

Fixture: `dev/tasks/compare-forks/BookWithTable.xlsx` — same fixture used in
`dev/tasks/fix-table-corruption` (3-row: 1 header + 2 data, 3-column table
"Table2", authored directly in Excel desktop).

## Result: `xl/tables/table1.xml`, orig vs. round-trip

**`exceljs@4.4.0` (upstream) — `ref` preserved correctly:**
```diff
-  id="2"
-  xr:uid="{37B93493-...}"
+  id="1"
   ref="A1:C3"
-  totalsRowShown="0"
+  totalsRowShown="1"
+  headerRowCount="0"
```
`ref` stays `A1:C3`. Cosmetic/metadata losses only (uid stripped, id
renumbered, `totalsRowShown` flipped to `1`, filter-column visibility
attributes added) — not the corruption this fork is chasing.

**`@protobi/exceljs@4.4.0-protobi.10` (this fork, published) — bug reproduced:**
```diff
-  ref="A1:C3"
+  ref="A1:C1"
-  totalsRowShown="0"
+  totalsRowShown="1"
+  headerRowCount="1"
```
`ref` is corrupted from `A1:C3` down to `A1:C1`, and `headerRowCount="1"`
appears. This exactly matches the root cause already diagnosed in
`dev/tasks/fix-table-corruption/findings.md` (the `worksheet.js` model
setter forces `table.rows = []` on load, so `Table.validate()` recomputes
`tableRef` as if the table has zero data rows). Confirmed the fix documented
there has **not** shipped yet — this repo's current HEAD (`fix-table-corruption`
branch, based on the same commit as the published `4.4.0-protobi.10`) still
has the buggy `headerRowCount === '1'` default in
[lib/xlsx/xform/table/table-xform.js:69](../../../lib/xlsx/xform/table/table-xform.js#L69)
and the `rows = []` clobber in
[lib/doc/worksheet.js:1002-1032](../../../lib/doc/worksheet.js#L1002-L1032).

The `rows = []` clobber was introduced by protobi's own commit:

- **[cc6912ef — "Update #23 Adopt table addRow() fix from rmartin93/exceljs-fork"](https://github.com/protobi/exceljs/commit/cc6912ef920d85e86e698015c07975b64f1fb6d7)**
  (Nov 7, 2025, Pieter Sheth-Voss). This is the commit that ported an
  external `addRow()` fix and, as a side effect, added the `worksheet.js`
  reduce block that always sets `table.rows = []` before constructing
  `Table`, which is what makes `Table.validate()` recompute a bogus
  zero-height `tableRef` on every load.

**`@hyperliskdev/exceljs@4.4.2` — `ref` preserved correctly:**
```diff
-  id="2"
-  xr:uid="{37B93493-...}"
+  id="1"
   ref="A1:C3"
-  totalsRowShown="0"
+  totalsRowShown="1"
+  headerRowCount="0"
```
Byte-for-byte identical diff shape to upstream `exceljs@4.4.0` — this fork
does not carry the table-corruption bug. It also does not appear to include
protobi's `cc6912e` ("Adopt table addRow() fix from rmartin93/exceljs-fork")
commit that introduced the regression.

**`@rmartin93/exceljs-fork@4.4.4` — bug reproduced (this is the origin fork):**
```diff
-  id="2"
-  xr:uid="{37B93493-...}"
+  id="1"
-  ref="A1:C3"
+  ref="A1:C1"
-  totalsRowShown="0"
+  totalsRowShown="1"
+  headerRowCount="1"
```
Identical corruption to `@protobi/exceljs`: `ref` collapses to `A1:C1` and
`headerRowCount="1"` is added. This is expected — protobi's `cc6912ef`
commit (above) explicitly ported this fork's `addRow()` fix. The originating
commit in `rmartin93/exceljs-fork` is:

- **[6b77cea7 — "Fix getTable() addRow bug and preserve Excel table filter buttons"](https://github.com/rmartin93/exceljs-fork/commit/6b77cea7147e99a3bb750b0fc902bff9ef343708)**
  (Oct 20, 2025). Its own commit message describes the exact change that
  causes the corruption: *"Add empty rows array for loaded tables"* and
  *"Auto-detect headerRow when columns have names"* in the `worksheet.js`
  model setter — this is the `table.rows = []` clobber that later made its
  way into the protobi fork unchanged.

**SheetJS `xlsx@0.18.5` (community/free build) — table dropped entirely, not corrupted:**

File listing diff (orig vs. round-trip):
```diff
< ./xl/sharedStrings.xml
---
> ./xl/metadata.xml
< ./xl/tables/table1.xml
< ./xl/worksheets/_rels/sheet1.xml.rels
```
`xl/tables/table1.xml` is **not written at all** on round-trip — no table
part, no `_rels` file relating the sheet to a table, and no `<tableParts>`
element in `xl/worksheets/sheet1.xml` either. This isn't the same failure
mode as the four ExcelJS-family libraries above (which preserve the table
but sometimes corrupt its `ref`); SheetJS's free build silently discards
the table structure altogether while keeping the cell data/values. This
matches SheetJS's own documentation, which lists table (`!tables`)
read/write as a **SheetJS Pro** feature not included in the community
`xlsx` package — so this likely is not a bug in the community build, just
a feature it doesn't have. (The paid Pro build was not tested here, since
it isn't available via a plain `npm install` in this environment.)

## Sixth check: `exceljs-community`

Added `f-exceljs-community/` — [`exceljs-community`](https://www.npmjs.com/package/exceljs-community)
([xcybplx/exceljs-community](https://github.com/xcybplx/exceljs-community)),
version `5.1.1` (latest on npm), described as a "Maintained drop-in
replacement for exceljs." Same API as upstream (`main: ./excel.js`), so it
uses the shared `roundtrip.js` harness like the other ExcelJS-family forks.

**`exceljs-community@5.1.1` — `ref` preserved correctly:**
```diff
-  id="2"
-  xr:uid="{37B93493-...}"
+  id="1"
   ref="A1:C3"
-  totalsRowShown="0"
+  totalsRowShown="1"
+  headerRowCount="0"
```
Same diff shape as upstream `exceljs@4.4.0` and `@hyperliskdev/exceljs`:
`ref` stays `A1:C3`. This fork does not carry the `rmartin93`/protobi
`rows = []` regression either.

## Conclusion

The table-`ref`-corruption bug **originates in `rmartin93/exceljs-fork`**
(commit `6b77cea7`, Oct 20, 2025) and was carried into the protobi fork when
protobi adopted that fix (commit `cc6912ef`, Nov 7, 2025). It is not present
in upstream `exceljs`, `hyperliskdev/exceljs`, or `exceljs-community` —
none of which picked up that commit. The fix plan already written up in
`dev/tasks/fix-table-corruption/findings.md` remains the right next step;
this comparison corroborates the diagnosis against three independent,
unaffected implementations, traces the regression to its origin, and
confirms the bug is still live in the latest published releases of both
affected forks (`@protobi/exceljs@4.4.0-protobi.10` and
`@rmartin93/exceljs-fork@4.4.4`).

SheetJS's free/community build isn't a useful point of comparison for this
specific bug: it doesn't corrupt the table, it just doesn't round-trip
tables at all (a documented Pro-only feature gap), so it can't confirm or
rule out the `rows = []`/`Table.validate()` failure mode being investigated
here.

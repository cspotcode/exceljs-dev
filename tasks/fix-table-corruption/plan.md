# Fix table corruption on load/round-trip

## Context

Loading a real Excel-authored workbook with a table, then writing it back
out (`wb.xlsx.readFile()` → `wb.xlsx.writeFile()`, no mutation in between),
produces a `.xlsx` that Excel refuses to open. Excel reports the file as
corrupted and offers to repair it.

This matches the long-standing upstream report
[exceljs/exceljs#2585](https://github.com/exceljs/exceljs/issues/2585)
(filed by protobi-pieter, still open, 14 comments). We independently
reproduced and diagnosed it using a real fixture. One of the three root
causes we found (Bug 3 below) matches what a commenter on that issue
(`hyperliskdev`) partially diagnosed — but they only found the
`autoFilter`/`filterColumn` symptom, not the `ref`-collapse bug. The
`ref`-collapse bug is more severe and is what actually triggers Excel's
repair prompt on our fixture.

We diagnosed and reproduced this with a new test harness at
`dev/tasks/fix-table-corruption/harness/` (see
`dev/tasks/fix-table-corruption/findings.md` for the original investigation
notes) and a real Excel-created fixture at
`dev/tasks/fix-table-corruption/harness/fixtures/BookWithTable.xlsx`. It's a
single-sheet workbook with one table, "Table2", over `A1:C3`: 1 header row +
2 data rows, 3 columns. `totalsRowShown="0"` and no `headerRowCount`
attribute — both at Excel's implicit defaults. `autoFilter` has no
`filterColumn` children, since nothing is filtered.

Diffing orig vs. round-tripped `xl/tables/table1.xml` (via `just task bc` /
`just task diff`) shows:
- `ref` collapses from `A1:C3` to `A1:C1`.
- `totalsRowShown="1"` appears (was `"0"`); a new `headerRowCount="1"`
  appears.
- `autoFilter` gains 3 `<filterColumn>` children it never had.

`sheet1.xml`'s diff (dropped `xr:uid`/revision namespaces, `tabSelected`,
`<selection>`; gained `zoomScale`/`zoomScaleNormal`) is cosmetic metadata
churn. Excel regenerates this freely. It is not corruption and is out of
scope here.

The table's declared extent and filter state no longer match its actual
data and position. That mismatch is what Excel flags as corrupt.

## Root cause

We confirmed this by inspecting the in-memory model right after
`readFile()`, before any write occurs: corruption happens on **read**, not
on write.

Three compounding bugs, all in the table load path:

### Bug 1 — [lib/xlsx/xform/table/table-xform.js:69](../../../lib/xlsx/xform/table/table-xform.js#L69) — wrong `headerRowCount` default

```js
headerRow: attributes.headerRowCount === '1',
```

Excel omits `headerRowCount` from the XML when it's `1` (the default). It
writes the attribute only when explicitly `0`. So a normal Excel table with
a header row parses to `headerRow: false` here, because
`attributes.headerRowCount` is `undefined`, not `'1'`.

(`totalsRow` has the mirror-image quirk. Excel toggles between
`totalsRowCount="1"` when a totals row exists and `totalsRowShown="0"/"1"`
when it doesn't. The existing parse code already reads only
`totalsRowCount`, which defaults correctly to `false` when both attributes
are absent. No change needed there.)

### Bug 2 — [lib/doc/worksheet.js:1002-1032](../../../lib/doc/worksheet.js#L1002-L1032) — `table.rows` forced empty, collapsing `ref`

This is the most severe bug. It breaks the table's relationship to its own
data.

**Why the code is there.** Before commit `cc6912ef` ("Adopt table addRow()
fix from rmartin93/exceljs-fork"), loading a table crashed as soon as you
called `table.addRow()`. The load path called `new Table()` with no
arguments, so `this.table` stayed `undefined`, and `Table.height`'s
`this.table.rows.length` threw. `cc6912ef` fixed the constructor call to
`new Table(this, table)` — correct. But `Table`'s constructor calls
`validate()`, which asserts `table.rows` must exist. XML-sourced tables
never have a `rows` field: the `<table>` XML element stores only metadata
(`ref`, columns, style). Actual cell values live in the worksheet's
`<sheetData>`, parsed separately. So the assert started failing, and the
author patched around it the fastest way available:

```js
this.tables = value.tables.reduce((tables, table) => {
  if (table.tableRef && !table.ref) {
    table.ref = table.tableRef;
  }
  if (!table.rows) {
    table.rows = [];          // <-- always empty; nothing ever populates this from sheet data
  }
  if (!table.headerRow && table.columns && table.columns.length > 0) {
    const hasColumnNames = table.columns.some(col => col.name && col.name.length > 0);
    if (hasColumnNames) {
      table.headerRow = true;  // masks bug 1 above, but only when columns have names
    }
  }
  ...
  const t = new Table(this, table);   // <-- Table constructor calls validate()
  ...
```

**Why `[]` is wrong.** `table.rows` isn't just a presence check.
`Table.validate()` ([lib/doc/table.js:129-180](../../../lib/doc/table.js#L129-L180))
uses `table.rows.length` to *compute* `tableRef`:

```js
const {width, tableHeight} = this;   // tableHeight = table.rows.length + header? + totals?
table.tableRef = colCache.encode(row, col, row + tableHeight - 1, col + width - 1);
```

This is correct for the **authoring** path (`worksheet.addTable(model)`),
where the caller supplies `rows` as real data and expects exceljs to derive
the sheet layout from it. See `index.d.ts`'s `TableProperties.rows: any[][]`
— a *required* field of the public `addTable()` contract. It is wrong for
the **load** path, where `ref` is already ground truth (correctly parsed
from XML) and `rows` has no source data at all. Because `table.rows` is
always `[]` on load, `validate()` always recomputes `tableRef` as if the
table has zero data rows. It overwrites the correctly-parsed `A1:C3` with a
bogus `A1:C1`, regardless of how many rows actually exist on the sheet.

**Dead code aside.** `Table.load()`
([lib/doc/table.js:238-275](../../../lib/doc/table.js#L238-L275)) looks like
it should derive `rows` from the sheet. It's never called anywhere in the
codebase (confirmed via `grep`), and its logic actually *writes into*
worksheet cells (same direction as `store()`), not read from them. It isn't
usable as-is.

`table.rows.length` is the single source of truth for table height
throughout `Table`: the `height`/`filterHeight`/`tableHeight` getters,
`validate()`, `commit()`, `addRow()`, `removeRows()`, and the totals-row
positioning math in `_writeRowToWorksheet()`. Any fix must give `table.rows`
the correct row entries before `new Table(...)` runs — not bypass
`validate()`'s use of it.

### Bug 3 — [lib/doc/worksheet.js:1019-1026](../../../lib/doc/worksheet.js#L1019-L1026) — spurious `filterColumn` fabrication

```js
if (table.autoFilterRef && table.columns) {
  for (const column of table.columns) {
    if (column.filterButton === undefined) {
      column.filterButton = true;
    }
  }
}
```

`table.autoFilterRef` is present on almost every table. So this
unconditionally sets `filterButton = true` on every column that doesn't
already have it set — even when the original XML's `<autoFilter>` was
self-closing with zero `<filterColumn>` children. That self-closing form is
Excel's own convention for "nothing is filtered." Confirmed by
[lib/xlsx/xform/table/auto-filter-xform.js:35-46](../../../lib/xlsx/xform/table/auto-filter-xform.js#L35-L46),
whose `parseOpen`/`parseClose` leave `model.columns` as `[]` when there are
no `filterColumn` children to parse.

On write,
[lib/xlsx/xform/table/auto-filter-xform.js:24-33](../../../lib/xlsx/xform/table/auto-filter-xform.js#L24-L33)
unconditionally iterates `model.columns` and renders one `<filterColumn>`
leaf per column
([lib/xlsx/xform/table/filter-column-xform.js:47-51](../../../lib/xlsx/xform/table/filter-column-xform.js#L47-L51)).
So the fabricated `filterButton: true` values — now present on every column
because of the patch above — cause 3 spurious `<filterColumn colId="N"
hiddenButton="0"/>` tags to appear where the original had none. This matches
what `hyperliskdev` independently found on the upstream issue thread, though
they framed it only as "the render is wrong." The actual defect is one step
earlier: the load path fabricates `filterButton` state that was never
present in the source file.

## Fix

### 1. `lib/xlsx/xform/table/table-xform.js` — default `headerRowCount` to true when absent

```js
headerRow: attributes.headerRowCount === undefined ? true : attributes.headerRowCount === '1',
```

### 2. `lib/doc/worksheet.js` — derive `table.rows` from real sheet content instead of forcing `[]`

We considered two fixes for Bug 2.

**Option A — make `Table.validate()` tolerate a missing `rows`, and never
populate `rows` during load.** Skip `ref` recomputation when `rows` is
`undefined`; trust the XML-parsed `ref` as-is. This is a smaller diff.
`rows` is a required field of `addTable()`'s `TableProperties` type and is
always present on that path (the assert already enforces this today), so
`addTable()` and its `ref` derivation from real row data are unaffected.

But this leaves `table.rows` permanently empty for any table loaded from a
file. If a user then calls `table.addRow()` or `table.commit()` on a loaded
table, those methods still do `table.rows.push(...)` and iterate
`table.rows` as if it reflects real sheet state. They would silently behave
as if the table had zero existing rows: `commit()`'s "clear out below table
if it has shrunk" logic would think the table just grew from 0 rows, and
`_writeRowToWorksheet`'s totals-row-shifting math would compute the wrong
target row. This reintroduces a real bug for the exact
`addRow()`-on-a-loaded-table workflow that commit `cc6912ef` was written to
support.

**Option B (recommended) — populate `table.rows` with real data read back
from the worksheet during load, before constructing `Table`.**
`Table.validate()` stays untouched, `addTable()` is unaffected, and loaded
tables also become safe to mutate afterward via `addRow()`/`commit()`,
because `rows` genuinely reflects sheet state. This is the one change that
fixes the corruption bug without breaking the feature `cc6912ef` was added
for.

**Implementation for Option B.** In the `value.tables.reduce(...)` block
(around line 1002), replace the unconditional:
```js
if (!table.rows) {
  table.rows = [];
}
```
with logic that runs only when `table.rows` is missing — this only fires
for XML-sourced tables, since authoring API callers already supply real
`rows`. It should:
1. Derive the actual data row count from `table.ref` (already aliased from
   `tableRef` a few lines above) and the table's `headerRow`/`totalsRow`
   flags. Both are correct at this point, since Bug 1 is fixed upstream and
   `totalsRow` was already read correctly.
2. Read real values back from the worksheet's already-populated rows
   (`this.getRow(...)`, populated earlier in the same `set model()` by
   `this._parseRows(value)` at line 991, which runs before this `reduce`)
   to build one array per data row, one value per column.

Use `colCache.decode(table.ref)` to get `{top, bottom, left, right}`.
Compute:
```
dataRowCount = (bottom - top + 1) - (headerRow ? 1 : 0) - (totalsRow ? 1 : 0)
```
For each of those rows, read `this.getRow(top + offset).getCell(left +
colIndex).value` for each column to build the row's value array. Clamp
`dataRowCount` to `0` rather than throwing if the ref is malformed — this
runs during load of arbitrary real-world files.

### 3. `lib/doc/worksheet.js` — don't fabricate `filterButton` when orig had no filter columns

Replace the unconditional `filterButton = true` patch (lines 1019-1026) so
it fires only when the table's `autoFilter` XML actually had `filterColumn`
children. Only backfill `filterButton` on columns that already came back
from `AutoFilterXform` with some column filter state — never fabricate it
from nothing.

Concretely: run this patch only when `table.columns[i]` already has
`filterButton !== undefined` for at least one column (meaning
`autoFilterRef`'s children were actually parsed). Alternative: track whether
`autoFilter.columns` was non-empty and thread that through instead of keying
off `autoFilterRef` alone, since `autoFilterRef` is present on almost every
table regardless of filter state. We'll finalize the exact mechanism while
reading the surrounding `table-xform.js` `parseClose` reconciliation code
(lines ~95-108) during implementation — that's where
`autoFilter.model.columns` values already get copied onto
`this.model.columns[index].filterButton`. That existing per-index copy loop
already does the right thing when there ARE `filterColumn` children. The bug
is purely the `worksheet.js` patch overriding `undefined` back to `true`
afterward regardless.

## Files to change

- `lib/xlsx/xform/table/table-xform.js` — one-line default fix (Bug 1).
- `lib/doc/worksheet.js` — replace the `table.rows = []` fallback with real
  derivation from sheet content (Bug 2, Option B), and stop fabricating
  `filterButton` when the source had no filter columns (Bug 3).

## Regression tests

Per AGENTS.md requirement #4: tests must round-trip a real fixture, not
synthetic models.

Add `spec/integration/issues/issue-2585-table-corruption.spec.js`
(referencing [exceljs/exceljs#2585](https://github.com/exceljs/exceljs/issues/2585)
per this fork's commit-must-reference-an-issue workflow) that:
- Copies `dev/tasks/fix-table-corruption/harness/fixtures/BookWithTable.xlsx`
  into `spec/integration/data/` (confirm naming convention against existing
  files in that directory).
- `wb.xlsx.load()`s it, then `wb.xlsx.writeBuffer()`s it back out.
- Re-loads the round-tripped buffer and asserts `worksheet.tables.Table2`'s
  `ref`/`tableRef`, `headerRow`, `totalsRow`, `columns[].name`, and
  `columns[].filterButton` match the original. This is a full model-level
  round-trip assertion — the automatable proxy for "Excel would accept this
  file" available in CI.
- Also asserts on the raw `xl/tables/table1.xml` bytes (`ref="A1:C3"`, no
  unexpected `totalsRowShown`/`headerRowCount` drift, no spurious
  `filterColumn` children), using the same unzip approach the harness uses.
  Model-level assertions alone wouldn't catch Bug 3: `filterButton` defaults
  to `true` either way once read back, so the round-tripped model could look
  "equal" while the intermediate XML still had spurious `filterColumn` tags
  on a re-parse. Checking bytes directly on the first write is the more
  precise check.

## Verification

1. Run existing unit tests for the table xform to confirm no regression:
   `npx mocha spec/unit/xlsx/xform/table/*.spec.js` — in particular
   `table-xform.spec.js` and the existing `table.1.2.xml`/`table.1.1.json`
   fixtures. These already have `headerRowCount="1"` explicit, so Bug 1's
   fix doesn't affect them, but they must still pass.
2. Re-run the harness: `just task roundtrip` then `just task diff` (or `just
   task bc`) against `BookWithTable.xlsx`. Confirm `xl/tables/table1.xml`
   round-trips with `ref="A1:C3"`, `totalsRowShown="0"` (no
   `totalsRowCount`), and `autoFilter` without spurious `filterColumn`
   children (self-closing, matching orig).
3. Per AGENTS.md requirement #6 (XLSX serialization changes must be
   Excel-verified): ask the user to open the round-tripped file in Excel
   desktop and confirm no "Repaired Records" warning, OR round-trip through
   `soffice --headless --convert-to xlsx` and inspect the resulting
   `table1.xml` bytes. Required before considering this done.
4. Run the new regression spec and the full `npm run test:unit` suite.
5. Per this fork's workflow (`.claude/instructions.md`): commit messages
   reference `#2585`. After committing, add a comment to that GitHub issue
   linking the commit. Only do this after the user reviews and approves the
   diff (per the same file's "always ask before commit" rule).

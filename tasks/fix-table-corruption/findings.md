# Table corruption bug — findings

## Harness

`dev/tasks/fix-table-corruption/harness/`
- `roundtrip.js <input.xlsx> [outdir]` — loads an xlsx with exceljs and writes it back out.
- `diff.sh <original.xlsx> <roundtrip.xlsx> [workdir]` — unzips both and diffs every XML part.

Run against the fixture:
```
node dev/tasks/fix-table-corruption/harness/roundtrip.js dev/tasks/fix-table-corruption/harness/fixtures/BookWithTable.xlsx
dev/tasks/fix-table-corruption/harness/diff.sh dev/tasks/fix-table-corruption/harness/fixtures/BookWithTable.xlsx dev/tasks/fix-table-corruption/harness/out/roundtrip-BookWithTable.xlsx
```

Fixture: `dev/tasks/fix-table-corruption/harness/fixtures/BookWithTable.xlsx`. A 3-row (1 header + 2 data), 3-column table ("Table2"), created directly in Excel desktop.

## Root cause

The corruption happens on **read**, not write. Confirmed by inspecting the in-memory
table model right after `wb.xlsx.readFile()`. `tableRef` is already wrong (`A1:C1`
instead of `A1:C3`) before any write occurs.

Two compounding bugs:

### 1. `table-xform.js` parseOpen — wrong `headerRowCount` default

[lib/xlsx/xform/table/table-xform.js:69](../../../lib/xlsx/xform/table/table-xform.js#L69):
```js
headerRow: attributes.headerRowCount === '1',
```
Excel omits `headerRowCount` entirely when it's 1 (the default). It only writes the
attribute when explicitly 0. So a real Excel-authored table with a header row parses
to `headerRow: false`. (A downstream band-aid masks this in our fixture — see below.)

### 2. `worksheet.js` model setter — table rows discarded, then `Table.validate()` recomputes `ref` from zero rows

[lib/doc/worksheet.js:1002-1032](../../../lib/doc/worksheet.js#L1002-L1032), added in commit
`cc6912ef` ("Adopt table addRow() fix from rmartin93/exceljs-fork"):

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
      table.headerRow = true;  // masks bug #1 above, but only when columns have names
    }
  }
  ...
  const t = new Table(this, table);   // <-- Table constructor calls validate()
  ...
```

`Table.validate()` ([lib/doc/table.js:129-180](../../../lib/doc/table.js#L129-L180)) does:
```js
const {width, tableHeight} = this;   // tableHeight = table.rows.length + header? + totals?
table.tableRef = colCache.encode(row, col, row + tableHeight - 1, col + width - 1);
```

`table.rows` is always forced to `[]` on load, so `tableHeight` computes as if the
table has **zero data rows** — regardless of how many rows actually exist on the
sheet. This overwrites the correctly-parsed `ref`/`tableRef` (`A1:C3`) with a bogus
one (`A1:C1`). It also flips `totalsRowShown`/`headerRowCount` on write, because the
model now looks like a header-only table.

Verified via harness: `xl/tables/table1.xml` round-trips from
`ref="A1:C3" totalsRowShown="0"` (no `headerRowCount`) to
`ref="A1:C1" totalsRowShown="1" headerRowCount="1"`. This mismatch between the
table's declared `ref` and its actual position/size relative to `autoFilter` and
the sheet's real data is what Excel flags as corruption.

## Next steps (not yet implemented)

- Fix `table-xform.js` to default `headerRowCount` to `1` (true) when absent, matching
  Excel's own default, instead of defaulting to `false`.
- Fix the `worksheet.js` reduce/`Table.validate()` interaction so loading a table does
  not clobber the parsed `ref` based on a fabricated empty `rows` array. Either skip the
  mutating `validate()` path during load, or derive `table.rows` length from the real
  sheet extent (`ref` minus header/totals) before constructing `Table`.
- Add regression test(s) under `spec/integration/` that round-trip a real fixture
  (per AGENTS.md requirement #4). Assert the table's `ref`, `headerRowCount`, and
  `totalsRowShown` survive `wb.xlsx.load()` → `wb.xlsx.writeBuffer()` unchanged.
- Excel-verify the fix per AGENTS.md requirement #6 (open in Excel, or round-trip
  through `soffice --headless`) before considering this done.

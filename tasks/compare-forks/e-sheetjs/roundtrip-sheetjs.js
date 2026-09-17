#!/usr/bin/env node
// Round-trips BookWithTable.xlsx through SheetJS (xlsx) so the raw XML
// parts can be diffed against the original. SheetJS has a different API
// than ExcelJS, so this is a separate script rather than a variant of
// roundtrip.js.
//
// Usage:
//   node roundtrip-sheetjs.js <input.xlsx> [outdir]

const path = require('path');
const fs = require('fs');
const XLSX = require('xlsx');

function main() {
  const input = process.argv[2];
  const outDir = process.argv[3] || path.join(__dirname, 'out');

  if (!input) {
    console.error('Usage: node roundtrip-sheetjs.js <input.xlsx> [outdir]');
    process.exit(1);
  }

  fs.mkdirSync(outDir, {recursive: true});
  const outputPath = path.join(outDir, `roundtrip-${path.basename(input)}`);

  const wb = XLSX.readFile(input, {cellStyles: true, bookVBA: true});

  console.log('[sheetjs] Loaded workbook. Sheets:', wb.SheetNames);
  wb.SheetNames.forEach(name => {
    const ws = wb.Sheets[name];
    const tables = ws['!tables'] || wb.Workbook?.Tables || [];
    console.log(`  Sheet "${name}" tables:`, tables);
  });

  XLSX.writeFile(wb, outputPath);
  console.log('[sheetjs] Wrote round-tripped file to', outputPath);
}

main();

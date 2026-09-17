#!/usr/bin/env node
// Round-trips BookWithTable.xlsx through a named exceljs package (installed
// in one of the sibling subdirectories) so the raw XML parts can be diffed.
//
// Usage:
//   node roundtrip.js <pkgDir> <pkgName> <input.xlsx> [outdir]
//
// Example:
//   node roundtrip.js a-exceljs exceljs BookWithTable.xlsx a-exceljs/out

const path = require('path');
const fs = require('fs');

async function main() {
  const pkgDir = process.argv[2];
  const pkgName = process.argv[3];
  const input = process.argv[4];
  const outDir = process.argv[5] || path.join(pkgDir, 'out');

  if (!pkgDir || !pkgName || !input) {
    console.error('Usage: node roundtrip.js <pkgDir> <pkgName> <input.xlsx> [outdir]');
    process.exit(1);
  }

  fs.mkdirSync(outDir, {recursive: true});

  const requirePath = require.resolve(pkgName, {paths: [path.resolve(pkgDir)]});
  const ExcelJS = require(requirePath);

  const outputPath = path.join(outDir, `roundtrip-${path.basename(input)}`);

  const wb = new ExcelJS.Workbook();
  await wb.xlsx.readFile(input);

  console.log(`[${pkgName}] Loaded workbook. Worksheets:`, wb.worksheets.map(ws => ws.name));
  wb.worksheets.forEach(ws => {
    const tables = ws.tables ? Object.keys(ws.tables) : [];
    console.log(`  Sheet "${ws.name}" tables:`, tables);
  });

  await wb.xlsx.writeFile(outputPath);
  console.log(`[${pkgName}] Wrote round-tripped file to`, outputPath);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});

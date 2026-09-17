#!/usr/bin/env node
// Reproduction harness for table-corruption bug.
//
// Loads a real Excel-created .xlsx (with a table) using this library,
// writes it back out, then unzips both the original and the round-tripped
// file so the raw XML parts can be diffed by hand or by ./diff.sh.
//
// Usage:
//   node dev/tasks/fix-table-corruption/harness/roundtrip.js <input.xlsx> [outdir]
//
// Example:
//   node dev/tasks/fix-table-corruption/harness/roundtrip.js dev/tasks/fix-table-corruption/harness/fixtures/BookWithTable.xlsx

const path = require('path');
const fs = require('fs');
const ExcelJS = require('../../../../excel');

async function main() {
  const input = process.argv[2];
  if (!input) {
    console.error('Usage: node roundtrip.js <input.xlsx> [outdir]');
    process.exit(1);
  }

  const outDir = process.argv[3] || path.join(__dirname, 'out');
  fs.mkdirSync(outDir, {recursive: true});

  const outputPath = path.join(outDir, `roundtrip-${path.basename(input)}`);

  const wb = new ExcelJS.Workbook();
  await wb.xlsx.readFile(input);

  console.log('Loaded workbook. Worksheets:', wb.worksheets.map(ws => ws.name));
  wb.worksheets.forEach(ws => {
    const tables = ws.tables ? Object.keys(ws.tables) : [];
    console.log(`  Sheet "${ws.name}" tables:`, tables);
  });

  await wb.xlsx.writeFile(outputPath);
  console.log('Wrote round-tripped file to', outputPath);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});

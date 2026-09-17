# Browser/jasmine tests (`npm run test:jasmine`, via `npm run test:browser`)

Command: `grunt jasmine` (config in [gruntfile.js](../../../gruntfile.js), `jasmine.dev` target)

Location: `spec/browser/exceljs.spec.js`, run against the built browser bundle `dist/exceljs.js` (requires `npm run build` first — this is why `test:full` runs `build` before the test scripts).

This is a small, flat suite (single top-level `describe`, no nesting) verifying the browser bundle works end-to-end. Because it's Jasmine (not Mocha), `mocha --dry-run` does not apply; the full list was read directly from the spec file instead of executed.

```
ExcelJS
  ✓ should read and write xlsx via binary buffer
  ✓ should read and write xlsx via base64 buffer
  ✓ should write csv via buffer
```

Note: `npm run test:browser` is a no-op if a `.disable-test-browser` file exists at the repo root.

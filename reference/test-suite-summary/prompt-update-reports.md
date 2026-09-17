---
description: This is an LLM prompt to update the test suite reports.
---

Update the test suite reports in `dev/tasks/test-suite-summary/reports/`.

1. Check `package.json` `scripts` for new/removed/renamed `test:*` entries not already covered by `generate-reports.sh` or `reports/README.md`. If found, update the script and README accordingly.
2. Run `dev/tasks/test-suite-summary/generate-reports.sh`.
3. Manually update `reports/jasmine-browser-tests.md` to match the current contents of `spec/browser/exceljs.spec.js` (it can't be dry-run).
4. Update the case-count table in `reports/README.md` if counts changed.

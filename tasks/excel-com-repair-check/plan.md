# Excel-COM repair-log capture module

## Context

AGENTS.md rule #6 requires that any PR touching xlsx serialization be "Excel-verified" —
either opened in real Excel with no repair warning, or round-tripped through
`soffice --headless`. Right now that verification is manual: someone opens the file in
Excel, watches for the "We found a problem with some content..." dialog, and eyeballs it.

This matters immediately for the active `fix-table-corruption` branch. The scratch
investigation at `dev/tasks/fix-table-corruption/` has already diagnosed two bugs
(`table-xform.js` header-row-count default, `worksheet.js` table-rows-clobbered-on-load)
that cause `roundtrip-BookWithTable.xlsx` to trigger Excel's repair dialog. `findings.md`
explicitly lists as a next step: "Excel-verify the fix per AGENTS.md requirement #6" —
and a regression test needs a way to assert *automatically* (not by a human watching a
dialog) that a given xlsx does or does not trigger repair.

The goal: a reusable module, callable from automated tests, that drives real Microsoft
Excel via COM automation to open an xlsx file, force the repair path
(`CorruptLoad = xlRepairFile`, no modal blocking), detect whether a repair actually
happened, and capture the repair log. This turns "Excel-verified" from a manual step into
an assertion a test can make.

**Scope for this phase: native Windows only.** This tooling only ever runs on a Windows
host with Excel Desktop installed — it is never part of CI (unless a Windows CI runner
with Excel gets set up later), so it has no obligation to run under WSL2 or Linux. The
user will do the actual implementation work on a native Windows host, not inside the WSL2
session where this plan was drafted. A WSL2-to-Windows bridging design was discussed but
is explicitly **deferred to a documented future-ideas file, not built now** (see below) —
no `index.js`/IPC/spawn layer needs to exist yet.

## Key design decisions

**No PowerShell for the production path, no winax/edge-js.** PowerShell has real
per-invocation startup overhead, and generic COM automation via PowerShell fights untyped
`IDispatch` calls. `winax` (native Node COM addon) requires node-gyp + VS Build Tools on
the target box just to `npm install`, coupling the module to the Node install's toolchain
unnecessarily. Research into current options confirms the better tradeoff for the shipped
tool is a **small precompiled C# console app** using `Microsoft.Office.Interop.Excel`
(strongly-typed, well-documented, no reflection-heavy COM calls) invoked as a subprocess.
Build it once (`dotnet publish`), ship the `.exe`, invoke via `child_process.execFile` (or
just run it directly from a test runner / npm script). Far lighter than PowerShell
startup, no native Node addon compilation, no toolchain coupling.

**Explore via PowerShell first, before writing the C# helper.** Before locking in the C#
implementation, write a throwaway PowerShell script that does the same COM calls
(`New-Object -ComObject Excel.Application`, `Workbooks.Open(..., CorruptLoad: 1)`). This
is cheap to iterate on interactively on the Windows host and lets us confirm, before
committing to a design:
- Whether the repair log ever exists anywhere in memory (a `Workbook`/`Application`
  property, an event payload) rather than only on disk — actually test the hypothesis
  using a real Excel session, instead of assuming the temp-file path is the only source.
- The exact shape/contents of the `error*_*.xml` file, and whether/how it identifies the
  repaired file unambiguously (see correlation question below).
- Confirm `DisplayAlerts = $false` actually suppresses the modal dialog under
  `CorruptLoad: xlRepairFile` before that assumption gets baked into a compiled app.

This PowerShell script is exploratory/manual-use only — not the shipped tool, since the
per-invocation-overhead concern about PowerShell still applies to the *production* path —
but is worth keeping as `explore.ps1` alongside the C# project as living documentation of
what was verified interactively, since it's cheap to keep and useful if the detection
strategy ever needs revisiting.

**Repair-log detection: confirmed empirically, no COM property needed.** Manually opening
the known-bad `roundtrip-BookWithTable.xlsx` in real Excel shows the actual repair dialog:

```text
Repairs to 'roundtrip-BookWithTable.xlsx'
Excel was able to open the file by repairing or removing the unreadable content.
Removed Feature: AutoFilter from /xl/tables/table1.xml part (Table)
Removed Feature: Table from /xl/tables/table1.xml part (Table)
Click to view log file listing repairs:
C:\Users\cspot\AppData\Local\Temp\error046160_01.xml
```

This confirms: there is **no inserted log sheet** and **no documented COM property** —
the log is written to a `%TEMP%\error<digits>_<NN>.xml` file, and that path is the ground
truth.

**How do we know a found log file matches the file we just repaired, and not some other
repair** (a concurrent test run, a leftover from a previous manual open)? Timing alone
(snapshot-before/diff-after) narrows the window but doesn't prove identity — two repairs
racing in the same few-hundred-ms window are possible, however unlikely in a serial test
run. The reliable check is **content-based**: the repair log XML itself very likely names
the file it repaired (the dialog shows `Repairs to 'roundtrip-BookWithTable.xlsx'`, and
that filename almost certainly also appears inside the log XML — the PowerShell
exploration phase confirms the exact tag/attribute). So the detection strategy is:

1. Snapshot `%TEMP%` (file listing + mtimes) immediately before calling
   `Workbooks.Open(path, CorruptLoad: XlCorruptLoad.xlRepairFile)`.
2. After `Open()` returns, diff `%TEMP%` for new files matching `error*_*.xml` created
   during the call.
3. For each candidate, **parse the XML and verify it references the input filename**
   (exact basename match, not just "a file appeared"). Only a file that both appeared
   during this call's window AND names our input file is accepted as `repaired: true`
   with that log attached. If a candidate appears but doesn't name our file (a genuine
   concurrent collision), skip it and keep looking / report ambiguous rather than
   silently misattributing.
4. Read and return the confirmed log file's contents directly.
5. Always quit Excel / release COM objects in a `finally`, regardless of outcome.

This two-part check (timing window + content match) is what makes the module safe to use
even if a developer has another Excel session open, rather than relying on either signal
alone.

## Deferred: WSL2-to-Windows bridging (do not build yet)

A design was discussed for making this callable from tests running inside this repo's
WSL2 session: a "subservient" `node.exe` process launched on the Windows side, talking to
the WSL side over stdio via newline-delimited JSON, which would in turn shell out to the
C# helper exe. This is **not being built now** — implementation for this phase happens
entirely on a native Windows host. Write this idea up as its own short markdown file in
this task directory (e.g. `wsl-bridge-idea.md`) so it's committed to git and available
if/when running these checks from WSL2 or from CI becomes a real need. It should cover:
subservient `node.exe` on the Windows side with a configurable path (WSL can't assume a
Windows Node install location), NDJSON-over-stdio as the IPC mechanism, and the principle
that the "drive Excel" logic should live in exactly one place regardless of which side
calls it.

## File layout (native Windows, this phase)

```
dev/tasks/excel-com-repair-check/
  plan.md                     # this file
  explore.ps1                 # throwaway/manual PowerShell exploration
  wsl-bridge-idea.md          # deferred-idea writeup (see above)
  csharp/
    ExcelRepairCheck.csproj
    Program.cs                 # Microsoft.Office.Interop.Excel automation + log extraction
    bin/excel-repair-check.exe # precompiled output
  README.md                    # usage, Windows-only + Excel-Desktop-required caveat,
                                # what "repaired" means, how the log-matching works
```

Exact placement of the C# project is the user's call once they're on the Windows host —
this is scaffolding, not a hard requirement.

## Program.cs behavior

```
Usage: excel-repair-check.exe <input.xlsx>

Opens <input.xlsx> via Excel.Application COM with CorruptLoad = xlRepairFile,
DisplayAlerts = false. Detects repair via %TEMP% snapshot-diff + content-match
against the input filename (see detection strategy above). Always quits Excel /
releases COM objects, even on error.

Prints one JSON object to stdout:
  { "repaired": bool, "logPath": string|null, "logXml": string|null, "error": string|null }
```

Keep it a single input path per invocation (no batch mode) — simplest to reason about and
matches how a test would call it (once per fixture).

## Regression test for the table-corruption fix (follow-on consumer, not this module's job)

Once the module exists and is confirmed working, add — per `fix-table-corruption/findings.md`'s
own stated next step — an integration test under `spec/integration/` (e.g.
`spec/integration/issues/table-corruption.spec.js`) that:

1. Round-trips `BookWithTable.xlsx` (promote the fixture from
   `dev/tasks/fix-table-corruption/harness/fixtures/` to
   `spec/integration/data/BookWithTable.xlsx`, per AGENTS.md rule #4's fixture-location
   convention) through `wb.xlsx.load()` → `wb.xlsx.writeBuffer()`.
2. Asserts in-model that `table.ref`/`headerRowCount`/`totalsRowShown` survive unchanged
   (fast, always runs, no Excel/COM dependency — this is the part that runs in CI).
3. Optionally, gated by an **explicit opt-in environment variable** (e.g.
   `EXCEL_COM_TESTS=1`), also invokes `excel-repair-check.exe` on the round-tripped output
   and asserts `repaired === false` — the actual Excel-verification AGENTS.md rule #6 asks
   for, now automated instead of manual.

**Gating must be explicit opt-in, not auto-skip based on capability detection.** If this
test silently skips whenever Excel/COM isn't detected, a real regression could go
unnoticed on every machine except a developer's own Windows box — which is nearly all of
them, today (including CI). Auto-skip risks someone believing Excel-verification happened
because the test "passed" (as a skip) when it never ran. So:

```js
describe('Excel COM repair check', function () {
  before(function () {
    if (!process.env.EXCEL_COM_TESTS) this.skip(); // explicit opt-in only, never auto
  });

  it('does not trigger repair after the table fix', async function () {
    const {repaired} = await checkExcelRepair(roundTrippedPath);
    assert.strictEqual(repaired, false);
  });
});
```

Running normally (`npm test`, CI) never sets `EXCEL_COM_TESTS`, so this test skips there —
but the skip is a documented, deliberate default, not an automatic capability-based one.
An engineer who wants to actually run the Excel-verification check sets
`EXCEL_COM_TESTS=1` explicitly on their Windows box. If a Windows CI runner with Excel
installed is ever set up, that pipeline would set `EXCEL_COM_TESTS=1` itself — explicit
even there, never inferred from platform detection.

This regression test lands alongside (or right after) the actual bug fixes in
`lib/xlsx/xform/table/table-xform.js` and `lib/doc/worksheet.js` — it's the reason this
module is being built, not part of the module's own scope for this phase.

## Plan of work

1. **PowerShell exploration** (`explore.ps1`, throwaway/manual-use, kept as
   documentation): on the Windows host, interactively drive `Excel.Application` COM to
   open the known-bad fixture with `CorruptLoad = 1`, and:
   - Confirm `DisplayAlerts = $false` actually suppresses the modal dialog under repair.
   - Locate the `error*_*.xml` file and inspect its actual XML structure — confirm which
     element/attribute names the repaired file, to nail down the content-match logic
     before writing it in C#.
   - Rule out (or find) any in-memory alternative to the temp file, now that there's a
     real session to poke at rather than relying on docs alone.
2. Implement `Program.cs` using the confirmed strategy: opens the target file with
   `CorruptLoad: XlCorruptLoad.xlRepairFile`, snapshot-before/diff-after `%TEMP%` plus
   content-match against the input filename (per the correlation strategy above) to find
   and confirm the right `error*_*.xml`, quits Excel/releases COM in `finally`, prints the
   JSON result described above. Compile via `dotnet publish` to `excel-repair-check.exe`.
3. Manually verify against both the known-bad and known-good fixtures (see Verification).
4. Write `README.md` documenting the Windows/Excel-Desktop requirement and the meaning of
   the returned `repaired`/`logXml` fields.
5. Write up the deferred WSL2-bridging idea as its own committed markdown file (see
   "Deferred" section above) — a short writeup, not an implementation.
6. (Follow-on, separate concern) Add the table-corruption regression test once the
   underlying bugs are fixed in `lib/`.

## Verification

- The dialog text captured above (`Removed Feature: AutoFilter ... Removed Feature: Table
  ...`) is the exact repair content the tool's log output should surface once parsed — use
  it as the expected-content check when validating `Program.cs` against the known-bad
  fixture.
- Run `excel-repair-check.exe` against
  `dev/tasks/fix-table-corruption/harness/out/roundtrip-BookWithTable.xlsx` (known-bad) and
  confirm `repaired: true` with a populated `logXml` naming that file.
- Run it against `dev/tasks/fix-table-corruption/harness/fixtures/BookWithTable.xlsx`
  (known-good) and confirm `repaired: false`.
- Confirm no orphaned `EXCEL.EXE` process remains after either run (wrap Excel
  quit/COM-release in `finally` in `Program.cs`; check via Task Manager or `tasklist`).
- Once the module works, run `npm run test:unit` / `npm run test:integration` in the
  WSL2/Linux session and confirm nothing here was disturbed (this phase adds no code under
  `spec/` or `lib/` yet, so this should be a no-op check).

---
prompt: >
  Read AGENTS.md, .claude/instructions.md, and CONTRIBUTING.md in full.
  Write a merged dev/reference/merged-instructions.md so I can read one file
  and be sure I am adhering to all requirements. Where instructions are
  effectively duplicated across files, include them once. Be terse, concise,
  direct, blunt; write in Simplified Technical English; embrace GOV.UK style.
  Include this prompt itself as a `prompt` field in YAML front-matter so the
  file can be regenerated.
---

# Merged Agent Instructions

Single reference for AGENTS.md, .claude/instructions.md, and CONTRIBUTING.md.
Source files remain authoritative if this file goes stale.

## What this fork is

Curated Protobi fork of exceljs/exceljs. Not a general-purpose fork. We adopt
only features we use in production.

Accepted:
- Bug fixes for features already in this fork.
- Improvements to fork-specific features (e.g. pivot tables).
- Well-tested, self-contained features with clear use cases, tests, docs.
- Reviewed, high-quality cherry-picks from upstream that we will maintain.

Not accepted:
- Large refactors.
- Features we don't use.
- Breaking changes.
- Incomplete, untested, or undocumented features.

Before contributing: check existing issues, open an issue first, keep PRs
small, test thoroughly, update docs.

## Hard scope rules

1. Touch only the lines required for the fix or feature. Do not extract
   constants, rename variables, rewrite loops, or "clean up" surrounding
   code.
2. No formatter sweeps. Do not run prettier/eslint `--fix` across whole
   files. Do not edit `.prettierrc`, `.eslintrc`, or other config files in a
   feature/bugfix PR — config changes get their own PR.
3. One concern per PR. Bug fix + sibling bugs of the same shape in the same
   file = one PR. Bug fix + cleanup + dep bump = separate PRs. Revert
   incidental edits to `index.d.ts`, `README.md`, `package-lock.json`, etc.
   unless they are the PR's actual subject.
4. If the prettier/eslint pre-commit hook conflicts, commit with
   `--no-verify` and state this in the PR description. Do not reshape code
   to satisfy the hook.

## Before opening a PR

- Run `gh pr list --state open --limit 50 --json number,title,files` and
  confirm no overlap with your changed files.
- List every changed file in the PR description, including configs and
  lockfiles.
- Note `--no-verify` use and why, if used.
- Link any dependent or conflicting open PR.

## Testing requirements

- Tests use real fixtures. XLSX read/write fixes must round-trip through
  `wb.xlsx.load(...)` / `wb.xlsx.writeBuffer(...)` against a real or minimal
  fixture file. Do not build hand-rolled model objects and call internal
  serializers (e.g. `XLSX.reconcile`, xforms) directly.
- Place fixture files under `spec/integration/data/` using existing naming.
- Tests live in `spec/unit/`, `spec/integration/`, `spec/end-to-end/`
  (Mocha).
- Fast unit run: `npm run test:unit`. Full suite: `npm test` (build + unit +
  integration + e2e + jasmine).
- Run tests before any version bump/release. Fix failures first.

## XLSX serialization changes

Any change touching xforms, sheet/workbook serialization, pivot tables,
charts, comments, or conditional formatting must be Excel-verified:

- Confirm the output opens in Excel without a "Repaired Records" warning, OR
- Round-trip with LibreOffice headless and inspect bytes:
  ```bash
  soffice --headless --convert-to xlsx /tmp/your-output.xlsx --outdir /tmp/roundtrip
  unzip -p /tmp/roundtrip/your-output.xlsx xl/<relevant-part>.xml | head
  ```
- Unit tests do not catch Excel repair warnings. This step is mandatory.

## Dependency bumps

Major-version bumps (e.g. `fast-csv`, `unzipper`, `archiver`) require a
runtime smoke test, not just `npm test`. Example: streaming reader change →
load a real `.xlsx`; CSV writer change → write and re-parse real CSV.
Document the smoke test in the PR.

Do not introduce dependencies that:
- Ship ES2021+ syntax (`??=`, `?.()`) in their CJS output, or
- Publish `exports`-only packages with no `main` field.

Both break the Browserify browser bundle.

## Per-PR checklist

- [ ] Only required lines changed
- [ ] No prettier/eslint sweep on unrelated files
- [ ] Every changed file listed in PR description
- [ ] Tests round-trip real fixtures via `wb.xlsx.load` / `writeBuffer`
- [ ] `gh pr list --state open` checked for conflicts
- [ ] (If serialization) Output verified in Excel or via `soffice --headless`
- [ ] (If `--no-verify` used) Reason stated in PR description
- [ ] (If dep bump) Runtime smoke test described

## Commits and issues (this session's workflow)

- **Wait for explicit user review and approval before committing.** Never
  commit automatically, even if tests pass and changes look correct. Show
  the diff, wait for approval, then commit. Exception: purely documentary
  changes explicitly requested — still confirm first.
- Every commit must reference a GitHub issue. Check for an existing issue
  before starting work; create one if none exists.
- Commit message format: `Update #<issue> <description>`, blank line,
  details.
- After committing, comment on the issue with the commit hash:
  `gh issue comment <issue-number> --repo protobi/exceljs --body "Fixed in commit <hash>"`

## Versioning

- Format: `<upstream-version>-protobi.<N>`, e.g. `4.4.0-protobi.1`.
- Base version matches upstream. Counter increments per fork release. Reset
  counter to `.1` when upstream base version changes.
- Bump version for: new features, fork-specific bug fixes, adopted upstream
  PRs — anything a consuming project should pick up via its git dependency.
  npm only re-fetches git-dependency changes when `package.json` version
  changes.
- Do not bump for: docs-only changes, internal tooling/CI changes, commits
  that will be reverted.
- Never publish to npm. Distributed via GitHub only.

Release steps:
```bash
npm version prerelease --preid=protobi
git commit -m "Release v<version>: <description>"
git tag -a v<version> -m "Fork release v<version>\n\nFeatures:\n- ...\n- Reference issues: (#1, #2)"
git push origin master --tags
```
Update FORK.md after release.

## Git remotes

`origin` = protobi/exceljs (this fork). `upstream` = exceljs/exceljs
(original). Keep both configured. Verify: `git remote -v`.

## Submitting PRs to upstream

Exclude fork identity from upstream PRs: no FORK.md, no fork-specific
CONTRIBUTING.md content, no `-protobi.X` version — reset `package.json` to
the matching upstream version before submitting.

Preferred method: create a clean branch from the pre-fork commit, cherry-pick
only the feature commits, reset `package.json` to upstream version, run
`npm install && npm test`, then push and `gh pr create --repo exceljs/exceljs --base master`.

## Adopting upstream PRs

```bash
git fetch upstream pull/<N>/head:pr-<N>
git diff master..pr-<N>          # review
git checkout pr-<N> && npm install && npm test   # verify
git checkout master
git merge pr-<N> --no-ff -m "Adopt upstream PR #<N>: <description>"
npm version prerelease --preid=protobi
git push origin master --tags
```

## File purposes

- `README.md` — main docs, kept upstream-compatible.
- `FORK.md` — fork identity, feature list, maintainer workflows.
- `CONTRIBUTING.md` — contribution guidelines.
- `AGENTS.md` — hard rules for AI-agent PRs (also applies to AI-generated
  code from humans).
- `package.json` — version must use `-protobi.X` format.
- `.claude/instructions.md` — session workflow reference (commits, issues,
  versioning, releases).

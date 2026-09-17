# Deferred idea: WSL2-to-Windows bridging for excel-repair-check

**Status: not built. Written up so the idea isn't lost, not as a spec to implement yet.**

## Problem

`excel-repair-check.exe` (see `csharp/`) only runs on native Windows — it needs a real
Excel Desktop install reachable via COM. This repo's day-to-day development happens inside
a WSL2 session. If/when a test running under WSL2 (or Linux CI) needs to invoke this check,
there's no direct way to reach Windows COM automation from that side.

## Idea: a subservient `node.exe` on the Windows side

Rather than trying to bridge COM itself across the WSL2/Windows boundary, run a small
long-lived (or spawned-per-call) Node process **on the Windows side**, and have the WSL2
side talk to it over stdio.

Shape:

- A `node.exe` process is started on Windows (e.g. via `powershell.exe`/`cmd.exe` from
  WSL2, or pre-started and reused), whose only job is: read newline-delimited JSON (NDJSON)
  requests from stdin, shell out to `excel-repair-check.exe` for each request, and write
  NDJSON responses to stdout.
- The WSL2 side spawns/talks to that Windows process, sends `{"inputPath": "..."}` lines,
  and reads back the `{repaired, logPath, logXml, error}` result lines.
- **The Windows Node executable's path must be configurable**, not assumed. WSL2 can't
  reliably guess where Node is installed on the Windows side (nvm-windows, a system
  install, a portable install, etc. all place it differently) — this needs to be an
  explicit config value (env var or config file), not autodetected.
- Path translation: the input `.xlsx` path needs converting between WSL2 paths
  (`/mnt/c/...` or a Linux-side temp file that needs copying out) and Windows paths
  (`C:\...`) at the boundary.

## Key principle

**The "drive Excel" logic lives in exactly one place** — `Program.cs` / the compiled
`excel-repair-check.exe` — regardless of which side (native Windows test runner, or a
WSL2/Linux test runner via this bridge) ends up calling it. The bridge is purely a
transport/IPC layer on top of the existing exe; it must not duplicate or reimplement any
of the COM automation, repair-detection, or log-matching logic described in `plan.md` and
`README.md`.

## Why NDJSON over stdio, not HTTP/sockets

Discussed as the simplest option: no port management, no firewall/networking concerns
crossing the WSL2/Windows boundary, and it composes naturally with spawning a process and
reading line-delimited output — which is already how the rest of this repo's test tooling
tends to shell out to things.

## Open questions for whenever this actually gets built

- Long-lived bridge process (started once, reused across many test-check calls) vs.
  spawned fresh per call? Long-lived avoids repeated Node startup cost but adds lifecycle
  management (who starts/stops it, crash recovery, stale-process cleanup).
- How does the WSL2 side discover/verify the Windows Node path is valid before first use,
  and fail with a clear error if misconfigured, rather than a cryptic spawn failure?
- Does the input `.xlsx` need to physically exist on a Windows-visible path (via `/mnt/c`
  or a copy step), or can WSL2's 9p-based Windows filesystem access handle it directly for
  reasonably-sized fixtures?
- Should the bridge also handle starting the actual `excel-repair-check.exe` build step
  (via `dotnet publish`) if the exe isn't found, or should that remain a separate,
  explicit setup step documented in `README.md`?

None of this needs answering now — this file exists so the design isn't re-derived from
scratch if/when running these checks from WSL2 or CI becomes a real requirement.

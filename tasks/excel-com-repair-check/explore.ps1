<#
.SYNOPSIS
  Exploratory script: drive Excel via COM to open a corrupt/repairable xlsx and
  find out exactly how the repair log surfaces, before writing the C# helper.

.DESCRIPTION
  Run this manually, interactively, on a Windows host with Excel Desktop installed.
  This is NOT the production tool (PowerShell has too much per-invocation overhead
  for that) - it's a throwaway harness to answer three open questions:

    1. Does DisplayAlerts = $false actually suppress the repair dialog when
       opening with CorruptLoad = xlRepairFile (1)?
    2. Where does the repair log actually end up - only %TEMP%\error*_*.xml,
       or is there anything readable in memory (Workbook/Application properties,
       an inserted "log" worksheet, an event)?
    3. What does the log XML actually look like - does it name the repaired file
       unambiguously, so a real tool can match a found log file back to the
       specific Open() call that produced it?

.PARAMETER InputPath
  Path to the xlsx file to open. Defaults to the known-bad fixture already
  produced by the exceljs round-trip harness in this repo.

.EXAMPLE
  .\explore.ps1
  .\explore.ps1 -InputPath "C:\path\to\some-other.xlsx"
#>

param(
  [string]$InputPath = (Join-Path $PSScriptRoot "..\fix-table-corruption\harness\out\roundtrip-BookWithTable.xlsx")
)

$InputPath = (Resolve-Path $InputPath).Path
Write-Host "Target file: $InputPath"

$tempDir = $env:TEMP
Write-Host "Watching for new repair-log files under: $tempDir"

# Question 2 (part 1): snapshot %TEMP% before opening, so we can diff afterwards.
$before = Get-ChildItem -Path $tempDir -Filter 'error*_*.xml' -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty FullName

$excel = $null
$workbook = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false   # Question 1: does this actually suppress the modal?

    # Workbooks.Open positional signature (VBA order):
    #   Filename, UpdateLinks, ReadOnly, Format, Password, WriteResPassword,
    #   IgnoreReadOnlyRecommended, Origin, Delimiter, Editable, Notify,
    #   Converter, AddToMru, Local, CorruptLoad
    # xlRepairFile = 1 (see Microsoft's XlCorruptLoad enum)
    $xlRepairFile = 1
    Write-Host "Opening with CorruptLoad = xlRepairFile ..."
    $workbook = $excel.Workbooks.Open(
        $InputPath, 0, $false, 5, "", "", $false, 1, "", $true, $false, $false, $false, $false, $xlRepairFile
    )
    Write-Host "Open() returned. Workbook name: $($workbook.Name)"

    # Question 2 (part 2): does the returned Workbook object expose anything about
    # a repair happening? Dump what's available so we can eyeball it.
    Write-Host ""
    Write-Host "=== Workbook.Sheets (looking for an inserted log sheet) ==="
    foreach ($sheet in $workbook.Sheets) {
        Write-Host " - $($sheet.Name)"
    }

    Write-Host ""
    Write-Host "=== Workbook properties that might hint at repair state ==="
    Write-Host "CorruptLoad property support varies by Excel version; try common candidates:"
    try { Write-Host "Workbook.FileFormat: $($workbook.FileFormat)" } catch {}
    try { Write-Host "Workbook.ReadOnly: $($workbook.ReadOnly)" } catch {}

    # Give Excel a moment to finish writing the log file to disk, if it's going to.
    Start-Sleep -Seconds 2

    # Question 2 (part 3) / Question 3: diff %TEMP% for new error*_*.xml files.
    $after = Get-ChildItem -Path $tempDir -Filter 'error*_*.xml' -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty FullName
    $newFiles = $after | Where-Object { $before -notcontains $_ }

    Write-Host ""
    if ($newFiles) {
        Write-Host "=== New repair-log file(s) found in %TEMP% ==="
        foreach ($f in $newFiles) {
            Write-Host ""
            Write-Host "--- $f ---"
            Get-Content -Path $f -Raw
        }
    } else {
        Write-Host "No new error*_*.xml file appeared in %TEMP%."
        Write-Host "If Excel showed a repair dialog anyway, the log naming pattern may differ -"
        Write-Host "manually check %TEMP% for any file modified in the last minute:"
        Get-ChildItem -Path $tempDir -ErrorAction SilentlyContinue |
            Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-1) } |
            Select-Object FullName, LastWriteTime
    }
}
finally {
    if ($workbook) {
        $workbook.Close($false)
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($workbook) | Out-Null
    }
    if ($excel) {
        $excel.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
    Write-Host ""
    Write-Host "Excel closed. Verify no orphaned EXCEL.EXE process remains:"
    Write-Host "  Get-Process EXCEL -ErrorAction SilentlyContinue"
}

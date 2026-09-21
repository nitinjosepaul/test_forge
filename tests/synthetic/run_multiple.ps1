<#
.SYNOPSIS
  Runs the synthetic flaky-demo test suite multiple times to generate a batch
  of historical JUnit XML reports for the flaky test detector.

.DESCRIPTION
  This is a temporary demo helper (pre-Sprint-1 stepping stone). It runs
  `pytest tests/synthetic` N times (default 10), writing one JUnit XML report
  per run under flaky_demo_suite/reports/run_<timestamp>.xml (suite root,
  not next to this script). These reports are the input for
  framework/normalize.py during the detector demo.

  The filename timestamp is purely cosmetic / for uniqueness - it lets you
  run this script repeatedly without tracking what files already exist or
  worrying about overwriting previous batches. framework/normalize.py does
  NOT rely on the filename for run_id or ordering; it reads the authoritative
  timestamp from each report's own internal <testsuite timestamp="..."/>
  attribute.

.PARAMETER Runs
  Number of times to execute the suite. Defaults to 10 (minimum agreed for
  the demo).
#>
param(
    [int]$Runs = 10
)

# This script now lives in tests/synthetic/, two levels below the demo
# suite root (flaky_demo_suite/). reports/ still lives at the suite root,
# not next to this script, so we walk up two levels to find it.
$testDir = $PSScriptRoot
$demoRoot = Split-Path (Split-Path $testDir -Parent) -Parent
$reportDir = Join-Path $demoRoot "reports"
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null

for ($i = 1; $i -le $Runs; $i++) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
    $reportPath = Join-Path $reportDir "run_$timestamp.xml"
    Write-Host "=== Run $i of $Runs ==="
    pytest "$testDir" --junitxml="$reportPath" -q
}

Write-Host ""
Write-Host "Done. $Runs reports written to $reportDir"

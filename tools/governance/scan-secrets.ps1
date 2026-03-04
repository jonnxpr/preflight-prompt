param([switch]$UpdateBaseline)
$ErrorActionPreference = "Stop"
if (-not (Test-Path "tasks")) { New-Item -ItemType Directory -Path "tasks" | Out-Null }
$report = "tasks/secret-scan.sarif"
$baseline = ".governance/gitleaks-baseline.json"
if (-not (Get-Command gitleaks -ErrorAction SilentlyContinue)) {
  Write-Error "gitleaks not found. Install: winget install gitleaks"
}
if ($UpdateBaseline) {
  gitleaks detect --source . --redact --report-format json --report-path $baseline
  Write-Host "Updated baseline: $baseline"
  exit 0
}
if (Test-Path $baseline) {
  gitleaks detect --source . --redact --report-format sarif --report-path $report --baseline-path $baseline
} else {
  gitleaks detect --source . --redact --report-format sarif --report-path $report
}
Write-Host "Report: $report"

param([switch]$UpdateBaseline)
$ErrorActionPreference = "Stop"
if (-not (Test-Path "tasks")) { New-Item -ItemType Directory -Path "tasks" | Out-Null }
$govDir = ".governance"
if (-not (Test-Path $govDir)) { New-Item -ItemType Directory -Path $govDir | Out-Null }
$report = "tasks/secret-scan.sarif"
$baseline = ".governance/gitleaks-baseline.json"
$gitleaks = Get-Command gitleaks -ErrorAction SilentlyContinue
$useBashFallback = $false
if (-not $gitleaks) {
  $bash = Get-Command bash -ErrorAction SilentlyContinue
  if ($bash) {
    & bash -lc "command -v gitleaks >/dev/null 2>&1"
    if ($LASTEXITCODE -eq 0) {
      $useBashFallback = $true
    }
  }
}

if (-not $gitleaks -and -not $useBashFallback) {
  Write-Warning "gitleaks not found in PowerShell or bash PATH. Secret scan skipped."
  if (-not (Test-Path "tasks")) { New-Item -ItemType Directory -Path "tasks" | Out-Null }
  "Secret scan skipped: gitleaks not available in current shell." | Out-File -FilePath "tasks/secret-scan.sarif" -Encoding utf8
  exit 0
}

function Invoke-Gitleaks([string]$argsLine) {
  if ($useBashFallback) {
    & bash -lc "gitleaks $argsLine"
  } else {
    & gitleaks $argsLine.Split(' ')
  }
}
if ($UpdateBaseline) {
  Invoke-Gitleaks "detect --source . --redact --report-format json --report-path $baseline --exit-code 0"
  Write-Host "Updated baseline: $baseline"
  exit 0
}
if (Test-Path $baseline) {
  Invoke-Gitleaks "detect --source . --redact --report-format sarif --report-path $report --baseline-path $baseline"
} else {
  Invoke-Gitleaks "detect --source . --redact --report-format sarif --report-path $report"
}
Write-Host "Report: $report"

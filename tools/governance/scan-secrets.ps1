param(
  [switch]$UpdateBaseline,
  [switch]$FailOnLeaks
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path "tasks")) { New-Item -ItemType Directory -Path "tasks" | Out-Null }
$govDir = ".governance"
if (-not (Test-Path $govDir)) { New-Item -ItemType Directory -Path $govDir | Out-Null }
$report = "tasks/secret-scan.sarif"
$baseline = ".governance/gitleaks-baseline.json"
$gitleaks = Get-Command gitleaks -ErrorAction SilentlyContinue
$useBashFallback = $false
$isGitRepo = $false

try {
  & git rev-parse --is-inside-work-tree *> $null
  if ($LASTEXITCODE -eq 0) {
    $isGitRepo = $true
  }
} catch {
  $isGitRepo = $false
}

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
  "Secret scan skipped: gitleaks not available in current shell." | Out-File -FilePath "tasks/secret-scan.sarif" -Encoding utf8
  exit 0
}

function Get-BashQuotedArg([string]$arg) {
  if ($null -eq $arg) { return '""' }
  return '"' + ($arg -replace '"', '\\"') + '"'
}

function Invoke-Gitleaks([string[]]$argsList) {
  if ($useBashFallback) {
    $quoted = ($argsList | ForEach-Object { Get-BashQuotedArg $_ }) -join ' '
    & bash -lc "gitleaks $quoted"
  } else {
    & gitleaks @argsList
  }
}

$scanModeArgs = @('detect', '--source', '.', '--redact', '--report-format', 'sarif', '--report-path', $report)
$baselineModeArgs = @('detect', '--source', '.', '--redact', '--report-format', 'json', '--report-path', $baseline, '--exit-code', '0')

if (-not $isGitRepo) {
  $scanModeArgs += '--no-git'
  $baselineModeArgs += '--no-git'
}

if (-not $FailOnLeaks) {
  $scanModeArgs += @('--exit-code', '0')
}

if ($UpdateBaseline) {
  Invoke-Gitleaks $baselineModeArgs
  Write-Host "Updated baseline: $baseline"
  exit 0
}
if (Test-Path $baseline) {
  $scanModeArgs += @('--baseline-path', $baseline)
  Invoke-Gitleaks $scanModeArgs
} else {
  Invoke-Gitleaks $scanModeArgs
}
Write-Host "Report: $report"

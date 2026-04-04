<#
.SYNOPSIS
    Install the Conventional Commits commit-msg hook into one or more Git repositories.

.DESCRIPTION
    Copies scripts/commit-msg into .git/hooks/commit-msg for each target repository.
    If a commit-msg hook already exists and was NOT installed by this script,
    it is preserved as commit-msg.user-backup so it chains automatically.

    Supports nested repos (e.g., meuagendamento has root + backend + frontend + landingPage).

.PARAMETER Targets
    One or more paths to Git repository roots. Defaults to common project repos.

.EXAMPLE
    .\install-commit-msg-hook.ps1
    .\install-commit-msg-hook.ps1 -Targets "C:\Users\jonathan.tavares\Documents\caradhras-poc"
#>

[CmdletBinding()]
param(
    [string[]]$Targets
)

$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$HookSource = Join-Path $ScriptRoot "commit-msg"
$MARKER = "preflight-prompt-commit-msg-hook"

if (-not (Test-Path $HookSource)) {
    Write-Error "Hook source not found: $HookSource"
    exit 1
}

# Default targets: all known project repos (including nested)
if (-not $Targets -or $Targets.Count -eq 0) {
    $Targets = @(
        "$env:USERPROFILE\Documents\meuagendamento",
        "$env:USERPROFILE\Documents\meuagendamento\backend",
        "$env:USERPROFILE\Documents\meuagendamento\frontend",
        "$env:USERPROFILE\Documents\meuagendamento\landingPage",
        "$env:USERPROFILE\Documents\caradhras-poc",
        "$env:USERPROFILE\Documents\Portfolio",
        "$env:USERPROFILE\Documents\HelenSantosPortfolio",
        "$env:USERPROFILE\Documents\preflight-prompt",
        "$env:USERPROFILE\Documents\meuagendamento-governance",
        "$env:USERPROFILE\Documents\caradhras-poc-governance",
        "$env:USERPROFILE\Documents\portfolio-governance",
        "$env:USERPROFILE\Documents\helen-santos-portfolio-governance",
        "$env:USERPROFILE\workspace\ambiente-partner\partner-governance"
    )
}

$installed = 0
$skipped = 0
$failed = 0

foreach ($repo in $Targets) {
    $gitDir = Join-Path $repo ".git"
    if (-not (Test-Path $gitDir)) {
        Write-Warning "Not a git repo (no .git): $repo"
        $skipped++
        continue
    }

    $hooksDir = Join-Path $gitDir "hooks"
    if (-not (Test-Path $hooksDir)) {
        New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
    }

    $hookDest = Join-Path $hooksDir "commit-msg"
    $backupDest = Join-Path $hooksDir "commit-msg.user-backup"

    # Check if already installed by us
    if (Test-Path $hookDest) {
        $existing = Get-Content $hookDest -Raw -ErrorAction SilentlyContinue
        if ($existing -and $existing.Contains($MARKER)) {
            Write-Host "[OK] Already installed: $repo" -ForegroundColor Green
            $installed++
            continue
        }
        # Preserve existing user hook
        Write-Host "[BACKUP] Preserving existing hook: $hookDest -> $backupDest" -ForegroundColor Yellow
        Copy-Item -Path $hookDest -Destination $backupDest -Force
    }

    try {
        Copy-Item -Path $HookSource -Destination $hookDest -Force
        Write-Host "[INSTALLED] $repo" -ForegroundColor Green
        $installed++
    }
    catch {
        Write-Error "Failed to install at $repo : $_"
        $failed++
    }
}

Write-Host ""
Write-Host "Summary: $installed installed, $skipped skipped, $failed failed" -ForegroundColor Cyan

param(
    [string]$WorkspaceRoot = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$currentDir = $WorkspaceRoot
if ($WorkspaceRoot -eq (Get-Location).Path) {
    $currentDir = (Get-Location).Path
}

function Resolve-GitRepoRoot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    try {
        $repoRoot = git -C $Path rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($repoRoot)) {
            return $repoRoot.Trim()
        }
    } catch {
    }

    return $null
}

$directRepoRoot = Resolve-GitRepoRoot -Path $currentDir
if ($directRepoRoot) {
    $repoRoot = $directRepoRoot
} else {
    $gitEntries = @(
        @(Get-ChildItem -Path $currentDir -Recurse -Force -Directory -Filter '.git' -ErrorAction SilentlyContinue)
        @(Get-ChildItem -Path $currentDir -Recurse -Force -File -Filter '.git' -ErrorAction SilentlyContinue)
    ) | Sort-Object { $_.FullName.Length }

    $candidateRoots = @()
    foreach ($gitEntry in $gitEntries) {
        $candidateRoot = Split-Path -Parent $gitEntry.FullName
        $resolvedRoot = Resolve-GitRepoRoot -Path $candidateRoot
        if ($resolvedRoot) {
            $candidateRoots += $resolvedRoot
        }
    }

    $repoRoot = $candidateRoots |
        Select-Object -Unique |
        Sort-Object Length, @{ Expression = { $_ } } |
        Select-Object -First 1
}

if (-not $repoRoot) {
    @{
        is_repo = $false
        repo_path = $null
        branch = $null
        has_changes = $false
        message = "No git repository found in $currentDir or subdirectories"
    } | ConvertTo-Json -Compress
    return
}

try {
    $branch = git -C $repoRoot rev-parse --abbrev-ref HEAD 2>$null
    if ([string]::IsNullOrEmpty($branch)) {
        $branch = "HEAD"
    }
} catch {
    $branch = "unknown"
}

try {
    $status = git -C $repoRoot status --porcelain 2>$null
    $hasChanges = $status.Length -gt 0
} catch {
    $hasChanges = $false
}

@{
    is_repo = $true
    repo_path = $repoRoot
    branch = $branch
    has_changes = $hasChanges
    message = "Found git repository at $repoRoot"
} | ConvertTo-Json -Compress

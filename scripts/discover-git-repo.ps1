param(
    [string]$WorkspaceRoot = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$currentDir = $WorkspaceRoot
if ($WorkspaceRoot -eq (Get-Location).Path) {
    $currentDir = Get-Location
}

$gitDirs = Get-ChildItem -Path $currentDir -Recurse -Directory -Filter ".git" -ErrorAction SilentlyContinue | 
           Sort-Object { $_.FullName.Length }

if ($gitDirs.Count -eq 0) {
    @{
        is_repo = $false
        repo_path = $null
        branch = $null
        has_changes = $false
        message = "No git repository found in $currentDir or subdirectories"
    } | ConvertTo-Json -Compress
    return
}

$gitDir = $gitDirs[0]
$repoRoot = $gitDir.Parent.FullName

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

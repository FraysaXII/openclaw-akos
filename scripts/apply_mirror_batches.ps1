# Apply compliance mirror DML chunks via supabase db query --linked --file.
# Canonical operator path: docs/guides/holistika-mirror-dml-apply.md (Method A).
# Idempotent (every chunk is INSERT ... ON CONFLICT DO UPDATE).
# Skips files passed via -SkipFile (e.g. chunk already applied during contract test).

[CmdletBinding()]
param(
    [ValidateSet("custom", "ops8615")]
    [string]$Preset = "custom",
    [string]$BatchDir = "",
    [string]$LogPath = "",
    [string[]]$SkipFile = @()
)

$RepoRoot = Split-Path -Parent $PSScriptRoot
if ($Preset -eq "ops8615") {
    $BatchDir = Join-Path $RepoRoot "docs/wip/planning/93-data-area-foundation-and-governance/artifacts/ops8615-batches"
}
if (-not $BatchDir) {
    $BatchDir = Join-Path $RepoRoot "artifacts/sql/mirror-batches/20260504"
}
if (-not $LogPath) {
    $leaf = Split-Path -Leaf ($BatchDir.TrimEnd("\"))
    $LogPath = Join-Path $RepoRoot "artifacts/sql/mirror-batches-apply-$leaf.log"
}
if (-not (Test-Path -LiteralPath $BatchDir)) {
    Write-Error "BatchDir not found: $BatchDir (run emit / --ops8615-split first)"
    exit 1
}
$BatchDir = (Resolve-Path -LiteralPath $BatchDir).Path

# Deliberately NOT setting ErrorActionPreference = Stop:
# npx supabase prints benign info ("Initialising login role...") to stderr,
# which PowerShell wraps as RemoteException; under Stop it aborts the loop.
# We rely on $LASTEXITCODE for real failures.
$ErrorActionPreference = "Continue"
$start = Get-Date

# Ensure log dir exists
$logDir = Split-Path -Parent $LogPath
if ($logDir -and -not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }

"=== mirror batch apply started $($start.ToString('o')) ===" | Out-File -FilePath $LogPath -Encoding utf8

$files = Get-ChildItem -Path $BatchDir -Filter "*.sql" | Sort-Object Name
$total = $files.Count
$applied = 0
$skipped = 0
$failed = 0
$idx = 0

foreach ($f in $files) {
    $idx++
    if ($SkipFile -contains $f.Name) {
        $skipped++
        $msg = "[$idx/$total] SKIP $($f.Name) (already applied)"
        Write-Host $msg
        Add-Content -Path $LogPath -Value $msg
        continue
    }

    $tStart = Get-Date
    Write-Host "[$idx/$total] APPLY $($f.Name) ($($f.Length) bytes)"
    Add-Content -Path $LogPath -Value "[$idx/$total] APPLY $($f.Name) ($($f.Length) bytes) start=$($tStart.ToString('o'))"

    # Run supabase db query and capture combined stdout/stderr
    $output = & npx supabase db query --linked --file $f.FullName 2>&1
    $exit = $LASTEXITCODE
    $tEnd = Get-Date
    $elapsed = ($tEnd - $tStart).TotalSeconds

    $output | ForEach-Object { Add-Content -Path $LogPath -Value "  | $_" }

    if ($exit -ne 0) {
        $failed++
        $err = "[$idx/$total] FAIL $($f.Name) exit=$exit elapsed=$([math]::Round($elapsed,1))s"
        Write-Host $err -ForegroundColor Red
        Add-Content -Path $LogPath -Value $err
        Add-Content -Path $LogPath -Value "ABORT: subsequent chunks not applied"
        break
    } else {
        $applied++
        $ok = "[$idx/$total] OK  $($f.Name) elapsed=$([math]::Round($elapsed,1))s"
        Write-Host $ok -ForegroundColor Green
        Add-Content -Path $LogPath -Value $ok
    }
}

$end = Get-Date
$totalElapsed = ($end - $start).TotalSeconds
$summary = "=== mirror batch apply finished applied=$applied skipped=$skipped failed=$failed total=$total elapsed=$([math]::Round($totalElapsed,1))s ==="
Write-Host $summary
Add-Content -Path $LogPath -Value $summary

if ($failed -gt 0) { exit 1 } else { exit 0 }

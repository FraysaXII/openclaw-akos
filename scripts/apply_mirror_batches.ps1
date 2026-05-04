# Apply compliance mirror DML chunks via supabase db query --linked --file.
# OPS-55-1 / Phase H6 driver. Idempotent (every chunk is INSERT ... ON CONFLICT DO UPDATE).
# Skips files passed via -SkipFile (e.g. chunk01 already applied during contract test).

[CmdletBinding()]
param(
    [string]$BatchDir = "artifacts/sql/mirror-batches/20260504",
    [string]$LogPath = "artifacts/sql/mirror-batches-apply-20260504.log",
    [string[]]$SkipFile = @("10-persona_scenario_registry_mirror-chunk01.sql")
)

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

#Requires -Version 5.1
<#
.SYNOPSIS
    OpenCLAW-AKOS full environment bootstrap (Windows + Ollama + MCP).
.DESCRIPTION
    Reproduces every installation and configuration step from the SOP
    (Sections 3.0-5.0, Task Registry 8.3-8.5) to bring a clean Windows
    machine to a working OpenCLAW stack with local Ollama inference and
    three MCP servers.

    Idempotent: each phase detects current state and skips work already done.
    Non-destructive: openclaw.json is patched (never overwritten) and backed
    up before modification.

    SOP Reference: SOP-OPENCLAW_LLMOS_UPGRADE_002 v2.1
.NOTES
    Run from the repo root:  .\scripts\bootstrap.ps1
    Requires: PowerShell 5.1+, Node.js >= 22, Ollama running, gh CLI (optional).
#>

[CmdletBinding()]
param(
    [switch]$SkipWSL,
    [switch]$SkipOllama,
    [switch]$SkipMCP,
    [string]$PrimaryModel = "deepseek-r1:14b",
    [string]$EmbedModel   = "nomic-embed-text"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

$script:PassCount = 0
$script:FailCount = 0
$script:SkipCount = 0
$script:WarnCount = 0
$script:Summary   = [System.Collections.ArrayList]::new()

function Write-Status {
    param(
        [ValidateSet("PASS","FAIL","SKIP","WARN","INFO")]
        [string]$Level,
        [string]$Message
    )
    $colors = @{ PASS = "Green"; FAIL = "Red"; SKIP = "DarkYellow"; WARN = "Yellow"; INFO = "Cyan" }
    $tag    = "[$Level]"
    Write-Host "$tag " -ForegroundColor $colors[$Level] -NoNewline
    Write-Host $Message
    switch ($Level) {
        "PASS" { $script:PassCount++ }
        "FAIL" { $script:FailCount++ }
        "SKIP" { $script:SkipCount++ }
        "WARN" { $script:WarnCount++ }
    }
}

function Add-SummaryRow {
    param([string]$Component, [string]$Status, [string]$Detail)
    [void]$script:Summary.Add([PSCustomObject]@{
        Component = $Component
        Status    = $Status
        Detail    = $Detail
    })
}

function Test-CommandExists([string]$Cmd) {
    $null -ne (Get-Command $Cmd -ErrorAction SilentlyContinue)
}

function Invoke-OllamaApi {
    param([string]$Path, [string]$Method = "GET", [string]$Body)
    $uri = "http://localhost:11434$Path"
    $params = @{ Uri = $uri; Method = $Method; UseBasicParsing = $true; TimeoutSec = 30 }
    if ($Body) {
        $params.Body        = $Body
        $params.ContentType = "application/json"
    }
    (Invoke-WebRequest @params).Content | ConvertFrom-Json
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot  = Split-Path -Parent $ScriptDir
$ConfigDir = Join-Path $RepoRoot "config"
$OpenClawHome = Join-Path $env:USERPROFILE ".openclaw"

# ===================================================================
# PHASE 0 -- Preflight
# ===================================================================
Write-Host ""
Write-Host "===== PHASE 0: Preflight Checks =====" -ForegroundColor Magenta
Write-Host ""

# Windows version
$os = Get-CimInstance Win32_OperatingSystem
Write-Status INFO "Windows $($os.Version) -- $($os.Caption)"
Add-SummaryRow "Windows" "OK" $os.Version

# RAM
$ramGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
Write-Status INFO "System RAM: ${ramGB} GB"
if ($ramGB -lt 8) {
    Write-Status WARN "Less than 8 GB RAM -- large models may not fit."
}
Add-SummaryRow "RAM" "OK" "${ramGB} GB"

# GPU
if (Test-CommandExists "nvidia-smi") {
    $gpuInfo = & nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>$null
    if ($gpuInfo) {
        Write-Status PASS "NVIDIA GPU: $($gpuInfo.Trim())"
        Add-SummaryRow "GPU" "PASS" $gpuInfo.Trim()
    }
} else {
    Write-Status WARN "nvidia-smi not found -- GPU acceleration may be unavailable."
    Add-SummaryRow "GPU" "WARN" "nvidia-smi not on PATH"
}

# Node.js
if (Test-CommandExists "node") {
    $nodeVer = (& node -v).TrimStart("v")
    $nodeMajor = [int]($nodeVer.Split(".")[0])
    if ($nodeMajor -ge 22) {
        Write-Status PASS "Node.js v$nodeVer (>= 22 required)"
        Add-SummaryRow "Node.js" "PASS" "v$nodeVer"
    } else {
        Write-Status FAIL "Node.js v$nodeVer is too old (>= 22 required). Install from https://nodejs.org"
        Add-SummaryRow "Node.js" "FAIL" "v${nodeVer} -- too old"
    }
} else {
    Write-Status FAIL "Node.js not found. Install from https://nodejs.org (LTS >= 22)"
    Add-SummaryRow "Node.js" "FAIL" "not installed"
}

# Ollama
$ollamaRunning = $false
try {
    $tags = Invoke-OllamaApi "/api/tags"
    $ollamaRunning = $true
    $modelCount = ($tags.models | Measure-Object).Count
    Write-Status PASS "Ollama is running -- $modelCount models available"
    Add-SummaryRow "Ollama" "PASS" "$modelCount models"
} catch {
    Write-Status FAIL "Ollama is not responding on localhost:11434. Install from https://ollama.com"
    Add-SummaryRow "Ollama" "FAIL" "not running"
}

# gh CLI
$ghAuthed = $false
if (Test-CommandExists "gh") {
    try {
        $null = & gh auth status 2>&1
        if ($LASTEXITCODE -eq 0) {
            $ghAuthed = $true
            Write-Status PASS "gh CLI authenticated"
            Add-SummaryRow "gh CLI" "PASS" "authenticated"
        } else {
            Write-Status WARN "gh CLI installed but not authenticated (run: gh auth login)"
            Add-SummaryRow "gh CLI" "WARN" "not authenticated"
        }
    } catch {
        Write-Status WARN "gh CLI check failed: $_"
        Add-SummaryRow "gh CLI" "WARN" "check error"
    }
} else {
    Write-Status WARN "gh CLI not found -- GitHub MCP server will not have a token."
    Add-SummaryRow "gh CLI" "WARN" "not installed"
}

# Elevated?
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
           ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isAdmin) {
    Write-Status WARN "Running as Administrator. Ollama and OpenCLAW normally run as the current user."
}

# ===================================================================
# PHASE 1 -- WSL + Linux Environment
# ===================================================================
Write-Host ""
Write-Host "===== PHASE 1: WSL + Linux Environment =====" -ForegroundColor Magenta
Write-Host ""

if ($SkipWSL) {
    Write-Status SKIP "WSL phase skipped per -SkipWSL flag."
    Add-SummaryRow "WSL" "SKIP" "flag"
} else {
    $wslAvailable = $false
    $distroReady  = $false

    # Detect WSL status
    try {
        $wslList = & wsl --list --verbose 2>&1 | Out-String
        if ($wslList -match "Ubuntu") {
            $wslAvailable = $true
            $distroReady  = $true
            $wslVersion = if ($wslList -match "Ubuntu.*\s+(\d)") { $Matches[1] } else { "?" }
            Write-Status PASS "Ubuntu detected in WSL -- version $wslVersion"
            Add-SummaryRow "WSL distro" "PASS" "Ubuntu WSL${wslVersion}"
        } else {
            $wslAvailable = $true
            Write-Status INFO "WSL is installed but no Ubuntu distro found."
        }
    } catch {
        Write-Status INFO "WSL not detected. Will attempt install."
    }

    # Install Ubuntu if missing
    if ($wslAvailable -and -not $distroReady) {
        Write-Status INFO "Attempting: wsl --install --web-download -d Ubuntu-24.04"
        try {
            $installOut = & wsl --install --web-download -d Ubuntu-24.04 2>&1 | Out-String
            if ($installOut -match "HCS_E_HYPERV_NOT_INSTALLED") {
                Write-Status WARN "WSL2 unavailable (nested virtualization not supported on this host)."
                Write-Status INFO "Falling back to WSL1: wsl --set-version Ubuntu-24.04 1"
                try {
                    & wsl --set-version Ubuntu-24.04 1 2>&1 | Out-Null
                    Write-Status PASS "Ubuntu-24.04 set to WSL1."
                    $distroReady = $true
                    Add-SummaryRow "WSL distro" "PASS" "Ubuntu-24.04 (WSL1 fallback)"
                } catch {
                    Write-Status FAIL "WSL1 fallback failed. Manual intervention required."
                    Add-SummaryRow "WSL distro" "FAIL" "install failed"
                }
            } elseif ($LASTEXITCODE -eq 0) {
                Write-Status PASS "Ubuntu-24.04 installed."
                $distroReady = $true
                Add-SummaryRow "WSL distro" "PASS" "Ubuntu-24.04 (fresh install)"
            } else {
                Write-Status FAIL "WSL install returned unexpected output. May need a reboot."
                Write-Status INFO "Run in elevated PowerShell if features are missing:"
                Write-Host "  dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart"
                Write-Host "  dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart"
                Write-Host "  Restart-Computer"
                Add-SummaryRow "WSL distro" "FAIL" "needs reboot/elevation"
            }
        } catch {
            Write-Status FAIL "WSL install command failed: $_"
            Add-SummaryRow "WSL distro" "FAIL" "$_"
        }
    }

    # Provision service account inside WSL
    if ($distroReady) {
        Write-Status INFO "Provisioning openclaw service account in WSL..."
        $wslSetup = @'
set -e
if id openclaw >/dev/null 2>&1; then
    echo "SKIP: openclaw user already exists"
else
    sudo adduser --system --group openclaw
    echo "CREATED: openclaw user"
fi
if [ -d /opt/openclaw ]; then
    echo "SKIP: /opt/openclaw already exists"
else
    sudo mkdir -p /opt/openclaw
    sudo chown openclaw:openclaw /opt/openclaw
    echo "CREATED: /opt/openclaw"
fi
'@
        try {
            $setupResult = & wsl -d Ubuntu-24.04 -- bash -c $wslSetup 2>&1 | Out-String
            foreach ($line in ($setupResult -split "`n" | Where-Object { $_.Trim() })) {
                if ($line -match "^SKIP:") {
                    Write-Status SKIP $line.Trim()
                } elseif ($line -match "^CREATED:") {
                    Write-Status PASS $line.Trim()
                } else {
                    Write-Status INFO $line.Trim()
                }
            }
            Add-SummaryRow "WSL service account" "PASS" "openclaw:/opt/openclaw"
        } catch {
            Write-Status WARN "Could not provision WSL service account: $_"
            Add-SummaryRow "WSL service account" "WARN" "manual setup needed"
        }
    }
}

# ===================================================================
# PHASE 2 -- Ollama Model Provisioning
# ===================================================================
Write-Host ""
Write-Host "===== PHASE 2: Ollama Model Provisioning =====" -ForegroundColor Magenta
Write-Host ""

if ($SkipOllama -or -not $ollamaRunning) {
    $reason = if ($SkipOllama) { "flag" } else { "Ollama not running" }
    Write-Status SKIP "Ollama phase skipped -- $reason."
    Add-SummaryRow "Ollama models" "SKIP" $reason
} else {
    $existingModels = ($tags.models | ForEach-Object { $_.name }) -join ","

    foreach ($model in @($PrimaryModel, $EmbedModel)) {
        $shortName = $model.Split(":")[0]
        if ($existingModels -match [regex]::Escape($shortName)) {
            Write-Status SKIP "Model '$model' already pulled."
            Add-SummaryRow "Model: $model" "SKIP" "present"
        } else {
            Write-Status INFO "Pulling model '$model' (this may take several minutes)..."
            try {
                & ollama pull $model 2>&1 | Out-String | ForEach-Object { Write-Host "  $_" }
                Write-Status PASS "Model '$model' pulled."
                Add-SummaryRow "Model: $model" "PASS" "pulled"
            } catch {
                Write-Status FAIL "Failed to pull '$model': $_"
                Add-SummaryRow "Model: $model" "FAIL" "$_"
            }
        }
    }

    # GPU smoke test
    Write-Status INFO "Running GPU inference smoke test with $PrimaryModel..."
    try {
        $body = @{
            model  = $PrimaryModel
            prompt = "Reply with exactly: GPU OK"
            stream = $false
        } | ConvertTo-Json
        $resp = Invoke-OllamaApi "/api/generate" -Method POST -Body $body
        if ($resp.response) {
            Write-Status PASS "Inference OK: $($resp.response.Substring(0, [Math]::Min(60, $resp.response.Length)).Trim())"
        } else {
            Write-Status WARN "Inference returned empty response."
        }
        Add-SummaryRow "GPU inference" "PASS" $PrimaryModel
    } catch {
        Write-Status FAIL "Inference test failed: $_"
        Add-SummaryRow "GPU inference" "FAIL" "$_"
    }

    # VRAM check
    if (Test-CommandExists "nvidia-smi") {
        $vramUsed = & nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>$null
        if ($vramUsed) {
            Write-Status INFO "GPU VRAM in use: $($vramUsed.Trim()) MiB"
        }
    }
}

# ===================================================================
# PHASE 3 -- OpenCLAW Configuration
# ===================================================================
Write-Host ""
Write-Host "===== PHASE 3: OpenCLAW Configuration =====" -ForegroundColor Magenta
Write-Host ""

$ocConfigPath = Join-Path $OpenClawHome "openclaw.json"
$exportsDir   = Join-Path (Join-Path $OpenClawHome "workspace") "exports"

if (-not (Test-Path $ocConfigPath)) {
    Write-Status WARN "openclaw.json not found at $ocConfigPath."
    Write-Status INFO "Run 'openclaw onboard --install-daemon' to create it, then re-run this script."
    Add-SummaryRow "openclaw.json" "WARN" "not found"
} else {
    $ocRaw    = Get-Content $ocConfigPath -Raw
    $ocConfig = $ocRaw | ConvertFrom-Json
    $patched  = $false

    # Patch primary model
    $currentPrimary = $ocConfig.agents.defaults.model.primary
    $targetPrimary  = "ollama/$PrimaryModel"
    if ($currentPrimary -eq $targetPrimary) {
        Write-Status SKIP "Primary model already set to '$targetPrimary'."
    } else {
        Write-Status INFO "Patching primary model: '$currentPrimary' -> '$targetPrimary'"
        $backupPath = "$ocConfigPath.bak-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $ocConfigPath $backupPath
        Write-Status INFO "Backup saved to $backupPath"
        $ocConfig.agents.defaults.model.primary = $targetPrimary
        $patched = $true
    }

    # Enable reasoning on the primary model
    $modelDef = $ocConfig.models.providers.ollama.models | Where-Object { $_.id -eq $PrimaryModel }
    if ($modelDef) {
        if ($modelDef.reasoning -eq $true) {
            Write-Status SKIP "reasoning already enabled on '$PrimaryModel'."
        } else {
            Write-Status INFO "Enabling reasoning: true on '$PrimaryModel'."
            $modelDef.reasoning = $true
            $patched = $true
        }
    } else {
        Write-Status WARN "Model definition for '$PrimaryModel' not found in openclaw.json -- add it manually."
    }

    if ($patched) {
        $ocConfig | ConvertTo-Json -Depth 20 | Set-Content $ocConfigPath -Encoding UTF8
        # Validate round-trip
        try {
            $null = Get-Content $ocConfigPath -Raw | ConvertFrom-Json
            Write-Status PASS "openclaw.json patched and validated."
        } catch {
            Write-Status FAIL "JSON validation failed after patching! Restoring backup."
            Copy-Item $backupPath $ocConfigPath -Force
        }
    }
    Add-SummaryRow "openclaw.json" "PASS" "primary=$targetPrimary"
}

# Playwright exports directory
if (Test-Path $exportsDir) {
    Write-Status SKIP "Playwright exports directory already exists: $exportsDir"
} else {
    New-Item -ItemType Directory -Path $exportsDir -Force | Out-Null
    Write-Status PASS "Created Playwright exports directory: $exportsDir"
}
Add-SummaryRow "Exports dir" "PASS" $exportsDir

# ===================================================================
# PHASE 4 -- MCP Provisioning (T-2.1 through T-2.8)
# ===================================================================
Write-Host ""
Write-Host "===== PHASE 4: MCP Provisioning =====" -ForegroundColor Magenta
Write-Host ""

if ($SkipMCP) {
    Write-Status SKIP "MCP phase skipped per -SkipMCP flag."
    Add-SummaryRow "MCP" "SKIP" "flag"
} else {
    # mcporter CLI
    if (Test-CommandExists "mcporter") {
        $mcpVer = & mcporter --version 2>&1 | Out-String
        Write-Status SKIP "mcporter already installed: $($mcpVer.Trim())"
        Add-SummaryRow "mcporter" "SKIP" $mcpVer.Trim()
    } else {
        Write-Status INFO "Installing mcporter globally..."
        & npm install -g mcporter 2>&1 | Out-Null
        if (Test-CommandExists "mcporter") {
            $mcpVer = & mcporter --version 2>&1 | Out-String
            Write-Status PASS "mcporter installed: $($mcpVer.Trim())"
            Add-SummaryRow "mcporter" "PASS" $mcpVer.Trim()
        } else {
            Write-Status FAIL "mcporter install failed. Try manually: npm install -g mcporter"
            Add-SummaryRow "mcporter" "FAIL" "npm install failed"
        }
    }

    # Generate config/mcporter.json from template
    $mcpLive     = Join-Path $ConfigDir "mcporter.json"
    $mcpTemplate = Join-Path $ConfigDir "mcporter.json.example"
    if (Test-Path $mcpLive) {
        Write-Status SKIP "config/mcporter.json already exists."
        Add-SummaryRow "mcporter.json" "SKIP" "exists"
    } elseif (-not (Test-Path $mcpTemplate)) {
        Write-Status FAIL "Template not found: $mcpTemplate"
        Add-SummaryRow "mcporter.json" "FAIL" "no template"
    } else {
        $templateObj = Get-Content $mcpTemplate -Raw | ConvertFrom-Json
        $pwArgs = $templateObj.mcpServers.playwright.args
        for ($i = 0; $i -lt $pwArgs.Count; $i++) {
            if ($pwArgs[$i] -eq "/opt/openclaw/workspace/exports") {
                $pwArgs[$i] = $exportsDir.Replace("\", "\\")
            }
        }
        # Custom AKOS MCP: resolve script path so mcporter can spawn from any cwd
        if ($templateObj.mcpServers.akos) {
            $akosScript = (Join-Path $RepoRoot "scripts\mcp_akos_server.py") -replace '\\', '/'
            $templateObj.mcpServers.akos.args[0] = $akosScript
        }
        $templateObj | ConvertTo-Json -Depth 10 | Set-Content $mcpLive -Encoding UTF8
        Write-Status PASS "Generated config/mcporter.json from template -- Playwright dir: $exportsDir"
        Add-SummaryRow "mcporter.json" "PASS" "generated from template"
    }

    # GITHUB_TOKEN
    if ($env:GITHUB_TOKEN) {
        $tokenLen = $env:GITHUB_TOKEN.Length
        Write-Status SKIP "GITHUB_TOKEN already set -- $tokenLen chars."
        Add-SummaryRow "GITHUB_TOKEN" "SKIP" "set -- $tokenLen chars"
    } elseif ($ghAuthed) {
        Write-Status INFO "Extracting GITHUB_TOKEN from gh CLI..."
        try {
            $token = (& gh auth token 2>&1).Trim()
            if ($token -and $token.Length -gt 10) {
                [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $token, "User")
                $env:GITHUB_TOKEN = $token
                Write-Status PASS "GITHUB_TOKEN set as User environment variable -- $($token.Length) chars."
                Add-SummaryRow "GITHUB_TOKEN" "PASS" "from gh CLI -- $($token.Length) chars"
            } else {
                Write-Status WARN "gh auth token returned unexpected value."
                Add-SummaryRow "GITHUB_TOKEN" "WARN" "unexpected output"
            }
        } catch {
            Write-Status WARN "Could not extract token: $_"
            Add-SummaryRow "GITHUB_TOKEN" "WARN" "$_"
        }
    } else {
        Write-Status WARN "No GITHUB_TOKEN and gh CLI not authenticated. GitHub MCP will be limited."
        Write-Status INFO "To fix: gh auth login, then re-run this script."
        Add-SummaryRow "GITHUB_TOKEN" "WARN" "not set"
    }

    # MCP health check
    if (Test-CommandExists "mcporter") {
        Write-Status INFO "Running MCP consolidated health check..."
        try {
            $mcpList = & mcporter list 2>&1 | Out-String
            Write-Host $mcpList
            if ($mcpList -match "sequential-thinking" -and $mcpList -match "playwright" -and $mcpList -match "github") {
                Write-Status PASS "All three MCP servers detected."
                Add-SummaryRow "MCP servers" "PASS" "3/3 healthy"
            } else {
                Write-Status WARN "Not all MCP servers detected in mcporter list output."
                Add-SummaryRow "MCP servers" "WARN" "check output above"
            }
        } catch {
            Write-Status WARN "mcporter list failed: $_"
            Add-SummaryRow "MCP servers" "WARN" "$_"
        }
    }
}

# ===================================================================
# PHASE 5 -- Final Summary
# ===================================================================
Write-Host ""
Write-Host "===== PHASE 5: Summary =====" -ForegroundColor Magenta
Write-Host ""

$script:Summary | Format-Table -AutoSize -Property Component, Status, Detail

Write-Host ""
Write-Host "Totals: " -NoNewline
Write-Host "$($script:PassCount) passed" -ForegroundColor Green -NoNewline
Write-Host ", $($script:SkipCount) skipped" -ForegroundColor DarkYellow -NoNewline
Write-Host ", $($script:WarnCount) warnings" -ForegroundColor Yellow -NoNewline
Write-Host ", $($script:FailCount) failed" -ForegroundColor Red
Write-Host ""

if ($script:FailCount -gt 0) {
    Write-Host "Some steps failed. Review the output above and re-run after fixing." -ForegroundColor Red
    exit 1
} elseif ($script:WarnCount -gt 0) {
    Write-Host "Setup complete with warnings. Review yellow items above." -ForegroundColor Yellow
} else {
    Write-Host "All checks passed. OpenCLAW-AKOS environment is ready." -ForegroundColor Green
}

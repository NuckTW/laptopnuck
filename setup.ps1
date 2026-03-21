# ============================================================
# LAPTOP-Nuck — nuck001 OpenClaw Setup Script
# Run this on LAPTOP-Nuck (PowerShell as Administrator)
# ============================================================

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  [!!] $msg" -ForegroundColor Yellow }
function Write-Fail($msg) { Write-Host "  [XX] $msg" -ForegroundColor Red }

# ── STEP 1: Remove old OpenClaw ──────────────────────────────
Write-Step "Removing old OpenClaw installation"

# Uninstall old npm package (any name variant)
foreach ($pkg in @("openclaw", "@openclaw/cli", "clawd", "moltbot")) {
    $installed = npm list -g $pkg --depth=0 2>$null
    if ($installed -match $pkg) {
        npm uninstall -g $pkg 2>$null
        Write-Ok "Removed npm package: $pkg"
    }
}

# Remove old OpenClaw data directories
$oldPaths = @(
    "$env:USERPROFILE\.openclaw",
    "$env:USERPROFILE\.clawd",
    "$env:USERPROFILE\.moltbot",
    "$env:APPDATA\openclaw",
    "$env:LOCALAPPDATA\openclaw",
    "$env:APPDATA\clawd",
    "$env:LOCALAPPDATA\clawd"
)
foreach ($path in $oldPaths) {
    if (Test-Path $path) {
        Remove-Item -Recurse -Force $path
        Write-Ok "Removed: $path"
    }
}

Write-Ok "Old OpenClaw cleanup complete"

# ── STEP 2: Check Node.js ────────────────────────────────────
Write-Step "Checking prerequisites"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Fail "Node.js not found. Install from https://nodejs.org/ (v20+ recommended) then re-run this script."
    exit 1
}
$nodeVer = node --version
Write-Ok "Node.js $nodeVer"

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Fail "npm not found. It should come with Node.js."
    exit 1
}
$npmVer = npm --version
Write-Ok "npm $npmVer"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Fail "git not found. Install from https://git-scm.com/"
    exit 1
}
Write-Ok "git $(git --version)"

# ── STEP 3: Install OpenClaw ─────────────────────────────────
Write-Step "Installing OpenClaw"

npm install -g openclaw
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Failed to install openclaw. Check npm error above."
    exit 1
}
Write-Ok "OpenClaw installed: $(openclaw --version 2>$null)"

# ── STEP 4: Install ClawHub skills ───────────────────────────
Write-Step "Installing skills from ClawHub"

$skills = @(
    "skill-vetter",
    "find-skills",
    "skill-creator",
    "agent-browser",
    "playwright-cli",
    "memory-setup"
)

foreach ($skill in $skills) {
    Write-Host "  Installing: $skill ..." -ForegroundColor White
    clawhub install $skill
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "$skill installed"
    } else {
        Write-Warn "$skill install failed — you can install manually later: clawhub install $skill"
    }
}

# ── STEP 5: Install Playwright browsers ──────────────────────
Write-Step "Installing Playwright Chromium browser"

npx playwright install chromium
if ($LASTEXITCODE -eq 0) {
    Write-Ok "Playwright Chromium installed"
} else {
    Write-Warn "Playwright install failed — run 'npx playwright install chromium' manually"
}

# ── STEP 6: Copy custom skills into OpenClaw ─────────────────
Write-Step "Registering custom skills"

$openclawSkillsDir = "$env:USERPROFILE\.openclaw\skills"
if (-not (Test-Path $openclawSkillsDir)) {
    New-Item -ItemType Directory -Force -Path $openclawSkillsDir | Out-Null
}

$localSkills = Get-ChildItem -Path ".\skills\*.md" -ErrorAction SilentlyContinue
foreach ($skillFile in $localSkills) {
    Copy-Item $skillFile.FullName -Destination $openclawSkillsDir -Force
    Write-Ok "Registered custom skill: $($skillFile.Name)"
}

# ── STEP 7: Setup environment ────────────────────────────────
Write-Step "Setting up environment"

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Warn ".env created from template — EDIT IT with your real credentials before starting!"
    Write-Host "  Required: ANTHROPIC_API_KEY, TELEGRAM_TOKEN, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET" -ForegroundColor White
} else {
    Write-Ok ".env already exists"
}

# ── STEP 8: Configure OpenClaw ───────────────────────────────
Write-Step "Configuring OpenClaw"

$openclawConfigDir = "$env:USERPROFILE\.openclaw"
if (-not (Test-Path $openclawConfigDir)) {
    New-Item -ItemType Directory -Force -Path $openclawConfigDir | Out-Null
}

$settingsSource = ".\openclaw-config\settings.json.example"
$settingsDest   = "$openclawConfigDir\settings.json"

if ((Test-Path $settingsSource) -and (-not (Test-Path $settingsDest))) {
    Copy-Item $settingsSource $settingsDest
    Write-Ok "OpenClaw settings.json created"
} elseif (Test-Path $settingsDest) {
    Write-Ok "OpenClaw settings.json already exists (not overwritten)"
} else {
    Write-Warn "No settings template found — OpenClaw will use defaults"
}

# ── Done ──────────────────────────────────────────────────────
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "  nuck001 Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env with your real credentials" -ForegroundColor White
Write-Host "  2. Place credentials.json (Google OAuth) in this folder" -ForegroundColor White
Write-Host "  3. Start the agent:" -ForegroundColor White
Write-Host "     openclaw" -ForegroundColor Yellow
Write-Host ""
Write-Host "Telegram bot will connect automatically once TELEGRAM_TOKEN is set." -ForegroundColor Gray

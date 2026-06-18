# Local test launcher for teams-morning-bot
# Usage: .\run_local.ps1

$ErrorActionPreference = "Stop"

chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

Write-Host ""
Write-Host "=== Teams Morning Bot - Local Test ===" -ForegroundColor Cyan
Write-Host ""

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "[ERROR] Python not found. Install Python 3.12+" -ForegroundColor Red
    Write-Host "Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Python: $(python --version)" -ForegroundColor Green

Write-Host "[..] Installing dependencies..." -ForegroundColor Gray
python -m pip install -r requirements.txt -q
Write-Host "[OK] Dependencies installed" -ForegroundColor Green

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[!] Created .env - please add TEAMS_WEBHOOK_URL" -ForegroundColor Yellow
}

Get-Content ".env" -Encoding UTF8 | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $val = $matches[2].Trim()
        if ($val) { [Environment]::SetEnvironmentVariable($key, $val, "Process") }
    }
}

$webhook = $env:TEAMS_WEBHOOK_URL

Write-Host ""
Write-Host "Choose test mode:" -ForegroundColor Cyan
Write-Host "  1) Preview (no send, recommended first)"
Write-Host "  2) Send one message (today)"
Write-Host "  3) Send batch of 5 messages"
Write-Host "  4) Validate only (full pipeline, no Teams send)"
Write-Host ""
$choice = Read-Host "Enter 1 / 2 / 3 / 4 (default 1)"
if (-not $choice) { $choice = "1" }

switch ($choice) {
    "1" {
        $env:DRY_RUN = "true"
        $env:SKIP_WORKDAY_CHECK = "true"
        Write-Host ""
        Write-Host ">>> Preview: 5 messages + image URLs (no Teams send)" -ForegroundColor Yellow
        python test_batch.py
    }
    "2" {
        if (-not $webhook) {
            Write-Host ""
            Write-Host "[ERROR] Set TEAMS_WEBHOOK_URL in .env first" -ForegroundColor Red
            Write-Host "Edit: notepad .env" -ForegroundColor Gray
            exit 1
        }
        $env:SKIP_WORKDAY_CHECK = "true"
        Write-Host ""
        Write-Host ">>> Sending one test message to Teams..." -ForegroundColor Green
        python main.py
    }
    "3" {
        if (-not $webhook) {
            Write-Host ""
            Write-Host "[ERROR] Set TEAMS_WEBHOOK_URL in .env first" -ForegroundColor Red
            Write-Host "Edit: notepad .env" -ForegroundColor Gray
            exit 1
        }
        $env:TEST_BATCH_COUNT = "5"
        $env:TEST_BATCH_DELAY = "3"
        Write-Host ""
        Write-Host ">>> Sending 5 test messages to Teams..." -ForegroundColor Green
        python test_batch.py
    }
    "4" {
        Write-Host ""
        Write-Host ">>> Validate only: message + news + image + payload (no Teams send)" -ForegroundColor Yellow
        python main.py --validate-only
    }
    default {
        Write-Host "[ERROR] Invalid option" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan

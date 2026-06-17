# Python install helper for teams-morning-bot
$ErrorActionPreference = "Continue"

chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Python 3.12 Install Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    Write-Host "[OK] Python already installed:" -ForegroundColor Green
    python --version
    Write-Host ""
    Write-Host "Next step: run .\preview.bat" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 0
}

$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) {
    Write-Host "[OK] Python launcher (py) found:" -ForegroundColor Green
    py --version
    Write-Host ""
    Write-Host "Next step: py test_batch.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 0
}

$winget = Get-Command winget -ErrorAction SilentlyContinue
if ($winget) {
    Write-Host "[..] Installing Python 3.12 via winget..." -ForegroundColor Yellow
    Write-Host "This may take a few minutes." -ForegroundColor Gray
    Write-Host ""
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Install complete!" -ForegroundColor Green
        Write-Host "Close this window, open a NEW PowerShell, then run:" -ForegroundColor Yellow
        Write-Host "  cd C:\Users\Angus\Projects\teams-morning-bot" -ForegroundColor White
        Write-Host "  .\preview.bat" -ForegroundColor White
        Read-Host "Press Enter to exit"
        exit 0
    }
}

Write-Host "[!] Auto install failed. Use manual install:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Open https://www.python.org/downloads/" -ForegroundColor White
Write-Host "  2. Download Python 3.12" -ForegroundColor White
Write-Host "  3. Run the installer" -ForegroundColor White
Write-Host "  4. CHECK 'Add python.exe to PATH'  <-- IMPORTANT" -ForegroundColor Red
Write-Host "  5. Click 'Install Now'" -ForegroundColor White
Write-Host ""
Start-Process "https://www.python.org/downloads/"
Read-Host "Press Enter to exit"

# Preview mode - option 1
$ErrorActionPreference = "Stop"

chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Set-Location $PSScriptRoot

Write-Host ""
Write-Host "=== Preview mode (will NOT send to Teams) ===" -ForegroundColor Yellow
Write-Host ""

python -m pip install -r requirements.txt -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] pip install failed. Is Python installed?" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$env:DRY_RUN = "true"
$env:SKIP_WORKDAY_CHECK = "true"
python test_batch.py

Write-Host ""
Read-Host "Press Enter to exit"

# 用 Shell 設定 Telegram（寫入 .env + 可選 GitHub Secret）
# 用法：在專案根目錄執行  .\scripts\set_telegram_env.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

$envFile = Join-Path $root ".env"
if (-not (Test-Path $envFile)) {
    Copy-Item (Join-Path $root ".env.example") $envFile
    Write-Host "[OK] 已從 .env.example 建立 .env" -ForegroundColor Green
}

Write-Host ""
Write-Host "Telegram 設定（Chat ID 預設 -1002236690168）" -ForegroundColor Cyan
Write-Host "請貼上 BotFather 給你的 TELEGRAM_BOT_TOKEN，然後 Enter：" -ForegroundColor Yellow
$token = Read-Host "TELEGRAM_BOT_TOKEN"
$token = $token.Trim()
if (-not $token) {
    Write-Host "[ERROR] Token 不可為空" -ForegroundColor Red
    exit 1
}
if ($token -notmatch ":") {
    Write-Host "[WARN] Token 通常格式為 123456789:AAH..." -ForegroundColor Yellow
}

$chatId = Read-Host "TELEGRAM_CHAT_ID [Enter=沿用 -1002236690168]"
if (-not $chatId.Trim()) {
    $chatId = "-1002236690168"
} else {
    $chatId = $chatId.Trim()
}

$lines = Get-Content $envFile -Encoding UTF8
$out = New-Object System.Collections.Generic.List[string]
$seenToken = $false
$seenChat = $false
$seenEnable = $false

foreach ($line in $lines) {
    if ($line -match '^\s*#?\s*TELEGRAM_BOT_TOKEN=') {
        $out.Add("TELEGRAM_BOT_TOKEN=$token")
        $seenToken = $true
        continue
    }
    if ($line -match '^\s*#?\s*TELEGRAM_CHAT_ID=') {
        $out.Add("TELEGRAM_CHAT_ID=$chatId")
        $seenChat = $true
        continue
    }
    if ($line -match '^\s*#?\s*ENABLE_TELEGRAM=') {
        $out.Add("ENABLE_TELEGRAM=true")
        $seenEnable = $true
        continue
    }
    $out.Add($line)
}

if (-not $seenToken) { $out.Add("TELEGRAM_BOT_TOKEN=$token") }
if (-not $seenChat) { $out.Add("TELEGRAM_CHAT_ID=$chatId") }
if (-not $seenEnable) { $out.Add("ENABLE_TELEGRAM=true") }

$out | Set-Content $envFile -Encoding UTF8
Write-Host "[OK] 已寫入 .env（Token 不會顯示在畫面上）" -ForegroundColor Green

Write-Host ""
Write-Host "驗證 Token..." -ForegroundColor Cyan
python (Join-Path $PSScriptRoot "verify_telegram.py")

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] 驗證失敗，請檢查 Token 或 Bot 是否已加入群組" -ForegroundColor Red
    exit 1
}

$gh = Get-Command gh -ErrorAction SilentlyContinue
if ($gh) {
    Write-Host ""
    $sync = Read-Host "是否同步到 GitHub Secret? (y/N)"
    if ($sync -eq 'y' -or $sync -eq 'Y') {
        $token | gh secret set TELEGRAM_BOT_TOKEN -R gotodye/teams-morning-bot
        gh variable set TELEGRAM_CHAT_ID --body $chatId -R gotodye/teams-morning-bot
        Write-Host "[OK] GitHub TELEGRAM_BOT_TOKEN (secret) + TELEGRAM_CHAT_ID (variable)" -ForegroundColor Green
    }
} else {
    Write-Host "[INFO] 未安裝 gh CLI，略過 GitHub 同步" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "完成。測試發送：" -ForegroundColor Cyan
Write-Host '  $env:SKIP_WORKDAY_CHECK="true"; python main.py' -ForegroundColor White

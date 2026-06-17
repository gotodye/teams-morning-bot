# One-click deploy to GitHub Actions
# Usage: .\deploy.ps1

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Teams Morning Bot - Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check gh CLI
$gh = Get-Command gh -ErrorAction SilentlyContinue
if (-not $gh) {
    Write-Host "[ERROR] GitHub CLI (gh) not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Install:" -ForegroundColor Yellow
    Write-Host "  winget install GitHub.cli" -ForegroundColor White
    Write-Host "  gh auth login" -ForegroundColor White
    Write-Host ""
    Write-Host "Or deploy manually:" -ForegroundColor Yellow
    Write-Host "  1. Create repo on https://github.com/new" -ForegroundColor White
    Write-Host "  2. git init && git add . && git commit -m 'Initial commit'" -ForegroundColor White
    Write-Host "  3. git remote add origin <your-repo-url>" -ForegroundColor White
    Write-Host "  4. git push -u origin main" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

# 2. Check gh auth
gh auth status 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Not logged in to GitHub. Running: gh auth login" -ForegroundColor Yellow
    gh auth login
}

# 3. Init git if needed
if (-not (Test-Path ".git")) {
    git init
    git branch -M main
}

# 4. Commit
git add -A
$status = git status --porcelain
if ($status) {
    git commit -m "Deploy Teams morning bot with scheduled delivery"
    Write-Host "[OK] Changes committed" -ForegroundColor Green
} else {
    Write-Host "[OK] No new changes to commit" -ForegroundColor Green
}

# 5. Create repo and push
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    Write-Host ""
    Write-Host "Creating GitHub repository..." -ForegroundColor Yellow
    gh repo create teams-morning-bot --public --source=. --remote=origin --push
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create repo. It may already exist." -ForegroundColor Red
        Write-Host "Try: gh repo create teams-morning-bot --public --source=. --remote=origin --push" -ForegroundColor Gray
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[OK] Remote: $remote" -ForegroundColor Green
    git push -u origin main
}

# 6. Set webhook secret
Write-Host ""
$webhook = $env:TEAMS_WEBHOOK_URL
if (-not $webhook) {
    if (Test-Path ".env") {
        Get-Content ".env" -Encoding UTF8 | ForEach-Object {
            if ($_ -match '^\s*TEAMS_WEBHOOK_URL=(.+)$') {
                $webhook = $matches[1].Trim()
            }
        }
    }
}

if (-not $webhook) {
    Write-Host "[!] TEAMS_WEBHOOK_URL not set." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Get your webhook URL:" -ForegroundColor Cyan
    Write-Host "  Teams channel -> ... -> Workflows -> webhook template" -ForegroundColor White
    Write-Host ""
    $webhook = Read-Host "Paste your Teams Webhook URL here"
}

if ($webhook) {
    gh secret set TEAMS_WEBHOOK_URL --body $webhook
    Write-Host "[OK] TEAMS_WEBHOOK_URL secret saved" -ForegroundColor Green
} else {
    Write-Host "[!] Skipped secret. Set manually:" -ForegroundColor Yellow
    Write-Host "  gh secret set TEAMS_WEBHOOK_URL" -ForegroundColor White
}

# 7. Optional OpenAI key
$setAi = Read-Host "Set OPENAI_API_KEY for AI messages? (y/N)"
if ($setAi -eq "y") {
    $aiKey = Read-Host "Paste OpenAI API Key"
    if ($aiKey) { gh secret set OPENAI_API_KEY --body $aiKey }
}

# 8. Trigger test run
Write-Host ""
$testRun = Read-Host "Trigger a test run now? (Y/n)"
if ($testRun -ne "n") {
    gh workflow run teams_bot.yml
    Write-Host "[OK] Workflow triggered! Check: gh run list" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deploy complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Schedule: Mon-Fri 08:00 Taiwan time" -ForegroundColor Cyan
Write-Host "Dashboard: https://github.com/$(gh api user -q .login)/teams-morning-bot/actions" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"

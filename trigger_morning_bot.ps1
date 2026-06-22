# Trigger Teams Morning Bot on GitHub (same API call as Power Automate schedule)
$ErrorActionPreference = "Stop"

$repo = "gotodye/teams-morning-bot"
$workflow = "teams_bot.yml"

Write-Host ""
Write-Host "=== Trigger Teams Morning Bot (workflow_dispatch) ===" -ForegroundColor Cyan
Write-Host ""

if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh auth status 2>&1 | Out-Host
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Run: gh auth login" -ForegroundColor Yellow
        exit 1
    }
    gh workflow run $workflow --repo $repo
    if ($LASTEXITCODE -ne 0) { exit 1 }
    Write-Host ""
    Write-Host "[OK] Workflow triggered." -ForegroundColor Green
    Start-Sleep -Seconds 5
    gh run list --workflow=$workflow --repo $repo --limit 1
    Write-Host ""
    Write-Host "https://github.com/$repo/actions/workflows/$workflow"
    exit 0
}

# Fallback: GitHub REST API with GITHUB_TOKEN env var
$token = $env:GITHUB_TOKEN
if (-not $token) {
    Write-Host "[ERROR] Install gh and run 'gh auth login', or set GITHUB_TOKEN." -ForegroundColor Red
    exit 1
}

$uri = "https://api.github.com/repos/$repo/actions/workflows/$workflow/dispatches"
$headers = @{
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    Authorization = "Bearer $token"
}
$body = '{"ref":"main"}'

Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $body -ContentType "application/json"
Write-Host "[OK] Workflow triggered via REST API." -ForegroundColor Green

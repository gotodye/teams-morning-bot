@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Teams Morning Bot - Auto Deploy
echo ========================================
echo.

where gh >nul 2>&1
if errorlevel 1 (
    echo [ERROR] GitHub CLI not found. Installing...
    winget install GitHub.cli --accept-package-agreements --accept-source-agreements
)

echo [1/6] Checking GitHub login...
gh auth status
if errorlevel 1 (
    echo.
    echo Please login - browser will open:
    gh auth login -w -p https
)

echo.
echo [2/6] Initializing git...
if not exist ".git" (
    git init
    git branch -M main
)

echo.
echo [3/6] Committing files...
git add -A
git diff --cached --name-only | findstr /i "\.env" >nul
if not errorlevel 1 (
    echo [ERROR] .env should not be committed!
    git reset HEAD .env
)
git commit -m "Deploy Teams morning bot with 8AM schedule" 2>nul
if errorlevel 1 echo [OK] Nothing new to commit

echo.
echo [4/6] Creating GitHub repo and pushing...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    gh repo create teams-morning-bot --public --source=. --remote=origin --push
) else (
    git push -u origin main
)

echo.
echo [5/6] Setting Webhook secret...
set /p WEBHOOK="Paste Teams Webhook URL: "
if not "%WEBHOOK%"=="" (
    echo %WEBHOOK%| gh secret set TEAMS_WEBHOOK_URL
    echo [OK] Secret saved
) else (
    echo [!] Skipped - set later with: gh secret set TEAMS_WEBHOOK_URL
)

echo.
echo [6/6] Triggering test run...
gh workflow run teams_bot.yml
echo.
echo ========================================
echo   Deploy complete!
echo ========================================
gh repo view --json url -q .url
echo.
echo Schedule: Mon-Fri 08:00 Taiwan time
echo Check Actions tab for test run status.
echo.
pause

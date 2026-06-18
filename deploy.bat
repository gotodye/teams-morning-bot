@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Teams Morning Bot - Auto Deploy
echo ========================================
echo.

REM --- Install GitHub CLI if missing ---
where gh >nul 2>&1
if errorlevel 1 (
    echo [!] GitHub CLI not found. Installing via winget...
    winget install GitHub.cli --accept-package-agreements --accept-source-agreements
    echo.
    echo [IMPORTANT] Close this window, open a NEW PowerShell, then run deploy.bat again.
    echo Or run:  refreshenv   then   gh auth login
    pause
    exit /b 0
)

echo [1/7] Checking GitHub login...
gh auth status
if errorlevel 1 (
    echo.
    echo Please login in browser:
    gh auth login -w -p https
)

echo.
echo [2/7] Git commit...
if not exist ".git" (
    git init
    git branch -M main
)
git add -A
git reset HEAD .env 2>nul
git commit -m "Deploy Teams morning bot with 8AM schedule" 2>nul

echo.
echo [3/7] Push to GitHub...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    gh repo create teams-morning-bot --public --source=. --remote=origin --push
    if errorlevel 1 (
        echo.
        echo [ERROR] Could not create repo. It may already exist.
        echo Manual fix:
        echo   1. Go to https://github.com/new  create repo "teams-morning-bot"
        echo   2. git remote add origin https://github.com/YOUR_USER/teams-morning-bot.git
        echo   3. git push -u origin main
        pause
        exit /b 1
    )
) else (
    git push -u origin main
)

echo.
echo [4/7] Teams Webhook URL
echo Get it from: Teams channel -^> ... -^> Workflows -^> webhook template
echo.
set /p WEBHOOK="Paste Teams Webhook URL (or press Enter to skip): "
if not "%WEBHOOK%"=="" (
    echo %WEBHOOK%| gh secret set TEAMS_WEBHOOK_URL
    echo [OK] TEAMS_WEBHOOK_URL saved
) else (
    echo [!] Skipped. Set later at GitHub repo Settings -^> Secrets -^> Actions
)

echo.
echo [5/7] Trigger test run...
gh workflow run teams_bot.yml
if errorlevel 1 echo [!] Could not trigger - enable Actions in repo Settings

echo.
echo [6/7] Repo URL:
gh repo view --json url -q .url 2>nul

echo.
echo ========================================
echo   Done! Schedule: Mon-Fri 08:00 Taiwan
echo ========================================
pause

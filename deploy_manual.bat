@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Manual Deploy (no gh required)
echo ========================================
echo.

REM --- Git push ---
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Step 1: Create repo on GitHub first
    echo   https://github.com/new
    echo   Name: teams-morning-bot
    echo   Public, NO README
    echo.
    set /p GITHUB_USER=Enter your GitHub username: 
    if "%GITHUB_USER%"=="" (
        echo [ERROR] Username cannot be empty.
        pause
        exit /b 1
    )
    git remote add origin https://github.com/%GITHUB_USER%/teams-morning-bot.git
)

echo.
echo Step 2: Pushing code to GitHub...
git push -u origin main
if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Common fixes:
    echo   - Create the repo at https://github.com/new first
    echo   - Check username in remote URL: git remote -v
    pause
    exit /b 1
)

echo.
echo [OK] Code pushed!
echo.
echo ========================================
echo   Step 3: Set Webhook Secret (browser)
echo ========================================
echo.
echo 1. Open your repo on GitHub
echo 2. Settings -^> Secrets and variables -^> Actions
echo 3. New repository secret
echo    Name:  TEAMS_WEBHOOK_URL
echo    Value: your Teams Webhook URL
echo.
echo 4. Go to Actions tab -^> Teams Morning Bot -^> Run workflow
echo.
set /p GITHUB_USER2=Your GitHub username (to open browser): 
start https://github.com/%GITHUB_USER2%/teams-morning-bot/settings/secrets/actions/new
timeout /t 2 >nul
start https://github.com/%GITHUB_USER2%/teams-morning-bot/actions/workflows/teams_bot.yml

echo.
echo Schedule: Mon-Fri 08:00 Taiwan time
echo.
pause

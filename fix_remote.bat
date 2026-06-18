@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo Fix GitHub remote URL
echo.
echo Current remote:
git remote -v
echo.

set /p GITHUB_USER=Enter your GitHub username: 
if "%GITHUB_USER%"=="" (
    echo [ERROR] Username required.
    pause
    exit /b 1
)

git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/teams-morning-bot.git

echo.
echo New remote:
git remote -v
echo.
echo Pushing...
git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed.
    echo Make sure repo exists: https://github.com/new
    echo Name: teams-morning-bot  Public  no README
    pause
    exit /b 1
)

echo.
echo [OK] Push successful!
echo Next: set TEAMS_WEBHOOK_URL secret on GitHub
start https://github.com/%GITHUB_USER%/teams-morning-bot/settings/secrets/actions/new
pause

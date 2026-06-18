@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo [1/4] Git status...
git status -sb
echo.

echo [2/4] Stage files...
git add news.py main.py .github/workflows/teams_bot.yml .env.example
echo.

echo [3/4] Commit...
git commit -m "Add major breaking news appendix for TW/HK/VN/ID"
if errorlevel 1 (
    echo No new changes to commit, or commit failed.
)
echo.

echo [4/4] Push to GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo Push failed. Try: gh auth login
    pause
    exit /b 1
)

echo.
echo [OK] Pushed to https://github.com/gotodye/teams-morning-bot
git log -1 --oneline
pause

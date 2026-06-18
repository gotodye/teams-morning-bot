@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Fixing remote for gotodye/teams-morning-bot...
git remote remove origin 2>nul
git remote add origin https://github.com/gotodye/teams-morning-bot.git
git remote -v
echo.
echo Pushing code...
git push -u origin main
if errorlevel 1 (
    echo.
    echo If auth failed, run: gh auth login
    echo Or use GitHub Desktop / credential manager
    pause
    exit /b 1
)
echo.
echo [OK] Code pushed to https://github.com/gotodye/teams-morning-bot
pause

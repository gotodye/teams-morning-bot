@echo off
chcp 65001 >nul
cd /d "%~dp0"

git add .github/workflows/teams_bot.yml
git commit -m "Add manual workflow inputs to test Gemini AI messages"
git push origin main
if errorlevel 1 (
    echo Push failed.
    pause
    exit /b 1
)

echo.
echo [OK] Pushed. Next:
echo 1. Open https://github.com/gotodye/teams-morning-bot/actions
echo 2. Teams Morning Bot -^> Run workflow
echo 3. force_message_type = ai
echo 4. skip_workday_check = true
echo 5. Run workflow
pause

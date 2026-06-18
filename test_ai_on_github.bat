@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo === GitHub AI 金句測試 ===
echo.

echo [1/5] Git status...
git status -sb
echo.

echo [2/5] Stage workflow files...
git add .github\workflows\ai_test.yml .github\workflows\teams_bot.yml
echo.

echo [3/5] Commit...
git commit -m "Add GitHub Actions workflow to test AI morning messages"
if errorlevel 1 (
    echo No new changes to commit, or commit failed.
)
echo.

echo [4/5] Push to GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Check git credentials.
    pause
    exit /b 1
)
echo [OK] Pushed.
git log -1 --oneline
echo.

echo [5/5] Trigger AI test workflow...
where gh >nul 2>&1
if errorlevel 1 goto manual

gh auth status >nul 2>&1
if errorlevel 1 goto manual

gh workflow run ai_test.yml --repo gotodye/teams-morning-bot
if errorlevel 1 goto manual

echo [OK] Workflow triggered.
timeout /t 8 /nobreak >nul
gh run list --workflow=ai_test.yml --repo gotodye/teams-morning-bot --limit 1
echo.
echo Watch run: https://github.com/gotodye/teams-morning-bot/actions/workflows/ai_test.yml
echo Teams should show title with "AI Crafted" when done.
pause
exit /b 0

:manual
echo.
echo gh CLI not available. Open Actions and click Run workflow manually:
echo https://github.com/gotodye/teams-morning-bot/actions/workflows/ai_test.yml
start https://github.com/gotodye/teams-morning-bot/actions/workflows/ai_test.yml
pause

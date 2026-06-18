@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo === Sync and push Gemini truncation fix ===
echo.

git status -sb
echo.

echo [1/4] Fetching latest from GitHub...
git fetch origin
if errorlevel 1 (
    echo Fetch failed.
    pause
    exit /b 1
)

echo.
echo [2/4] Rebasing local commits onto origin/main...
git pull --rebase origin main
if errorlevel 1 (
    echo.
    echo Rebase failed. If you see conflicts, fix them then run:
    echo   git rebase --continue
    echo   git push origin main
    pause
    exit /b 1
)

echo.
echo [3/4] Committing main.py if needed...
git add main.py
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "fix Gemini 3.x truncated AI greetings by increasing maxOutputTokens and setting minimal thinking level"
    if errorlevel 1 (
        echo Commit failed.
        pause
        exit /b 1
    )
) else (
    echo No new changes to commit.
)

echo.
echo [4/4] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo Push failed.
    pause
    exit /b 1
)

echo.
echo [OK] Pushed to GitHub.
git log -3 --oneline
echo.
pause

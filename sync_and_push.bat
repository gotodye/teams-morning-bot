@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo === Sync local repo and push to GitHub ===
echo.

git status -sb
echo.

echo [1/5] Stashing uncommitted changes...
git stash push -u -m "auto-stash before sync"
if errorlevel 1 (
    echo Stash failed or nothing to stash - continuing...
)

echo.
echo [2/5] Fetching latest from GitHub...
git fetch origin
if errorlevel 1 (
    echo Fetch failed.
    goto cleanup
)

echo.
echo [3/5] Rebasing onto origin/main...
git pull --rebase origin main
if errorlevel 1 (
    echo.
    echo Rebase failed. Run: git status
    echo If conflicts: fix files, then: git add . ^&^& git rebase --continue
    goto cleanup
)

echo.
echo [4/5] Restoring stashed changes...
git stash pop
if errorlevel 1 (
    echo Stash pop had conflicts - resolve manually, then push.
    goto cleanup
)

echo.
echo [5/5] Committing remaining changes and pushing...
git add -A
git reset HEAD .env 2>nul
git diff --cached --quiet
if not errorlevel 1 (
    echo No extra changes to commit.
) else (
    git commit -m "Add local helper scripts and HR newsletter updates"
    if errorlevel 1 (
        echo Commit failed.
        goto cleanup
    )
)

git push origin main
if errorlevel 1 (
    echo Push failed.
    goto cleanup
)

echo.
echo [OK] Synced and pushed to GitHub.
git log -3 --oneline
goto end

:cleanup
echo.
echo Stash list:
git stash list
pause
exit /b 1

:end
echo.
pause

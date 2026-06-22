@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo ========================================
echo   teams-morning-bot — 移除 HR 模組並推送
echo ========================================
echo.

git add -A
git status

echo.
set /p CONFIRM=Commit and push split changes? (y/n):
if /i not "%CONFIRM%"=="y" exit /b 0

git commit -m "Split HR newsletter into separate teams-hr-newsletter repo"
git push origin main

echo Done.
pause

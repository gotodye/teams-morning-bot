@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo   Python 3.12 Installer Helper
echo ========================================
echo.

where python >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Python already installed:
    python --version
    echo.
    echo You can run preview.bat to test the bot.
    pause
    exit /b 0
)

where py >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Python launcher found:
    py --version
    echo.
    echo You can run: py test_batch.py
    pause
    exit /b 0
)

echo Python not found. Trying winget install...
echo.

where winget >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] winget not available.
    echo.
    echo Please install manually:
    echo   1. Open https://www.python.org/downloads/
    echo   2. Download Python 3.12
    echo   3. Run installer
    echo   4. CHECK "Add python.exe to PATH"
    echo   5. Click "Install Now"
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing Python 3.12 via winget...
echo This may take a few minutes.
echo.

winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] winget install failed.
    echo Opening Python download page...
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [OK] Install finished. Close this window, open a NEW PowerShell, then run:
echo   cd C:\Users\Angus\Projects\teams-morning-bot
echo   preview.bat
echo.
pause

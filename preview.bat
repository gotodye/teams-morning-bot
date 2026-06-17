@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo === Preview mode (no Teams send) ===
echo.

python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)

set DRY_RUN=true
set SKIP_WORKDAY_CHECK=true
set PYTHONIOENCODING=utf-8
python test_batch.py

echo.
pause

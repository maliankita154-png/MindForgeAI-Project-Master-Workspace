@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "AETHERA_PYTHON=.venv\Scripts\python.exe"
) else (
    set "AETHERA_PYTHON=python"
)

%AETHERA_PYTHON% -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Flask is not installed for the selected Python environment.
    echo Run this once in PowerShell from this folder:
    echo   python -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo Starting Aethera at http://127.0.0.1:8000
echo Keep this window open while using the website.
echo Press Ctrl+C here to stop the local server.
echo.
%AETHERA_PYTHON% src\app.py

endlocal



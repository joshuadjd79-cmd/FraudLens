@echo off
title FraudLens Backend Server (FastAPI + Oracle 26ai)
color 0B
cd /d "%~dp0"

echo ===============================================================================
echo                FRAUDLENS FINANCIAL FRAUD MONITORING PLATFORM
echo                           Backend Server Launcher
echo ===============================================================================
echo.

:: 1. Check Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.10+ from python.org and add it to your System PATH.
    echo.
    pause
    exit /b 1
)

:: 2. Display Python version
echo [CHECK] Python Environment:
python --version
echo.

:: 3. Check for dependencies
python -c "import fastapi, oracledb, uvicorn, pydantic" >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing required Python dependencies...
    pip install -r app\backend\requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Dependency installation failed!
        pause
        exit /b 1
    )
)

:: 4. Check if port 8000 is already in use
for /f "tokens=5" %%a in ('netstat -aon ^| findstr 127.0.0.1:8000 ^| findstr LISTENING 2^>nul') do set OCCUPIED_PID=%%a

if not defined OCCUPIED_PID goto :BACKEND_READY

echo.
echo ===============================================================================
echo [NOTICE] Port 8000 is ALREADY active [PID: %OCCUPIED_PID%]
echo The FraudLens Backend server is ALREADY RUNNING in the background.
echo Diagnostic URL: http://127.0.0.1:8000/api/health
echo ===============================================================================
echo.
set /p RESTART_CHOICE="Do you want to terminate the existing backend and restart fresh? [Y/N, default=N]: "
if /i "%RESTART_CHOICE%"=="Y" (
    echo Terminating process %OCCUPIED_PID%...
    taskkill /F /PID %OCCUPIED_PID% >nul 2>nul
    timeout /t 1 /nobreak >nul
    goto :BACKEND_READY
)
echo.
echo Keeping the existing backend server running. You can close this window.
pause
exit /b 0

:BACKEND_READY

echo [START] Launching FastAPI Uvicorn Server on http://127.0.0.1:8000 ...
echo [DOCS]  Interactive OpenAPI Docs: http://127.0.0.1:8000/docs
echo [HEALTH] Diagnostic Health Check: http://127.0.0.1:8000/api/health
echo.
echo Press Ctrl+C to stop the backend server.
echo ===============================================================================
echo.

python -m uvicorn app.backend.main:app --host 127.0.0.1 --port 8000

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Backend process terminated with error code %errorlevel%.
    pause
)

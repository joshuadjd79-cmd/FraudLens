@echo off
title FraudLens Frontend Console (Vite + React)
color 0A
cd /d "%~dp0"

echo ===============================================================================
echo                FRAUDLENS FINANCIAL FRAUD MONITORING PLATFORM
echo                          Frontend Console Launcher
echo ===============================================================================
echo.

:: 1. Check Node.js installation
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not found in PATH!
    echo Please install Node.js v18+ from https://nodejs.org and ensure it is in PATH.
    echo.
    pause
    exit /b 1
)

:: 2. Display Node version
echo [CHECK] Node Environment:
node --version
npm --version
echo.

:: 3. Check node_modules in app/frontend
if not exist "app\frontend\node_modules\" (
    echo [INFO] Installing frontend node dependencies...
    cd app\frontend
    call npm install
    cd ..\..
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed!
        pause
        exit /b 1
    )
)

:: 4. Check if port 5173 is already in use
for /f "tokens=5" %%a in ('netstat -aon ^| findstr 127.0.0.1:5173 ^| findstr LISTENING 2^>nul') do set OCCUPIED_FRONTEND_PID=%%a

if not defined OCCUPIED_FRONTEND_PID goto :FRONTEND_READY

echo.
echo ===============================================================================
echo [NOTICE] Port 5173 is ALREADY active [PID: %OCCUPIED_FRONTEND_PID%]
echo The FraudLens Frontend Vite server is ALREADY RUNNING in the background.
echo Application URL: http://localhost:5173
echo ===============================================================================
echo.
set /p RESTART_CHOICE="Do you want to terminate the existing frontend and restart fresh? [Y/N, default=N]: "
if /i "%RESTART_CHOICE%"=="Y" (
    echo Terminating process %OCCUPIED_FRONTEND_PID%...
    taskkill /F /PID %OCCUPIED_FRONTEND_PID% >nul 2>nul
    timeout /t 1 /nobreak >nul
    goto :FRONTEND_READY
)
echo.
echo Keeping the existing frontend server running. You can close this window.
pause
exit /b 0

:FRONTEND_READY

echo [START] Starting Vite Development Server on http://localhost:5173 ...
echo.
echo Press Ctrl+C to stop the frontend server.
echo ===============================================================================
echo.

cd app\frontend
npm run dev

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Frontend process terminated with error code %errorlevel%.
    pause
)

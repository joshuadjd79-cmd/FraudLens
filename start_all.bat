@echo off
title FraudLens Unified Full-Stack Launcher
color 0F
cd /d "%~dp0"

echo ===============================================================================
echo                FRAUDLENS FINANCIAL FRAUD MONITORING PLATFORM
echo                     Complete Full-Stack Application Launcher
echo ===============================================================================
echo.
echo Launching FraudLens Full-Stack Application...
echo.
echo 1. Launching FastAPI Backend on http://127.0.0.1:8000
start "FraudLens Backend Server" cmd /k "start_backend.bat"

echo 2. Waiting 3 seconds for backend initialization...
timeout /t 3 /nobreak >nul

echo 3. Launching Vite React Frontend on http://localhost:5173
start "FraudLens Frontend Console" cmd /k "start_frontend.bat"

echo.
echo ===============================================================================
echo [SUCCESS] Both backend and frontend servers have been initiated!
echo.
echo  - Web Application:       http://localhost:5173
echo  - Backend API:           http://127.0.0.1:8000
echo  - OpenAPI Documentation: http://127.0.0.1:8000/docs
echo  - Oracle DB Status:      http://127.0.0.1:8000/api/health
echo.
echo Keep the opened command windows running while using the application.
echo ===============================================================================
echo.
pause

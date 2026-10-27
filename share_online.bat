@echo off
title FraudLens Cloudflare Public Share Link
color 0B
cd /d "%~dp0"

echo ===============================================================================
echo                FRAUDLENS FINANCIAL FRAUD MONITORING PLATFORM
echo                     Public Mobile-Friendly Share Link
echo ===============================================================================
echo.
echo Launching Cloudflare Tunnel (Zero Passwords, Mobile Optimized)...
echo.
echo Your public HTTPS link will appear below:
echo ===============================================================================
echo.

.\cloudflared.exe tunnel --protocol http2 --url http://localhost:5173
pause

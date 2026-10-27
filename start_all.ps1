# FraudLens Unified PowerShell Launcher
Set-Location -Path $PSScriptRoot

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "                FRAUDLENS FINANCIAL FRAUD MONITORING PLATFORM" -ForegroundColor Cyan
Write-Host "                     Complete Full-Stack Application Launcher" -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Launching FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Green
Start-Process cmd.exe -ArgumentList '/k "start_backend.bat"'

Write-Host "2. Waiting 3 seconds for backend initialization..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "3. Launching Vite React Frontend on http://localhost:5173 ..." -ForegroundColor Green
Start-Process cmd.exe -ArgumentList '/k "start_frontend.bat"'

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "[SUCCESS] Both backend and frontend servers have been initiated!" -ForegroundColor Green
Write-Host ""
Write-Host "  - Web Application:       http://localhost:5173" -ForegroundColor White
Write-Host "  - Backend API:           http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  - OpenAPI Documentation: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "  - Oracle DB Status:      http://127.0.0.1:8000/api/health" -ForegroundColor White
Write-Host ""
Write-Host "Keep the opened terminal windows running while using the application." -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan

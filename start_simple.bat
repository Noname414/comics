@echo off
title Comic Generator Service Launcher
cd /d "c:\Users\sheng\copilot-projects\comics"

echo.
echo ====================================
echo   Comic Generator Service Launcher
echo ====================================
echo.

echo Starting API Server...
start "API Server" cmd /k "python comic_api_server.py"

echo Starting Web Server...
start "Web Server" /D "docs" cmd /k "python -m http.server 8000"

echo.
echo Services started!
echo.
echo Web: http://localhost:8000
echo API: http://localhost:5000
echo.
echo Keep both windows open!
echo.

timeout /t 5 /nobreak >nul
start http://localhost:8000

echo Browser opened. Press any key to exit.
pause >nul

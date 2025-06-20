@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

title Comic Generator Service (UTF-8)
cd /d "c:\Users\sheng\copilot-projects\comics"

echo.
echo ====================================
echo   Comic Generator Service (UTF-8)
echo ====================================
echo.

echo Starting API Server with UTF-8 encoding...
start "API Server (UTF-8)" cmd /k "chcp 65001 >nul & set PYTHONIOENCODING=utf-8 & python comic_api_server.py"

echo Starting Web Server...
start "Web Server" /D "docs" cmd /k "chcp 65001 >nul & python -m http.server 8000"

echo.
echo Services started with UTF-8 encoding!
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

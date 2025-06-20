@echo off
chcp 65001 >nul
echo Starting Comic Generator Service...
echo.

echo [1/3] Checking environment...
cd /d "c:\Users\sheng\copilot-projects\comics"

echo [2/3] Starting API Server...
start "Comic API Server" /D "c:\Users\sheng\copilot-projects\comics" cmd /k "python comic_api_server.py"

echo [3/3] Starting Web Server...
start "Web Server" /D "c:\Users\sheng\copilot-projects\comics\docs" cmd /k "python -m http.server 8000"

echo.
echo Service started successfully!
echo.
echo Web URL: http://localhost:8000
echo API URL: http://localhost:5000
echo Test Page: http://localhost:8000/test.html
echo.
echo Tips:
echo - Wait 10-15 seconds for services to fully start
echo - Keep both black windows open for proper operation
echo - Test the generation function on the web page
echo.
pause

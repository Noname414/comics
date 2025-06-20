@echo off
echo 正在檢查服務狀態...
echo.

echo [檢查 API 服務器]
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel%==0 (
    echo ✅ API 服務器運行正常 (http://localhost:5000)
) else (
    echo ❌ API 服務器未啟動
)

echo.
echo [檢查網頁服務器]
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel%==0 (
    echo ✅ 網頁服務器運行正常 (http://localhost:8000)
) else (
    echo ❌ 網頁服務器未啟動
)

echo.
echo [開啟測試頁面]
start http://localhost:8000/test.html

echo.
pause

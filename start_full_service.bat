@echo off
chcp 65001 >nul
echo ====================================
echo 🚀 四格漫畫完整服務啟動
echo ====================================
echo.

echo 📡 啟動 API 服務器 (Flask)...
echo 🌐 啟動網頁服務器 (HTTP Server)...
echo.
echo ⚠️  請勿關閉此視窗
echo 💡 在瀏覽器中訪問: http://localhost:8000
echo 🔧 API 服務地址: http://localhost:5000
echo.

cd /d "%~dp0"

rem 啟動 API 服務器 (背景執行)
start "API Server" cmd /c "python comic_api_server.py & pause"

rem 等待 API 服務器啟動
timeout /t 3 /nobreak >nul

rem 啟動網頁服務器並自動開啟瀏覽器
cd docs
echo 🔗 正在開啟瀏覽器...
start http://localhost:8000

echo 🚀 啟動網頁服務器...
python -m http.server 8000

@echo off
chcp 65001 >nul
echo ====================================
echo 四格漫畫本地測試伺服器
echo ====================================
echo.

cd /d "%~dp0docs"

echo 正在啟動本地伺服器...
echo 伺服器位址: http://localhost:8000
echo.
echo 按 Ctrl+C 可停止伺服器
echo.

echo 正在開啟瀏覽器...
start http://localhost:8000

echo 啟動 HTTP 伺服器中...
python -m http.server 8000

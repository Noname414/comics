@echo off
chcp 65001 >nul
echo ====================================
echo 🧹 四格漫畫互動式清理工具
echo ====================================
echo.
echo 📝 這個工具會逐一詢問您是否要刪除沒有圖片的漫畫資料夾
echo.

cd /d "%~dp0"

python cleanup_comics.py

echo.
pause

@echo off
chcp 65001 >nul
echo ====================================
echo 🧹 四格漫畫自動清理工具
echo ====================================
echo.

cd /d "%~dp0"

echo 📋 正在掃描沒有圖片的漫畫資料夾...
echo.

python cleanup_comics.py auto

echo.
echo ✅ 清理完成！
echo.
pause

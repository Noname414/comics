@echo off
chcp 65001 >nul
echo ====================================
echo 🔄 更新本地漫畫清單
echo ====================================
echo.

echo 正在掃描漫畫資料夾...
python generate_manifest.py

echo.
echo ✅ 漫畫清單已更新！
echo 您可以刷新網頁查看最新的漫畫作品。
echo.

pause

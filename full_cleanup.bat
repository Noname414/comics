@echo off
chcp 65001 >nul
echo ====================================
echo 🧹 四格漫畫完整清理與更新工具
echo ====================================
echo.

cd /d "%~dp0"

echo 📋 步驟 1: 自動清理沒有圖片的漫畫資料夾...
python cleanup_comics.py auto

echo.
echo 📋 步驟 2: 重新生成漫畫清單...
python -c "import generate_manifest; generate_manifest.generate_comics_manifest()"

echo.
echo 📋 步驟 3: 檢查 Git 狀態...
git status

echo.
echo ✅ 完整清理流程完成！
echo 💡 您可以執行以下命令來提交變更：
echo    git add .
echo    git commit -m "清理沒有圖片的漫畫資料夾"
echo    git push
echo.
pause

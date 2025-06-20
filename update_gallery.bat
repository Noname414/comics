@echo off
chcp 65001 >nul
echo 正在更新漫畫清單...
python generate_manifest.py
echo.
echo 漫畫清單更新完成！
echo 您現在可以：
echo 1. 本地預覽：cd docs ^&^& python -m http.server 8000
echo 2. 提交到 GitHub 來更新 GitHub Pages
pause

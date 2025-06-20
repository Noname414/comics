@echo off
chcp 65001 >nul
echo ====================================
echo 🎯 四格漫畫生成器測試
echo ====================================
echo.

cd /d "%~dp0"

echo 檢查 Google API 金鑰...
if "%GOOGLE_API_KEY%"=="" (
    echo ❌ 錯誤：未設定 GOOGLE_API_KEY 環境變數
    echo.
    echo 請先設定您的 Google API 金鑰：
    echo set GOOGLE_API_KEY=你的_Google_API_金鑰
    echo.
    pause
    exit /b 1
) else (
    echo ✅ API 金鑰已設定
)

echo.
echo 🚀 啟動漫畫生成器...
echo 建議測試關鍵字：AI新聞、科技趨勢、台積電
echo.

python comic_generator.py

echo.
echo 📋 生成完成後，執行以下步驟查看結果：
echo 1. 雙擊執行 update_local_comics.bat
echo 2. 在瀏覽器中刷新 localhost:8000
echo.
pause

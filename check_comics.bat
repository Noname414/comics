@echo off
chcp 65001 >nul
echo ====================================
echo 📊 四格漫畫統計與檢查工具
echo ====================================
echo.

cd /d "%~dp0"

echo 📋 漫畫資料夾統計:
echo.

setlocal enabledelayedexpansion
set /a total_folders=0
set /a folders_with_images=0
set /a folders_without_images=0

echo 🔍 掃描中...
for /d %%D in (docs\comic_output_*) do (
    set /a total_folders+=1
    if exist "%%D\four_panel_comic.png" (
        set /a folders_with_images+=1
        echo ✅ %%~nxD
    ) else (
        set /a folders_without_images+=1
        echo ❌ %%~nxD ^(沒有圖片^)
    )
)

echo.
echo 📊 統計結果:
echo    📁 總資料夾數: !total_folders!
echo    🖼️  有圖片的: !folders_with_images!
echo    ❌ 沒圖片的: !folders_without_images!
echo.

if !folders_without_images! gtr 0 (
    echo ⚠️  發現 !folders_without_images! 個沒有圖片的資料夾
    echo 💡 您可以執行 auto_cleanup.bat 來自動清理
) else (
    echo ✅ 所有漫畫資料夾都有完整圖片！
)

echo.
pause

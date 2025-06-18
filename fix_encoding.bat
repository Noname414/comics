@echo off
rem 設定 UTF-8 編碼
chcp 65001 >nul

rem 設定 PowerShell 執行策略（如果需要）
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" >nul 2>&1

echo ========================================
echo 🔧 修復中文顯示問題
echo ========================================
echo.

echo 正在設定系統編碼...
echo.

rem 設定環境變數
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo ✅ UTF-8 編碼已設定
echo ✅ Python 輸出編碼已設定
echo.
echo 現在可以正常使用其他批次檔案了！
echo.
echo 提示：如果仍有亂碼，請：
echo 1. 重新啟動 CMD
echo 2. 或使用 PowerShell 替代 CMD
echo.

pause

# PowerShell 腳本 - 更新漫畫清單
# 設定輸出編碼
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🔄 正在更新漫畫清單..." -ForegroundColor Cyan

# 執行 Python 腳本
try {
    python generate_manifest.py
    Write-Host ""
    Write-Host "✅ 漫畫清單更新完成！" -ForegroundColor Green
    Write-Host ""
    Write-Host "你現在可以：" -ForegroundColor Yellow
    Write-Host "1. 本地預覽：雙擊 start_local_server.bat 或 start_local_server.ps1" -ForegroundColor White
    Write-Host "2. 提交到 GitHub 來更新 GitHub Pages" -ForegroundColor White
} catch {
    Write-Host "❌ 更新失敗，請確認 Python 已安裝且 generate_manifest.py 存在" -ForegroundColor Red
}

Write-Host ""
Read-Host "按 Enter 鍵繼續"

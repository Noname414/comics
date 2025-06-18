# PowerShell 腳本 - 啟動本地測試伺服器
# 設定輸出編碼
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 四格漫畫本地測試伺服器" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 切換到 docs 目錄
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$docsPath = Join-Path $scriptPath "docs"

if (Test-Path $docsPath) {
    Set-Location $docsPath
    Write-Host "📁 當前目錄: $docsPath" -ForegroundColor Green
} else {
    Write-Host "❌ 找不到 docs 目錄" -ForegroundColor Red
    Read-Host "按 Enter 鍵退出"
    exit
}

Write-Host "🌐 伺服器位址: http://localhost:8000" -ForegroundColor Green
Write-Host "🌐 或使用: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  按 Ctrl+C 可停止伺服器" -ForegroundColor Yellow
Write-Host ""

# 自動開啟瀏覽器
Write-Host "🔗 正在開啟瀏覽器..." -ForegroundColor Cyan
Start-Process "http://localhost:8000"

Write-Host "🚀 啟動 HTTP 伺服器中..." -ForegroundColor Green
Write-Host ""

# 啟動 Python HTTP 伺服器
try {
    python -m http.server 8000
} catch {
    Write-Host "❌ 啟動伺服器失敗，請確認 Python 已安裝" -ForegroundColor Red
    Read-Host "按 Enter 鍵退出"
}

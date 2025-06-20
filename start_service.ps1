# 設定執行路徑
Set-Location "c:\Users\sheng\copilot-projects\comics"

Write-Host "Starting Comic Generator Service..." -ForegroundColor Green
Write-Host ""

Write-Host "[1/3] Checking environment..." -ForegroundColor Yellow
if (-not (Test-Path "comic_api_server.py")) {
    Write-Host "Error: comic_api_server.py not found!" -ForegroundColor Red
    pause
    exit
}

Write-Host "[2/3] Starting API Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\sheng\copilot-projects\comics'; python comic_api_server.py" -WindowStyle Normal

Write-Host "[3/3] Starting Web Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\sheng\copilot-projects\comics\docs'; python -m http.server 8000" -WindowStyle Normal

Write-Host ""
Write-Host "Service started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Web URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Test Page: http://localhost:8000/test.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tips:" -ForegroundColor Yellow
Write-Host "- Wait 10-15 seconds for services to fully start"
Write-Host "- Keep both PowerShell windows open for proper operation"
Write-Host "- Test the generation function on the web page"
Write-Host ""

# 等待 5 秒後自動開啟瀏覽器
Write-Host "Opening browser in 5 seconds..." -ForegroundColor Magenta
Start-Sleep -Seconds 5
Start-Process "http://localhost:8000"

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

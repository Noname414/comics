# 四格漫畫生成器 - Vercel 部署腳本
# 執行此腳本前請確保已安裝 Git 和 Vercel CLI

Write-Host "🎨 四格漫畫生成器 - Vercel 部署" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# 檢查是否為 Git 倉庫
if (-not (Test-Path ".git")) {
    Write-Host "❌ 錯誤：當前目錄不是 Git 倉庫" -ForegroundColor Red
    Write-Host "請先初始化 Git 倉庫：git init" -ForegroundColor Yellow
    exit 1
}

# 檢查是否有變更需要提交
$status = git status --porcelain
if ($status) {
    Write-Host "📝 偵測到檔案變更，正在提交..." -ForegroundColor Yellow
    
    # 添加所有檔案
    git add .
    
    # 提交變更
    $commitMessage = "feat: 準備 Vercel 部署 - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMessage
    
    Write-Host "✅ 變更已提交：$commitMessage" -ForegroundColor Green
}

# 推送到 GitHub
Write-Host "🚀 正在推送到 GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 成功推送到 GitHub" -ForegroundColor Green
} else {
    Write-Host "❌ 推送失敗，請檢查 GitHub 連線" -ForegroundColor Red
    exit 1
}

# 檢查是否安裝 Vercel CLI
try {
    vercel --version | Out-Null
    Write-Host "✅ Vercel CLI 已安裝" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Vercel CLI 未安裝" -ForegroundColor Yellow
    Write-Host "請安裝 Vercel CLI：npm install -g vercel" -ForegroundColor Yellow
    
    $install = Read-Host "是否現在安裝？(y/N)"
    if ($install -eq "y" -or $install -eq "Y") {
        npm install -g vercel
    } else {
        Write-Host "請手動安裝 Vercel CLI 後重新執行此腳本" -ForegroundColor Yellow
        exit 1
    }
}

# 詢問是否執行 Vercel 部署
Write-Host ""
Write-Host "🌐 準備部署到 Vercel" -ForegroundColor Cyan
Write-Host "部署前請確認：" -ForegroundColor Yellow
Write-Host "1. 已註冊 Vercel 帳號" -ForegroundColor Yellow
Write-Host "2. 已取得 Google API 金鑰" -ForegroundColor Yellow
Write-Host "3. GitHub 倉庫設定正確" -ForegroundColor Yellow

$deploy = Read-Host "是否現在部署到 Vercel？(y/N)"

if ($deploy -eq "y" -or $deploy -eq "Y") {
    Write-Host "🚀 開始部署..." -ForegroundColor Green
    
    # 執行 Vercel 部署
    vercel --prod
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 部署成功！" -ForegroundColor Green
        Write-Host "📋 請記得在 Vercel Dashboard 設定環境變數：" -ForegroundColor Yellow
        Write-Host "   GOOGLE_API_KEY = 您的 Google API 金鑰" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📚 詳細說明請參考：VERCEL_DEPLOYMENT.md" -ForegroundColor Cyan
    } else {
        Write-Host "❌ 部署失敗" -ForegroundColor Red
        Write-Host "請檢查 Vercel CLI 設定或網路連線" -ForegroundColor Yellow
    }
} else {
    Write-Host "💡 手動部署步驟：" -ForegroundColor Cyan
    Write-Host "1. 前往 https://vercel.com/dashboard" -ForegroundColor White
    Write-Host "2. 點擊 'New Project'" -ForegroundColor White
    Write-Host "3. 選擇您的 GitHub 倉庫" -ForegroundColor White
    Write-Host "4. 設定環境變數 GOOGLE_API_KEY" -ForegroundColor White
    Write-Host "5. 點擊 Deploy" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 詳細說明請參考：VERCEL_DEPLOYMENT.md" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎨 感謝使用四格漫畫生成器！" -ForegroundColor Cyan 
# Vercel 部署指南

## 🚀 部署到 Vercel

### 前置需求

1. **GitHub 帳號**: 確保您的專案已經推送到 GitHub
2. **Vercel 帳號**: 註冊 [Vercel](https://vercel.com) 帳號
3. **Google API 金鑰**: 從 [Google AI Studio](https://makersuite.google.com/app/apikey) 取得

### 步驟 1: 連接 GitHub 倉庫

1. 登入 [Vercel Dashboard](https://vercel.com/dashboard)
2. 點擊 "New Project"
3. 選擇您的 GitHub 倉庫：`sheng-luen-chung/comics`
4. 點擊 "Import"

### 步驟 2: 配置專案設定

在 Vercel 的專案設定頁面：

1. **Framework Preset**: 選擇 "Other"
2. **Root Directory**: 保持預設（根目錄）
3. **Build Settings**:
   - Build Command: 留空或 `echo "Static site"`
   - Output Directory: `docs`
   - Install Command: `npm install`

### 步驟 3: 設定環境變數

在 "Environment Variables" 區域新增：

```
Key: GOOGLE_API_KEY
Value: 您的 Google API 金鑰
Environment: Production, Preview, Development
```

### 步驟 4: 部署

1. 點擊 "Deploy" 按鈕
2. 等待部署完成（約 1-2 分鐘）
3. 部署成功後會看到您的網站 URL

## 🔧 專案架構

```
comics/
├── api/                     # Vercel Serverless Functions
│   ├── requirements.txt     # Python 依賴
│   ├── generate-comic.py    # 漫畫生成 API
│   └── health.py           # 健康檢查 API
├── docs/                   # 前端靜態檔案
│   ├── index.html          # 主頁面
│   ├── comic-api.js        # 前端 JavaScript
│   └── comics_manifest.json # 漫畫清單
├── vercel.json             # Vercel 配置
└── package.json            # Node.js 專案設定
```

## 🌐 API 端點

部署後可用的 API 端點：

- `GET /api/health` - API 健康檢查
- `POST /api/generate-comic` - 漫畫生成請求（引導到 GitHub Actions）

## 📝 使用方式

### 在線生成漫畫

1. 訪問您的 Vercel 網站 URL
2. 在輸入框中輸入新聞關鍵字
3. 點擊 "生成四格漫畫" 按鈕
4. 系統會引導您到 GitHub Actions 完成實際生成
5. 執行完成後返回網站重新整理查看結果

### GitHub Actions 工作流程

由於 Vercel 的執行時間限制（10 秒），實際的漫畫生成透過 GitHub Actions 完成：

1. 前往 [GitHub Actions](https://github.com/sheng-luen-chung/comics/actions)
2. 選擇 "Generate Comic from Keyword" 工作流程
3. 點擊 "Run workflow"
4. 輸入關鍵字並執行
5. 等待 2-3 分鐘完成生成

## 🛠️ 故障排除

### 常見問題

**Q: API 無法正常運作？**
A: 確認環境變數 `GOOGLE_API_KEY` 已正確設定

**Q: 部署失敗？**
A: 檢查是否有語法錯誤，或查看 Vercel 的建置日誌

**Q: 漫畫無法顯示？**
A: 確認 `docs/comics_manifest.json` 檔案存在且格式正確

**Q: 生成功能不工作？**
A: 確認您有 GitHub 倉庫的寫入權限，且 Actions 已啟用

### 重新部署

如果需要重新部署：

1. 推送更新到 GitHub
2. Vercel 會自動偵測並重新部署
3. 或在 Vercel Dashboard 手動觸發重新部署

### 檢查日誌

- Vercel Dashboard > 專案 > Functions > 查看函數執行日誌
- GitHub Actions > 查看工作流程執行狀態

## 🔄 更新專案

### 更新前端

1. 修改 `docs/` 目錄下的檔案
2. 推送到 GitHub
3. Vercel 自動重新部署

### 更新 API

1. 修改 `api/` 目錄下的檔案
2. 推送到 GitHub
3. Vercel 自動重新部署 Serverless Functions

### 更新漫畫清單

1. 執行 GitHub Actions 工作流程生成新漫畫
2. 或手動更新 `docs/comics_manifest.json`
3. 推送更新到 GitHub

## 📊 監控與分析

### Vercel Analytics

在 Vercel Dashboard 中可以查看：

- 網站訪問量
- 函數執行次數
- 效能指標
- 錯誤率

### 成本控制

- Vercel 免費方案足夠個人使用
- 監控函數執行次數避免超額
- 考慮使用 GitHub Actions 減少 Serverless 函數使用

## 🔐 安全設定

### 環境變數保護

- 不要在程式碼中暴露 API 金鑰
- 使用 Vercel 的環境變數功能
- 定期輪換 API 金鑰

### CORS 設定

API 已設定允許跨域請求，但在生產環境中可以考慮：

- 限制允許的來源域名
- 使用更嚴格的 CORS 政策

---

## 🎉 部署完成！

恭喜！您的四格漫畫生成器現在已經部署到 Vercel 上了。

- 🌐 **網站 URL**: `https://your-project.vercel.app`
- 🔧 **API 端點**: `https://your-project.vercel.app/api/`
- 📚 **GitHub**: `https://github.com/sheng-luen-chung/comics`

享受您的 AI 漫畫創作之旅！🎨

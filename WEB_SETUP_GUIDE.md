# 🎨 網頁端四格漫畫生成器設定指南

## 概述
此系統允許使用者直接在網頁上輸入關鍵字，自動觸發 GitHub Actions 生成四格漫畫。

## 設定步驟

### 1. GitHub Repository 設定

#### 1.1 設定 Secrets
在你的 GitHub 倉庫中設定以下 secrets：

1. 前往 `Settings` > `Secrets and variables` > `Actions`
2. 點擊 `New repository secret`
3. 添加以下 secrets：
   - `GOOGLE_API_KEY`: 你的 Google Gemini API 金鑰

#### 1.2 啟用 GitHub Pages
1. 前往 `Settings` > `Pages`
2. Source 選擇 `Deploy from a branch`
3. Branch 選擇 `main`
4. Folder 選擇 `/docs`
5. 點擊 `Save`

#### 1.3 設定 Actions 權限
1. 前往 `Settings` > `Actions` > `General`
2. 在 "Workflow permissions" 選擇 `Read and write permissions`
3. 勾選 `Allow GitHub Actions to create and approve pull requests`

### 2. 本地配置檔案更新

請更新 `docs/comic-api.js` 中的 GitHub 配置：

```javascript
const GITHUB_CONFIG = {
    owner: 'YOUR_GITHUB_USERNAME',  // 替換為你的 GitHub 用戶名
    repo: 'comics',                 // 替換為你的倉庫名稱
    token: null
};
```

### 3. 使用方式

#### 方案A: GitHub Issues 觸發（推薦）
使用者在網頁上輸入關鍵字後，系統會：
1. 創建一個 GitHub Issue
2. 自動觸發 GitHub Actions
3. 生成漫畫並更新網站
4. 自動關閉 Issue

#### 方案B: 手動觸發
如果自動觸發遇到問題，可以：
1. 前往 GitHub Repository 的 `Actions` 標籤
2. 選擇 "Generate Comic from Keyword" workflow
3. 點擊 `Run workflow`
4. 輸入關鍵字並執行

### 4. 工作流程

```
用戶輸入關鍵字 → 創建 GitHub Issue → 觸發 Actions → 
執行 comic_generator.py → 生成漫畫 → 更新 manifest → 
推送到 GitHub → GitHub Pages 自動更新 → 用戶看到新漫畫
```

### 5. 故障排除

#### 5.1 如果生成失敗
1. 檢查 GitHub Actions 日誌
2. 確認 `GOOGLE_API_KEY` 設定正確
3. 檢查 API 配額是否足夠

#### 5.2 如果網站不更新
1. 檢查 GitHub Pages 部署狀態
2. 強制重新整理瀏覽器 (Ctrl+F5)
3. 檢查 `comics_manifest.json` 是否更新

#### 5.3 生成時間太長
- 正常生成時間約 2-3 分鐘
- 如果超過 10 分鐘，可能是 API 限制或網路問題

### 6. 限制與注意事項

1. **API 限制**: Google Gemini API 有使用配額限制
2. **生成頻率**: 建議控制生成頻率，避免超出限制
3. **安全性**: 目前版本不包含用戶認證，任何人都可以觸發生成
4. **儲存空間**: 每個漫畫約占用 2-5MB 空間

### 7. 未來改進

- [ ] 添加用戶認證系統
- [ ] 實現即時狀態更新
- [ ] 添加生成隊列管理
- [ ] 優化圖像壓縮
- [ ] 添加漫畫分類功能

### 8. 成本估算

- GitHub Actions: 免費額度通常足夠
- GitHub Pages: 免費
- Google Gemini API: 根據使用量計費
- 存儲空間: GitHub 免費倉庫 1GB 限制

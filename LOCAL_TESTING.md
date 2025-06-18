# 本地測試指南

## 🚀 快速開始

### 方法一：使用批次檔案（最簡單）
1. 雙擊 `start_local_server.bat`
2. 瀏覽器會自動開啟 http://localhost:8000
3. 按 Ctrl+C 停止伺服器

### 方法二：手動啟動
```bash
# 1. 進入 docs 目錄
cd docs

# 2. 啟動 HTTP 伺服器
python -m http.server 8000

# 3. 開啟瀏覽器訪問
# http://localhost:8000
```

### 方法三：使用 VS Code Live Server
1. 安裝 "Live Server" 擴展
2. 右鍵點擊 `docs/index.html`
3. 選擇 "Open with Live Server"

## 🧪 測試流程

### 1. 測試現有漫畫展示
- 確認頁面正常載入
- 檢查是否顯示 2 個現有漫畫
- 測試圖片點擊放大功能
- 測試響應式設計（調整瀏覽器視窗大小）

### 2. 生成新漫畫並測試
```bash
# 1. 生成新漫畫
python comic_generator.py

# 2. 更新漫畫清單
python generate_manifest.py

# 3. 重新整理瀏覽器頁面
# 應該會看到新的漫畫出現
```

### 3. 測試項目檢查清單
- [ ] 頁面正常載入，沒有 JavaScript 錯誤
- [ ] 漫畫圖片正常顯示
- [ ] 點擊圖片能夠放大檢視
- [ ] 漫畫標題、日期、關鍵字正確顯示
- [ ] 在手機尺寸下頁面布局正常
- [ ] 新生成的漫畫能夠正常出現在列表中

## 🔧 常見問題

### 問題：瀏覽器顯示 "無法連接"
**解決方案：**
- 確認 HTTP 伺服器正在執行
- 檢查是否有其他程式佔用 port 8000
- 嘗試使用其他 port：`python -m http.server 8080`

### 問題：圖片無法顯示
**解決方案：**
- 確認圖片檔案存在於正確位置
- 檢查 `comics_manifest.json` 中的路徑是否正確
- 重新執行 `python generate_manifest.py`

### 問題：新漫畫沒有出現
**解決方案：**
- 確認新漫畫已生成到 `docs/` 目錄
- 執行 `python generate_manifest.py` 更新清單
- 重新整理瀏覽器頁面（Ctrl+F5 強制重新載入）

### 問題：JavaScript 錯誤
**解決方案：**
- 開啟瀏覽器開發者工具（F12）查看錯誤訊息
- 確認 `comics_manifest.json` 格式正確
- 檢查網路連線

## 📱 測試不同裝置

### 桌面電腦測試
- Chrome/Edge：http://localhost:8000
- Firefox：http://localhost:8000

### 手機模擬測試
1. 開啟瀏覽器開發者工具（F12）
2. 點擊手機圖示切換到行動裝置模式
3. 選擇不同裝置尺寸測試

### 實際手機測試
1. 確保手機和電腦在同一 WiFi 網路
2. 查詢電腦 IP 位址：`ipconfig`
3. 在手機瀏覽器訪問：`http://[電腦IP]:8000`

## 🎯 效能測試

### 載入速度測試
- 使用瀏覽器開發者工具的 Network 頁籤
- 檢查圖片載入時間
- 確認總頁面載入時間合理

### 圖片優化建議
如果圖片太大，可以考慮：
- 壓縮 PNG 圖片
- 轉換為 WebP 格式
- 實作懶載入（lazy loading）

## 🚀 部署前檢查

在部署到 GitHub Pages 前，確認：
- [ ] 本地測試完全正常
- [ ] 所有圖片和檔案都在 `docs/` 目錄下
- [ ] `comics_manifest.json` 已更新
- [ ] 沒有包含敏感資訊（API 金鑰等）
- [ ] `.gitignore` 設定正確

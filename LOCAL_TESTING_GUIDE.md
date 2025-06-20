# 📖 本地測試指南

## 🚀 快速開始

### 方法一：完整服務（推薦）
啟動網頁界面 + API 服務，支援生成新漫畫
```batch
# 雙擊執行
start_full_service.bat

# 或手動執行
python comic_api_server.py  # 啟動 API (終端 1)
cd docs && python -m http.server 8000  # 啟動網頁 (終端 2)
```
- 🌐 網頁界面: http://localhost:8000
- 🔧 API 服務: http://localhost:5000

### 方法二：僅瀏覽模式
只啟動網頁伺服器，瀏覽現有漫畫
```batch
# 雙擊執行
start_local_server.bat

# 或手動執行
cd docs
python -m http.server 8000
```
- 🌐 網頁界面: http://localhost:8000

## 🔧 替代測試方法

### 使用 VS Code Live Server
1. 在 VS Code 中安裝 "Live Server" 擴展
2. 右鍵點擊 `docs/index.html`
3. 選擇 "Open with Live Server"
4. ⚠️ 注意：此方法無法使用生成功能

### 使用 Node.js serve
```bash
npx serve docs
```

### 方法四：使用 PHP（如果有安裝）
```bash
cd docs
php -S localhost:8000
```

## 🧪 測試檢查清單

### ✅ 基本功能測試
- [ ] 頁面能正常載入
- [ ] 顯示漫畫總數 "總共找到 2 個漫畫作品"
- [ ] 兩個漫畫卡片都顯示出來
- [ ] 漫畫圖片完整顯示（不被截掉）
- [ ] 點擊圖片能放大檢視
- [ ] 按 ESC 或點擊外部能關閉放大檢視

### ✅ 響應式設計測試
- [ ] 在桌面瀏覽器中正常顯示
- [ ] 在手機模式下正常顯示
- [ ] 調整瀏覽器視窗大小時布局正確調整

### ✅ 內容測試
- [ ] 漫畫標題正確顯示
- [ ] 生成日期正確顯示
- [ ] 關鍵字標籤正確顯示
- [ ] 圖片載入正常

## 🐛 常見問題解決

### Q: 頁面顯示空白或載入失敗
**解決方法：**
1. 確認已在 docs 目錄啟動伺服器
2. 檢查控制台是否有錯誤訊息
3. 確認 comics_manifest.json 文件存在

### Q: 圖片顯示不出來
**解決方法：**
1. 確認圖片文件確實存在於對應資料夾
2. 檢查圖片路徑是否正確
3. 重新生成 manifest：`python generate_manifest.py`

### Q: 漫畫被截掉上下部分
**解決方法：**
已修復！現在使用 `object-fit: contain` 確保完整顯示。

### Q: 手機上顯示不正常
**解決方法：**
已添加響應式設計，應該在各種設備上都能正常顯示。

## 📱 在不同設備上測試

### 桌面瀏覽器
- Chrome, Firefox, Edge, Safari

### 手機測試
1. 在電腦上使用瀏覽器開發者工具模擬手機
2. 或在同一網路下的手機訪問：http://你的電腦IP:8000

### 獲取電腦IP地址
```powershell
ipconfig | findstr IPv4
```

## 🔄 更新測試流程

1. 修改代碼後，刷新瀏覽器頁面
2. 如果生成新漫畫，執行：`python generate_manifest.py`
3. 然後刷新頁面查看新內容

## 📊 測試數據

目前應該能看到：
- 川普提前結束G7 (2025年06月18日 19:14)
- 小S撈錢 (2025年06月17日 16:33)

每個漫畫應該顯示完整的四格內容，不會被截掉。

# 漫畫生成器網頁測試指南

## 快速啟動

1. **啟動完整服務**
   ```
   雙擊執行：start_complete_service.bat
   ```

2. **檢查服務狀態**
   ```
   雙擊執行：check_services.bat
   ```

3. **開啟網頁**
   - 主要網頁：http://localhost:8000
   - 測試頁面：http://localhost:8000/test.html

## 修正問題

✅ **已修正的問題：**
- 按鈕點擊事件函數名稱不匹配 (`generateComicWithStatusCheck()` → `generateComic()`)
- 移除了 `comic-api.js` 引用避免函數衝突
- 修正 `comic-api.js` 中的重複程式碼

## 測試步驟

### 1. 基本功能測試
1. 開啟 http://localhost:8000/test.html
2. 檢查是否顯示「按鈕點擊正常！」
3. 檢查是否顯示「API 連接成功」

### 2. 完整生成測試
1. 開啟 http://localhost:8000
2. 在輸入框輸入關鍵字（例如：台股、選舉）
3. 點擊「🎯 生成四格漫畫」按鈕
4. 應該會看到：
   - 按鈕變成「🔄 生成中...」
   - 狀態顯示「🚀 正在啟動生成程序...」
   - 進度條顯示

### 3. 如果還是沒反應

檢查瀏覽器控制台（F12）是否有錯誤訊息：

1. 按 F12 開啟開發者工具
2. 切換到 Console 標籤
3. 點擊生成按鈕
4. 查看是否有紅色錯誤訊息

## 常見問題排除

### API 服務器未啟動
- 症狀：按鈕點擊後顯示「無法連接到生成服務」
- 解決：確認 `comic_api_server.py` 正在運行

### 網頁服務器未啟動
- 症狀：無法開啟 http://localhost:8000
- 解決：確認 `python -m http.server 8000` 正在 docs 目錄中運行

### JavaScript 錯誤
- 症狀：按鈕完全沒反應
- 解決：檢查瀏覽器控制台錯誤訊息

## 手動啟動方式

如果批次檔無法運行，可手動啟動：

### 啟動 API 服務器
```powershell
cd "c:\Users\sheng\copilot-projects\comics"
python comic_api_server.py
```

### 啟動網頁服務器
```powershell
cd "c:\Users\sheng\copilot-projects\comics\docs"
python -m http.server 8000
```

## 預期流程

1. **輸入關鍵字** → 點擊按鈕
2. **按鈕狀態改變** → 顯示「生成中...」
3. **API 呼叫** → 後台開始生成漫畫
4. **進度更新** → 顯示生成步驟和進度條
5. **完成通知** → 頁面自動重新載入顯示新漫畫

如果任何步驟失敗，請檢查對應的服務是否正在運行。

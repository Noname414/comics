# 四格漫畫生成器 - GitHub Pages 展示

## 概述

這個專案現在將所有生成的四格漫畫輸出到 `docs/` 目錄下，以便於在 GitHub Pages 上展示。

## 目錄結構

```
comics/
├── comic_generator.py          # 主要的漫畫生成程式
├── generate_manifest.py        # 生成漫畫清單的工具程式
├── start_local_server.bat      # 一鍵啟動本地測試伺服器 (CMD版)
├── start_local_server.ps1      # 一鍵啟動本地測試伺服器 (PowerShell版，推薦)
├── update_gallery.bat          # 一鍵更新漫畫清單 (CMD版)
├── update_gallery.ps1          # 一鍵更新漫畫清單 (PowerShell版，推薦)
├── fix_encoding.bat            # 修復中文亂碼問題
├── LOCAL_TESTING_GUIDE.md      # 詳細測試指南
├── requirements.txt            # Python 依賴套件
├── docs/                       # GitHub Pages 輸出目錄
│   ├── index.html             # 主頁面（已優化圖片顯示）
│   ├── comics_manifest.json   # 漫畫清單 (自動生成)
│   ├── README.md              # 本說明文檔
│   └── comic_output_*/        # 生成的漫畫資料夾
│       ├── four_panel_comic.png
│       ├── comic_script.txt
│       └── comic_panel_*.png
```

## 使用方法

### 1. 生成四格漫畫

```bash
python comic_generator.py
```

漫畫將會自動儲存到 `docs/comic_output_{關鍵字}_{時間戳}/` 目錄中。

### 2. 更新漫畫清單

每次生成新漫畫後，執行以下命令來更新展示頁面的漫畫清單：

```bash
python generate_manifest.py
```

這將會掃描 `docs/` 目錄下的所有漫畫，並生成 `docs/comics_manifest.json` 文件。

### 3. 本地測試

#### 🚀 快速開始（推薦方法）

**方法一：使用 PowerShell 腳本（推薦，無亂碼問題）**
```powershell
# 雙擊運行根目錄下的 PowerShell 腳本
start_local_server.ps1
```

**方法二：使用批次檔案（已修復中文亂碼）**
```bash
# 雙擊運行根目錄下的批次檔案
start_local_server.bat
```

**方法三：手動啟動 Python 伺服器**
```bash
# 切換到 docs 目錄
cd docs
python -m http.server 8000
```

**方法三：使用 VS Code Live Server**
1. 安裝 VS Code 的 "Live Server" 擴展
2. 右鍵點擊 `docs/index.html`
3. 選擇 "Open with Live Server"

**方法四：使用 Node.js serve**
```bash
npx serve docs
```

#### 📍 訪問地址
啟動伺服器後，在瀏覽器中訪問：
- http://localhost:8000
- http://127.0.0.1:8000

#### 🧪 本地測試檢查清單

**基本功能測試：**
- [ ] 頁面能正常載入
- [ ] 顯示正確的漫畫總數
- [ ] 漫畫卡片都能正常顯示
- [ ] 漫畫圖片完整顯示（不被截掉上下部分）
- [ ] 點擊圖片能放大檢視
- [ ] 放大檢視能正常關閉

**響應式設計測試：**
- [ ] 桌面瀏覽器顯示正常
- [ ] 手機模式顯示正常
- [ ] 調整視窗大小時布局正確

**內容顯示測試：**
- [ ] 漫畫標題顯示正確
- [ ] 生成日期格式正確
- [ ] 關鍵字標籤顯示正常

#### 🐛 常見問題排除

**Q: 頁面顯示空白**
```bash
# 解決方法：
1. 確認在 docs 目錄啟動伺服器
2. 檢查 comics_manifest.json 是否存在
3. 重新生成清單：python generate_manifest.py
```

**Q: 圖片無法載入**
```bash
# 解決方法：
1. 確認圖片文件存在於對應資料夾
2. 檢查瀏覽器控制台錯誤訊息
3. 重新生成清單更新路徑
```

**Q: 手機上顯示異常**
```bash
# 解決方法：
1. 清除瀏覽器快取
2. 使用瀏覽器開發者工具測試不同屏幕尺寸
3. 確認網路連線正常
```

**Q: CMD 中顯示中文亂碼**
```bash
# 解決方法：
1. 使用 PowerShell 腳本（推薦）：start_local_server.ps1
2. 或雙擊運行 fix_encoding.bat 修復編碼
3. 或在 CMD 中手動執行：chcp 65001
4. 重新啟動 CMD 視窗
```

**Q: PowerShell 腳本無法執行**
```powershell
# 解決方法：
1. 以管理員身份開啟 PowerShell
2. 執行：Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
3. 或雙擊 fix_encoding.bat 自動設定
```

#### 📱 在不同設備測試

**同網路下的手機測試：**
1. 獲取電腦 IP 地址：
   ```powershell
   ipconfig | findstr IPv4
   ```
2. 在手機瀏覽器訪問：`http://你的電腦IP:8000`

**瀏覽器相容性測試：**
- Chrome（推薦）
- Firefox
- Edge
- Safari（Mac/iOS）

#### 🔄 更新測試流程

1. **修改頁面後：** 直接刷新瀏覽器
2. **生成新漫畫後：** 
   ```bash
   # 方法一：使用 PowerShell（推薦）
   雙擊 update_gallery.ps1
   
   # 方法二：使用批次檔案
   雙擊 update_gallery.bat
   
   # 方法三：手動執行
   python generate_manifest.py
   ```
3. **修改 CSS 樣式後：** 強制刷新（Ctrl+F5）

#### 🛠️ 工具檔案說明

**自動化腳本：**
- `start_local_server.ps1` - PowerShell版本伺服器啟動器（推薦，無亂碼）
- `start_local_server.bat` - CMD版本伺服器啟動器（已修復亂碼）
- `update_gallery.ps1` - PowerShell版本清單更新器（推薦）
- `update_gallery.bat` - CMD版本清單更新器（已修復亂碼）

**問題修復工具：**
- `fix_encoding.bat` - 一鍵修復中文亂碼和 PowerShell 執行策略

## GitHub Pages 設定

1. 在 GitHub 倉庫的 Settings 中
2. 找到 "Pages" 設定
3. 選擇 "Deploy from a branch"
4. 選擇分支為 `main` 或 `master`
5. 選擇資料夾為 `/docs`
6. 儲存設定

設定完成後，你的四格漫畫作品將會在 `https://你的用戶名.github.io/倉庫名稱/` 上展示。

## 特色功能

### 展示頁面功能
- 📱 響應式設計，支援手機和電腦瀏覽
- 🖼️ 點擊圖片可以放大檢視
- 🏷️ 顯示漫畫關鍵字和生成時間
- 🎨 美觀的卡片式布局
- ⚡ 自動載入最新的漫畫作品

### 自動化功能
- 🔄 自動掃描並列出所有生成的漫畫
- 📊 顯示漫畫總數和最後更新時間
- 🗂️ 智能解析資料夾名稱提取資訊

## 更新記錄

- ✅ 將輸出目錄從根目錄移動到 `docs/` 目錄
- ✅ 創建 GitHub Pages 展示頁面
- ✅ 實現自動漫畫清單生成
- ✅ 添加響應式設計和圖片查看功能
- ✅ 修復圖片顯示問題（完整顯示四格漫畫，不被截掉）
- ✅ 創建一鍵啟動本地測試伺服器批次檔案
- ✅ 添加詳細的本地測試指南和故障排除
- ✅ 優化手機端顯示效果
- ✅ 修復 Windows CMD 中文亂碼問題
- ✅ 創建 PowerShell 版本腳本，支援更好的中文顯示
- ✅ 添加編碼修復工具和執行策略設定

## 注意事項

1. 每次生成新漫畫後，建議使用 `update_gallery.ps1` 或 `update_gallery.bat` 來更新清單
2. 如遇到中文亂碼，優先使用 PowerShell 腳本或執行 `fix_encoding.bat`
3. 可以考慮設定 GitHub Actions 來自動化更新過程
4. 圖片文件可能較大，注意 GitHub 倉庫大小限制
5. 確保 API 金鑰不要提交到 GitHub 倉庫中

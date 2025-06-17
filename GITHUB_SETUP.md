# GitHub 推送步驟

## 1. 初始化 Git 倉庫（如果還沒有）

```bash
cd "c:\Users\Sheng-Luen Cheng\copilot-projects\comics"
git init
```

## 2. 添加所有檔案到暫存區

```bash
git add .
```

## 3. 創建第一次提交

```bash
git commit -m "Initial commit: 四格漫畫生成器"
```

## 4. 在 GitHub 上創建新倉庫

1. 前往 https://github.com
2. 點擊右上角的 "+" 號，選擇 "New repository"
3. 輸入倉庫名稱，例如：`comic-generator` 或 `四格漫畫生成器`
4. 可以添加描述：`AI-powered 4-panel comic generator using Google Gemini API`
5. 選擇 Public 或 Private
6. **不要**勾選 "Add a README file"（因為我們已經有了）
7. 點擊 "Create repository"

## 5. 連接本地倉庫到 GitHub

```bash
git remote add origin https://github.com/你的用戶名/你的倉庫名.git
```

## 6. 推送到 GitHub

```bash
git branch -M main
git push -u origin main
```

## 完成！

現在您的專案就在 GitHub 上了！

## 後續更新

當您修改代碼後，可以用以下命令更新：

```bash
git add .
git commit -m "描述您的更改"
git push
```

## 注意事項

- API 金鑰不會被上傳（已在 .gitignore 中排除）
- 輸出資料夾也不會被上傳
- 確保在 README.md 中說明如何設定 API 金鑰

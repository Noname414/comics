// GitHub Repository 設定
const GITHUB_CONFIG = {
    owner: 'YOUR_GITHUB_USERNAME',  // 請替換為你的 GitHub 用戶名
    repo: 'comics',                 // 請替換為你的倉庫名稱
    // 當前使用手動觸發方案
};

// 當前實現：引導用戶到 GitHub Actions 手動觸發
async function triggerComicGeneration(keyword) {
    try {
        // 準備 GitHub Actions URL
        const actionsUrl = `https://github.com/${GITHUB_CONFIG.owner}/${GITHUB_CONFIG.repo}/actions/workflows/generate-comic.yml`;
        
        // 顯示指引訊息
        const instructions = `
為了生成「${keyword}」的四格漫畫，請按照以下步驟：

1. 🔗 點擊以下連結前往 GitHub Actions
2. 📝 點擊 "Run workflow" 按鈕
3. ⌨️ 在 "新聞關鍵字" 欄位輸入：${keyword}
4. ▶️ 點擊綠色的 "Run workflow" 按鈕
5. ⏱️ 等待 2-3 分鐘後回到此頁面重新整理

點擊下方按鈕前往 GitHub Actions：
        `;
        
        // 創建彈出視窗
        if (confirm(instructions + '\n\n是否現在前往 GitHub Actions？')) {
            window.open(actionsUrl, '_blank');
            return true;
        }
        
        return false;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// 檢查生成狀態
async function checkGenerationStatus(keyword) {
    try {
        // 重新載入 manifest 檢查是否有新漫畫
        const response = await fetch('comics_manifest.json?t=' + Date.now());
        if (!response.ok) return false;
        
        const manifest = await response.json();
        
        // 檢查是否有包含關鍵字的新漫畫（5分鐘內）
        const recentComic = manifest.comics.find(comic => 
            comic.keyword.includes(keyword) && 
            new Date(comic.timestamp) > new Date(Date.now() - 5 * 60 * 1000)
        );
        
        return !!recentComic;
    } catch (error) {
        console.error('Error checking status:', error);
        return false;
    }
}

// 改進的生成函數
async function generateComicWithStatusCheck() {
    const keywordInput = document.getElementById('keywordInput');
    const generateBtn = document.getElementById('generateBtn');
    const btnText = document.getElementById('btnText');
    const btnLoading = document.getElementById('btnLoading');
    const statusDiv = document.getElementById('generateStatus');
    
    const keyword = keywordInput.value.trim();
    
    if (!keyword) {
        showStatus('請輸入新聞關鍵字', 'error');
        return;
    }
    
    // 禁用按鈕
    generateBtn.disabled = true;
    
    try {
        showStatus('正在準備生成流程...', 'info');
        
        // 觸發生成（當前版本會引導到 GitHub）
        const success = await triggerComicGeneration(keyword);
        
        if (success) {
            showStatus(`✅ 已引導到 GitHub Actions！請按照指示完成「${keyword}」四格漫畫生成`, 'success');
            
            // 提供手動重新整理按鈕
            setTimeout(() => {
                showStatus(`🔄 生成完成後，點擊這裡重新載入： 
                    <button onclick="location.reload()" style="padding: 0.5rem 1rem; margin-left: 1rem; background: #4ECDC4; color: white; border: none; border-radius: 5px; cursor: pointer;">重新整理頁面</button>`, 'info');
            }, 3000);
            
        } else {
            showStatus('❌ 取消生成', 'error');
        }
        
    } catch (error) {
        console.error('Generation error:', error);
        showStatus('❌ 準備過程中發生錯誤', 'error');
    } finally {
        // 重新啟用按鈕
        setTimeout(() => {
            generateBtn.disabled = false;
        }, 2000);
    }
}

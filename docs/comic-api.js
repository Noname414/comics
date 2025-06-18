// GitHub Repository 設定
const GITHUB_CONFIG = {
    owner: 'sheng-luen-chung',  // 你的 GitHub 用戶名
    repo: 'comics',             // 你的倉庫名稱
    // 當前使用手動觸發方案
};

// 當前實現：引導用戶到 GitHub Actions 手動觸發
async function triggerComicGeneration(keyword) {
    try {
        // 準備 GitHub Actions URL
        const actionsUrl = `https://github.com/${GITHUB_CONFIG.owner}/${GITHUB_CONFIG.repo}/actions/workflows/generate-comic.yml`;
        
        // 直接開啟 GitHub Actions 頁面
        window.open(actionsUrl, '_blank');
        
        // 顯示詳細指引
        showDetailedInstructions(keyword);
        
        return true;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// 顯示詳細操作指引
function showDetailedInstructions(keyword) {
    const instructionsHtml = `
        <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px; max-width: 600px; margin: 1rem auto; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
            <h3 style="color: #333; margin-bottom: 1rem;">📋 操作指引</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">已為您開啟 GitHub Actions 頁面，請按照以下步驟完成「<strong>${keyword}</strong>」四格漫畫生成：</p>
            
            <ol style="color: #555; line-height: 1.8; margin-bottom: 1.5rem;">
                <li>在新開啟的頁面中找到 <strong>"Run workflow"</strong> 按鈕（綠色按鈕）</li>
                <li>點擊 <strong>"Run workflow"</strong></li>
                <li>在彈出的表單中，<strong>"新聞關鍵字"</strong> 欄位輸入：<code style="background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">${keyword}</code></li>
                <li>點擊綠色的 <strong>"Run workflow"</strong> 按鈕執行</li>
                <li>等待 2-3 分鐘後回到此頁面重新整理查看結果</li>
            </ol>
            
            <div style="background: #e8f4fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>💡 提示：</strong> 如果沒有看到 "Run workflow" 按鈕，請確認您已登入 GitHub 並有此倉庫的權限。
            </div>
            
            <button onclick="this.parentElement.remove()" style="background: #4ECDC4; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; cursor: pointer; float: right;">知道了</button>
            <div style="clear: both;"></div>
        </div>
    `;
    
    // 創建覆蓋層
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        z-index: 2000;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    `;
    overlay.innerHTML = instructionsHtml;
    
    // 點擊覆蓋層關閉
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            overlay.remove();
        }
    });
    
    document.body.appendChild(overlay);
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
        showStatus('🚀 正在開啟 GitHub Actions 頁面...', 'info');
        
        // 觸發生成（會開啟新頁面並顯示指引）
        const success = await triggerComicGeneration(keyword);
        
        if (success) {
            showStatus(`✅ 已開啟 GitHub Actions！請在新頁面中輸入「${keyword}」並執行 workflow`, 'success');
            
            // 清空輸入框
            keywordInput.value = '';
            
            // 顯示重新整理提示
            setTimeout(() => {
                showStatus(`
                    <div>
                        <p>� 執行完成後，點擊下方按鈕檢查是否有新漫畫：</p>
                        <button onclick="checkAndReloadComics('${keyword}')" 
                                style="background: #4ECDC4; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; cursor: pointer; margin: 0.5rem;">
                            🔄 檢查新漫畫
                        </button>
                        <button onclick="location.reload()" 
                                style="background: #FF6B6B; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; cursor: pointer; margin: 0.5rem;">
                            🔄 重新整理頁面
                        </button>
                    </div>
                `, 'info');
            }, 3000);
            
        } else {
            showStatus('❌ 開啟 GitHub Actions 失敗', 'error');
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

// 檢查並重新載入漫畫
async function checkAndReloadComics(keyword) {
    showStatus('🔍 正在檢查是否有新漫畫...', 'info');
    
    try {
        const hasNew = await checkGenerationStatus(keyword);
        
        if (hasNew) {
            showStatus('🎉 發現新漫畫！正在重新載入...', 'success');
            setTimeout(() => {
                loadComics();
                showStatus('✅ 頁面已更新', 'success');
            }, 1000);
        } else {
            showStatus('⏰ 還沒有新漫畫，請稍後再試或手動重新整理頁面', 'info');
        }
    } catch (error) {
        showStatus('❌ 檢查過程中發生錯誤', 'error');
        console.error('Check error:', error);
    }
}

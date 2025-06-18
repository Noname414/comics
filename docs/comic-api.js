// GitHub Repository 設定
const GITHUB_CONFIG = {
    owner: 'sheng-luen-chung',  // 你的 GitHub 用戶名
    repo: 'comics',             // 你的倉庫名稱
    // 當前使用手動觸發方案            // 顯示重新整理提示
            setTimeout(() => {
                showStatus(`
                    <div>
                        <p><strong>如果 GitHub Actions 頁面沒有自動開啟：</strong></p>
                        <a href="https://github.com/sheng-luen-chung/comics/actions" target="_blank" 
                           style="display: inline-block; background: #007bff; color: white; padding: 0.8rem 1.5rem; 
                                  border-radius: 8px; text-decoration: none; margin: 0.5rem;">
                            🔗 點擊前往 GitHub Actions
                        </a>
                        <br><br>
                        <p>📖 執行完成後，點擊下方按鈕檢查是否有新漫畫：</p>
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
            }, 2000);導用戶到 GitHub Actions 手動觸發
async function triggerComicGeneration(keyword) {
    try {
        // 準備 GitHub Actions URL - 修正為正確的路徑
        const actionsUrl = `https://github.com/${GITHUB_CONFIG.owner}/${GITHUB_CONFIG.repo}/actions`;
        
        console.log('正在開啟 GitHub Actions 頁面:', actionsUrl);
        
        // 直接開啟 GitHub Actions 頁面
        const newWindow = window.open(actionsUrl, '_blank');
        
        // 檢查是否成功開啟
        if (!newWindow) {
            console.error('無法開啟新視窗，可能被瀏覽器阻擋');
            // 如果被阻擋，直接跳轉到當前頁面
            window.location.href = actionsUrl;
            return true;
        }
        
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
        <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px; max-width: 650px; margin: 1rem auto; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
            <h3 style="color: #333; margin-bottom: 1rem;">📋 GitHub Actions 操作指引</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">已嘗試為您開啟 GitHub Actions 頁面，請按照以下步驟完成「<strong>${keyword}</strong>」四格漫畫生成：</p>
            
            <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #ffc107;">
                <strong>🔗 如果頁面沒有自動開啟：</strong><br>
                <a href="https://github.com/sheng-luen-chung/comics/actions" target="_blank" style="color: #007bff; text-decoration: underline;">
                    點擊這裡手動前往 GitHub Actions
                </a>
            </div>
            
            <h4 style="color: #333; margin: 1.5rem 0 1rem;">操作步驟：</h4>
            <ol style="color: #555; line-height: 1.8; margin-bottom: 1.5rem;">
                <li>在 GitHub Actions 頁面中找到 <strong>"Generate Comic from Keyword"</strong> workflow</li>
                <li>點擊該 workflow 進入詳細頁面</li>
                <li>找到並點擊 <strong>"Run workflow"</strong> 按鈕（灰色或綠色按鈕）</li>
                <li>在彈出的表單中，<strong>"新聞關鍵字"</strong> 欄位輸入：<br>
                    <code style="background: #f0f0f0; padding: 4px 8px; border-radius: 4px; font-size: 1.1em;">${keyword}</code></li>
                <li>點擊綠色的 <strong>"Run workflow"</strong> 按鈕開始執行</li>
                <li>等待 2-3 分鐘執行完成</li>
                <li>回到此頁面點擊下方的 "檢查新漫畫" 按鈕</li>
            </ol>
            
            <div style="background: #e8f4fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>💡 常見問題：</strong><br>
                • 如果看不到 "Run workflow" 按鈕，請確認已登入 GitHub<br>
                • 如果顯示權限錯誤，請確認您有此倉庫的寫入權限<br>
                • 執行時間約 2-3 分鐘，請耐心等待
            </div>
            
            <div style="text-align: center; margin-top: 1.5rem;">
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: #4ECDC4; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; cursor: pointer; margin-right: 1rem;">
                    知道了
                </button>
                <button onclick="window.open('https://github.com/sheng-luen-chung/comics/actions', '_blank')" 
                        style="background: #007bff; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; cursor: pointer;">
                    🔗 前往 GitHub Actions
                </button>
            </div>
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

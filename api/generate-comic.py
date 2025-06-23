import json

def handler(request):
    # 處理 CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 處理 OPTIONS 請求
    if request.method == 'OPTIONS':
        return ('', 200, headers)
    
    # 處理 POST 請求
    if request.method == 'POST':
        try:
            # 解析請求數據
            data = request.get_json()
            if not data:
                return (json.dumps({'success': False, 'error': '無效的請求數據'}), 400, headers)
            
            keyword = data.get('keyword', '').strip()
            
            if not keyword:
                return (json.dumps({'success': False, 'error': '請提供關鍵字'}), 400, headers)
            
            # 返回 GitHub Actions 引導信息
            response = {
                'success': True,
                'message': f'請使用 GitHub Actions 生成「{keyword}」四格漫畫',
                'github_actions_url': 'https://github.com/Noname414/comics/actions/workflows/generate-comic.yml',
                'instructions': {
                    'step1': '前往 GitHub Actions 頁面',
                    'step2': '點擊 "Run workflow" 按鈕', 
                    'step3': f'輸入關鍵字: {keyword}',
                    'step4': '等待執行完成後重新整理此頁面'
                }
            }
            
            return (json.dumps(response, ensure_ascii=False), 200, headers)
            
        except Exception as e:
            response = {'success': False, 'error': f'處理請求時發生錯誤: {str(e)}'}
            return (json.dumps(response, ensure_ascii=False), 500, headers)
    
    # 不支援的方法
    return (json.dumps({'success': False, 'error': '不支援的請求方法'}), 405, headers) 
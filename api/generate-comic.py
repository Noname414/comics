from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/generate-comic', methods=['POST', 'OPTIONS'])
def generate_comic():
    # 處理 CORS
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        # 解析請求數據
        data = request.get_json()
        if not data:
            response = jsonify({'success': False, 'error': '無效的請求數據'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            response = jsonify({'success': False, 'error': '請提供關鍵字'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        # 返回 GitHub Actions 引導信息
        result = {
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
        
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        result = {'success': False, 'error': f'處理請求時發生錯誤: {str(e)}'}
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

if __name__ == '__main__':
    app.run() 
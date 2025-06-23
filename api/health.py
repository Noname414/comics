import json
from datetime import datetime

def handler(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    response = {
        'status': 'ok',
        'message': '四格漫畫生成器 Vercel API 運行中',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return (json.dumps(response, ensure_ascii=False), 200, headers) 
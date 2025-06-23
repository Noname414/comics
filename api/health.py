from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    result = {
        'status': 'ok',
        'message': '四格漫畫生成器 Vercel API 運行中',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run() 
# -*- coding: utf-8 -*-
import os
import sys
# 設定編碼
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 存儲生成狀態
generation_status = {
    'is_generating': False,
    'status': 'idle',
    'message': '',
    'keyword': '',
    'step': 0,
    'total_steps': 4,
    'start_time': None
}

def update_status(status, message, step=None):
    """更新生成狀態"""
    generation_status['status'] = status
    generation_status['message'] = message
    if step is not None:
        generation_status['step'] = step
    print(f"狀態更新: {status} - {message}")

def run_comic_generation(keyword):
    """在背景執行漫畫生成"""
    try:
        generation_status['is_generating'] = True
        generation_status['keyword'] = keyword
        generation_status['start_time'] = datetime.now()
        
        # 步驟 1: 開始生成
        update_status('starting', f'🚀 開始生成「{keyword}」四格漫畫...', 1)
        time.sleep(1)
        
        # 步驟 2: 搜尋新聞
        update_status('searching', f'🔍 正在搜尋「{keyword}」相關新聞...', 2)
          # 執行 Python 腳本
        process = subprocess.Popen(
            ['python', 'comic_generator.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore',
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # 發送關鍵字到腳本
        process.stdin.write(keyword + '\n')
        process.stdin.flush()
        
        # 等待一段時間後更新狀態
        time.sleep(5)
        update_status('generating_script', f'✍️ 正在生成「{keyword}」四格漫畫腳本...', 3)
        
        # 等待腳本完成
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            # 步驟 4: 生成圖像
            update_status('generating_images', f'🎨 正在生成「{keyword}」漫畫圖像...', 4)
            time.sleep(2)
              # 更新 manifest
            subprocess.run(['python', 'generate_manifest.py'], 
                         cwd=os.path.dirname(os.path.abspath(__file__)),
                         encoding='utf-8',
                         errors='ignore')
            
            update_status('completed', f'✅ 「{keyword}」四格漫畫生成完成！', 4)
        else:
            update_status('error', f'❌ 生成失敗: {stderr}', 0)
            
    except Exception as e:
        update_status('error', f'❌ 生成過程中發生錯誤: {str(e)}', 0)
    finally:
        generation_status['is_generating'] = False

@app.route('/generate-comic', methods=['POST'])
def generate_comic():
    """處理漫畫生成請求"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({'success': False, 'error': '請提供關鍵字'}), 400
        
        if generation_status['is_generating']:
            return jsonify({
                'success': False, 
                'error': '目前正在生成其他漫畫，請稍後再試'
            }), 409
        
        # 在背景開始生成
        thread = threading.Thread(target=run_comic_generation, args=(keyword,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'開始生成「{keyword}」四格漫畫'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/generation-status', methods=['GET'])
def get_generation_status():
    """獲取生成狀態"""
    return jsonify(generation_status)

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({'status': 'ok', 'message': '漫畫生成服務運行中'})

if __name__ == '__main__':
    print("🚀 漫畫生成 API 服務器啟動中...")
    print("📡 服務地址: http://localhost:5000")
    print("⚠️  請保持此視窗開啟以使用網頁生成功能")
    app.run(debug=True, host='0.0.0.0', port=5000)

# -*- coding: utf-8 -*-
import os
import sys
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler

# 設定編碼
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 處理 CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        try:
            # 讀取請求內容
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            keyword = data.get('keyword', '').strip()
            
            if not keyword:
                response = {'success': False, 'error': '請提供關鍵字'}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            # 由於 Vercel 的 serverless 限制，我們返回指引訊息
            # 引導用戶使用 GitHub Actions 進行實際生成
            response = {
                'success': True,
                'message': f'請使用 GitHub Actions 生成「{keyword}」四格漫畫',
                'github_actions_url': 'https://github.com/sheng-luen-chung/comics/actions/workflows/generate-comic.yml',
                'instructions': {
                    'step1': '前往 GitHub Actions 頁面',
                    'step2': '點擊 "Run workflow" 按鈕',
                    'step3': f'輸入關鍵字: {keyword}',
                    'step4': '等待執行完成後重新整理此頁面'
                }
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            response = {'success': False, 'error': f'處理請求時發生錯誤: {str(e)}'}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        # 處理 CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 
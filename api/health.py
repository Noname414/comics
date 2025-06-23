# -*- coding: utf-8 -*-
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': '四格漫畫生成器 Vercel API 運行中',
            'timestamp': '2025-01-21'
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8')) 
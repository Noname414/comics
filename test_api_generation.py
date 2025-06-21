import requests
import json

# 測試 API 生成功能
url = 'http://localhost:5000/generate-comic'
data = {'keyword': '測試API'}

try:
    response = requests.post(url, json=data)
    print(f"狀態碼: {response.status_code}")
    print(f"回應: {response.json()}")
except Exception as e:
    print(f"錯誤: {e}")

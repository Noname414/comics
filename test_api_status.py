import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if api_key:
    print("✅ API 金鑰已找到")
    print(f"金鑰前幾位: {api_key[:10]}...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content('測試連線')
        print("✅ API 連線正常")
        print(f"回應: {response.text[:50]}...")
    except Exception as e:
        print(f"❌ API 錯誤: {e}")
else:
    print("❌ 找不到 API 金鑰")

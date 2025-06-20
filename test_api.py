import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 檢查 API 金鑰
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ 錯誤：未找到 GOOGLE_API_KEY")
    sys.exit(1)

print(f"✅ API 金鑰已載入（前10字元）: {api_key[:10]}...")

# 測試 Google AI 連接
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    print("✅ Google AI 模組載入成功")
    
    # 測試文字生成
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("測試連接，請回答：連接成功")
    print(f"✅ 文字生成測試成功: {response.text[:50]}...")
    
    # 測試圖片生成模型
    image_model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ 圖片生成模型初始化成功")
    
    # 嘗試簡單圖片生成
    test_prompt = "一個簡單的紅色圓圈"
    print(f"🧪 測試圖片生成: {test_prompt}")
    
    response = image_model.generate_content([test_prompt])
    
    if response.candidates:
        print("✅ 圖片生成回應成功")
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                print("✅ 找到圖片數據")
                break
        else:
            print("⚠️  回應中沒有圖片數據")
    else:
        print("❌ 圖片生成失敗：沒有候選回應")
        
except ImportError as e:
    print(f"❌ 模組導入錯誤: {e}")
except Exception as e:
    print(f"❌ API 測試失敗: {e}")
    print(f"   錯誤類型: {type(e).__name__}")
    
print("\n測試完成！")

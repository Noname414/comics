import os
from dotenv import load_dotenv
from google import genai as google_genai
from google.genai import types

# 載入環境變數
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

print(f"API 金鑰前10字: {api_key[:10]}...")

try:
    # 使用和您原本程式相同的設定
    client = google_genai.Client(api_key=api_key)
    
    print("✅ Client 初始化成功")
    
    # 測試簡單圖片生成
    image_prompt = """
    Create a simple comic panel illustration:
    A cat sitting in a sunny garden.
    
    Style: 4-panel comic style, clean line art, cartoon style, manga-inspired.
    """
    
    print("🧪 測試圖片生成...")
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=image_prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )
    
    print("✅ API 呼叫成功")
    
    if response.candidates:
        print(f"✅ 收到 {len(response.candidates)} 個候選回應")
        
        candidate = response.candidates[0]
        if candidate.content.parts:
            print(f"✅ 收到 {len(candidate.content.parts)} 個內容部分")
            
            for i, part in enumerate(candidate.content.parts):
                if part.inline_data is not None:
                    print(f"✅ 第 {i+1} 部分包含圖片數據 ({len(part.inline_data.data)} bytes)")
                    
                    # 嘗試保存測試圖片
                    with open(f"test_image_{i+1}.raw", 'wb') as f:
                        f.write(part.inline_data.data)
                    print(f"💾 測試圖片已保存為 test_image_{i+1}.raw")
                    
                elif part.text is not None:
                    print(f"📝 第 {i+1} 部分包含文字: {part.text[:100]}...")
                else:
                    print(f"❓ 第 {i+1} 部分類型未知")
        else:
            print("❌ 候選回應中沒有內容部分")
    else:
        print("❌ 沒有收到候選回應")
        
except Exception as e:
    print(f"❌ 錯誤: {e}")
    print(f"   錯誤類型: {type(e).__name__}")
    
    # 檢查是否是 API 配額問題
    if "quota" in str(e).lower() or "limit" in str(e).lower():
        print("💡 可能是 API 配額達到限制")
    elif "permission" in str(e).lower() or "forbidden" in str(e).lower():
        print("💡 可能是 API 權限問題")
    elif "not found" in str(e).lower():
        print("💡 可能是模型名稱或 API 端點問題")
        
print("\n測試完成！")

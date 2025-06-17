import os
import google.generativeai as genai
from google import genai as google_genai
from google.genai import types
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import re
import base64
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("❌ 錯誤：找不到 GOOGLE_API_KEY 環境變數")
    print("請設定您的 Google API 金鑰：")
    print("Windows: set GOOGLE_API_KEY=your_api_key_here")
    print("或在程式中直接輸入 API 金鑰")
    
    # 提供直接輸入 API 金鑰的選項
    api_key_input = input("\n請輸入您的 Google API 金鑰 (或按 Enter 退出): ").strip()
    if not api_key_input:
        print("程式退出")
        exit(1)
    GOOGLE_API_KEY = api_key_input

genai.configure(api_key=GOOGLE_API_KEY)

# Configure GenAI client for image generation
client = google_genai.Client(api_key=GOOGLE_API_KEY)

def get_recent_news(keyword, num_articles=3):
    """Fetch recent news based on keyword using Google News."""
    url = f"https://news.google.com/rss/search?q={keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-TW"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    articles = soup.find_all('item', limit=num_articles)
    
    news_summaries = []
    for article in articles:
        title = article.title.text
        news_summaries.append(title)
    
    return news_summaries

def generate_comic_script(news_items):
    """Generate a 4-panel comic script using Gemini."""
    try:
        # List available models
        print("\n可用的模型：")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        
        # Use the fully qualified model name
        model = genai.GenerativeModel(model_name='models/gemini-2.5-flash-preview-05-20')
        
        prompt = f"""
        Based on these news items:
        {' '.join(news_items)}
        
        Create a funny 4-panel comic script in Traditional Chinese. For each panel, clearly separate:
        1. Scene setting and character actions (for visual representation)
        2. Dialogue or thoughts (for speech/thought bubbles)
        
        Format the output as:
        第一格：
        場景：[visual scene description - setting, characters, actions]
        對話：[actual dialogue in quotes, or "無" if no dialogue]
        
        第二格：
        場景：[visual scene description - setting, characters, actions]
        對話：[actual dialogue in quotes, or "無" if no dialogue]
        
        第三格：
        場景：[visual scene description - setting, characters, actions]
        對話：[actual dialogue in quotes, or "無" if no dialogue]
        
        第四格：
        場景：[visual scene description - setting, characters, actions]
        對話：[actual dialogue in quotes, or "無" if no dialogue]
        
        Make it humorous and creative while relating to the news topics.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"\n錯誤詳情: {str(e)}")
        if "not found for API version" in str(e):
            print("\n提示：請確認您的 Google API 金鑰是否正確設定，且有啟用 Gemini API 的權限。")
            print("您可以到 https://makersuite.google.com/app/apikey 檢查 API 金鑰設定。")
        raise

def parse_comic_script(script):
    """Parse the comic script into individual panels with scene and dialogue separation."""
    panels = []
    lines = script.split('\n')
    current_panel = {"scene": "", "dialogue": ""}
    panel_number = 0
    
    for line in lines:
        line = line.strip()
        if line.startswith('第') and '格：' in line:
            if panel_number > 0 and (current_panel["scene"] or current_panel["dialogue"]):
                panels.append(current_panel)
            current_panel = {"scene": "", "dialogue": ""}
            panel_number += 1
        elif line.startswith('場景：'):
            current_panel["scene"] = line.replace('場景：', '').strip()
        elif line.startswith('對話：'):
            dialogue = line.replace('對話：', '').strip()
            if dialogue != "無" and dialogue != "":
                current_panel["dialogue"] = dialogue
        elif line and not line.startswith('第'):
            # Fallback for old format - treat as scene description
            if not current_panel["scene"]:
                current_panel["scene"] = line
            else:
                current_panel["scene"] += " " + line
    
    # Add the last panel
    if panel_number > 0 and (current_panel["scene"] or current_panel["dialogue"]):
        panels.append(current_panel)
    
    return panels

def generate_comic_images(comic_script, output_folder="."):
    """Generate images for each panel of the comic."""
    try:
        # Parse the script into individual panels
        panels = parse_comic_script(comic_script)
        
        if len(panels) < 4:
            print(f"警告：只解析到 {len(panels)} 格漫畫，預期為 4 格")
        
        generated_images = []
        
        for i, panel_data in enumerate(panels[:4], 1):  # 限制為前4格
            print(f"\n正在生成第 {i} 格圖像...")
            
            # Extract scene and dialogue
            scene = panel_data.get("scene", "") if isinstance(panel_data, dict) else str(panel_data)
            dialogue = panel_data.get("dialogue", "") if isinstance(panel_data, dict) else ""
            
            print(f"📝 場景: {scene}")
            if dialogue:
                print(f"💬 對話: {dialogue}")
            
            # Create a detailed prompt for image generation
            image_prompt = f"""
            Create a comic panel illustration with this scene:
            {scene}
            
            IMPORTANT INSTRUCTIONS:
            - Show the scene, setting, and character actions visually through the artwork
            - DO NOT include scene descriptions or narrative text in the image
            - Focus on visual storytelling through character expressions, poses, and environmental details"""
            
            # Add dialogue instructions if there is dialogue
            if dialogue:
                image_prompt += f"""
            - Include this dialogue in a speech bubble: "{dialogue}"
            - Make sure the speech bubble text is clear and readable"""
            else:
                image_prompt += """
            - No speech bubbles needed - show everything visually"""
            
            image_prompt += """
            
            Style: 4-panel comic style, clean line art, cartoon style, manga-inspired, 
            suitable for newspaper comic strips. The image should be in a rectangular 
            format suitable for a comic panel. Use bright, cheerful colors and clear, 
            simple character designs. Professional comic book illustration quality.
            """
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=image_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )
                
                # Check if response has candidates
                if not response.candidates:
                    print(f"✗ 第 {i} 格沒有收到回應候選項")
                    continue
                    
                # Check if the response has content parts
                if not response.candidates[0].content.parts:
                    print(f"✗ 第 {i} 格回應中沒有內容部分")
                    continue                # Process the response
                image_saved = False
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        try:
                            # Get the image data and MIME type
                            image_data = part.inline_data.data
                            mime_type = part.inline_data.mime_type if hasattr(part.inline_data, 'mime_type') else 'unknown'
                            print(f"📊 第 {i} 格圖像數據長度: {len(image_data)} bytes")
                            print(f"📝 第 {i} 格 MIME 類型: {mime_type}")
                              # Check the first few bytes to identify format
                            if len(image_data) >= 8:
                                header = image_data[:8]
                                print(f"🔍 第 {i} 格數據頭部: {header}")
                                
                                # Check if data is base64 encoded (PNG signature in base64 starts with 'iVBORw0K')
                                if header.startswith(b'iVBORw0K'):
                                    print(f"✓ 第 {i} 格檢測到 base64 編碼的 PNG 格式")
                                elif header.startswith(b'\x89PNG'):
                                    print(f"✓ 第 {i} 格檢測到原始 PNG 格式")
                                elif header.startswith(b'\xff\xd8\xff'):
                                    print(f"✓ 第 {i} 格檢測到 JPEG 格式")
                                elif header.startswith(b'GIF'):
                                    print(f"✓ 第 {i} 格檢測到 GIF 格式")
                                elif header.startswith(b'RIFF') and len(image_data) >= 12 and image_data[8:12] == b'WEBP':
                                    print(f"✓ 第 {i} 格檢測到 WEBP 格式")
                                else:
                                    print(f"❓ 第 {i} 格未知圖像格式")
                              # Try to save raw data first for debugging
                            raw_filename = os.path.join(output_folder, f"debug_panel_{i}.raw")
                            with open(raw_filename, 'wb') as f:
                                f.write(image_data)
                            print(f"💾 第 {i} 格原始數據已保存為: {raw_filename}")
                              # Try different methods to process the image data
                            image = None
                              # Based on Google's example, the data should be used directly
                            # The issue might be that we need to handle it as binary data
                            try:
                                # Method from Google's example - direct BytesIO usage with extra parentheses
                                image = Image.open(BytesIO((image_data)))
                                print(f"✅ 第 {i} 格使用 Google 範例方法成功")
                            except Exception as e1:
                                print(f"❌ 第 {i} 格 Google 方法失敗: {str(e1)}")
                                
                                # If the data starts with base64 PNG signature, try decoding
                                try:
                                    if image_data[:8] == b'iVBORw0K':
                                        print(f"🔄 第 {i} 格嘗試 base64 解碼...")
                                        # The data is base64 encoded
                                        decoded_data = base64.b64decode(image_data)
                                        image = Image.open(BytesIO(decoded_data))
                                        print(f"✅ 第 {i} 格 base64 解碼成功")
                                    else:
                                        print(f"🔄 第 {i} 格嘗試字符串轉換...")
                                        # Try treating as string and decode
                                        if isinstance(image_data, bytes):
                                            data_str = image_data.decode('utf-8')
                                            decoded_data = base64.b64decode(data_str)
                                        else:
                                            decoded_data = base64.b64decode(image_data)
                                        image = Image.open(BytesIO(decoded_data))
                                        print(f"✅ 第 {i} 格字符串轉換成功")
                                except Exception as e2:
                                    print(f"❌ 第 {i} 格解碼失敗: {str(e2)}")
                                    
                                    # Last resort: save and try to open as file
                                    try:
                                        print(f"🔄 第 {i} 格嘗試文件方法...")
                                        temp_filename = os.path.join(output_folder, f"temp_panel_{i}.png")                                        # Try saving the raw data as PNG
                                        with open(temp_filename, 'wb') as f:
                                            if image_data[:8] == b'iVBORw0K':
                                                # Base64 decode first
                                                decoded_data = base64.b64decode(image_data)
                                                f.write(decoded_data)
                                            else:
                                                f.write(image_data)
                                        
                                        image = Image.open(temp_filename)
                                        print(f"✅ 第 {i} 格文件方法成功")
                                        
                                        # Don't remove temp file immediately, let user check it
                                        
                                    except Exception as e3:
                                        print(f"❌ 第 {i} 格所有方法都失敗: {str(e3)}")
                                        
                                        # Save debug info
                                        print(f"🔧 調試信息:")
                                        print(f"   數據類型: {type(image_data)}")
                                        print(f"   數據長度: {len(image_data)}")
                                        print(f"   前16字節: {image_data[:16]}")
                                        continue
                            
                            if image:
                                # Save the image
                                filename = os.path.join(output_folder, f"comic_panel_{i}.png")
                                image.save(filename, 'PNG')
                                generated_images.append(filename)
                                print(f"✅ 第 {i} 格圖像已儲存為: {filename}")
                                print(f"📊 目前 generated_images 列表長度: {len(generated_images)}")
                                image_saved = True
                                break
                                
                        except Exception as img_error:
                            print(f"💥 處理第 {i} 格圖像數據時發生錯誤: {str(img_error)}")
                            continue
                    elif part.text is not None:
                        print(f"📝 第 {i} 格收到文字回應: {part.text[:100]}...")
                
                if not image_saved:                    print(f"❌ 第 {i} 格未能生成或保存圖像")
                    
            except Exception as e:
                print(f"✗ 生成第 {i} 格圖像時發生錯誤: {str(e)}")
                continue        
        print(f"\n📊 圖像生成完成統計:")
        print(f"   成功生成: {len(generated_images)} 張圖像")
        print(f"   檔案列表:")
        for i, img_file in enumerate(generated_images, 1):
            print(f"     {i}. {os.path.basename(img_file)}")
        
        return generated_images
        
    except Exception as e:
        print(f"\n圖像生成錯誤: {str(e)}")
        if "quota" in str(e).lower():
            print("提示：可能已達到免費額度限制，請稍後再試。")
        elif "image generation" in str(e).lower():
            print("提示：圖像生成功能可能在您的地區不可用。")
        return []

def create_comic_collage(image_files, output_folder="."):
    """Combine the 4 panel images into a single comic strip."""
    print(f"🔍 檢查圖像檔案數量: {len(image_files)}")
    print(f"📁 圖像檔案列表:")
    for i, img_file in enumerate(image_files, 1):
        if os.path.exists(img_file):
            print(f"  ✅ {i}. {img_file}")
        else:
            print(f"  ❌ {i}. {img_file} (檔案不存在)")
    
    if len(image_files) < 4:
        print(f"❌ 圖像數量不足，目前有 {len(image_files)} 張，需要 4 張才能建立完整的四格漫畫")
        return None
    
    try:
        # Load the images
        images = [Image.open(img_file) for img_file in image_files[:4]]
        
        # Get dimensions
        width = max(img.width for img in images)
        height = max(img.height for img in images)
        
        # Create a 2x2 grid layout
        collage_width = width * 2
        collage_height = height * 2
        collage = Image.new('RGB', (collage_width, collage_height), 'white')
        
        # Arrange the images in a 2x2 grid
        positions = [(0, 0), (width, 0), (0, height), (width, height)]
        
        for i, (image, position) in enumerate(zip(images, positions)):
            # Resize image to fit the grid cell
            resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
            collage.paste(resized_image, position)
          # Save the collage
        collage_filename = os.path.join(output_folder, "four_panel_comic.png")
        collage.save(collage_filename)
        print(f"\n✓ 四格漫畫已合併儲存為: {collage_filename}")
        
        return collage_filename
        
    except Exception as e:
        print(f"建立漫畫拼貼時發生錯誤: {str(e)}")
        return None

def create_output_folder(keyword):
    """Create a folder for storing outputs based on keyword and timestamp."""
    # Clean keyword for folder name (remove invalid characters)
    clean_keyword = re.sub(r'[<>:"/\\|?*]', '_', keyword)
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create folder name
    folder_name = f"comic_output_{clean_keyword}_{timestamp}"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"📁 建立輸出資料夾: {folder_name}")
    
    return folder_name

def main():
    # Get keyword from user
    keyword = input("輸入關鍵字來搜尋相關新聞: ")
    
    # Create output folder
    output_folder = create_output_folder(keyword)
    
    # Get recent news
    print("\n正在搜尋新聞...")
    news_items = get_recent_news(keyword)
    
    if not news_items:
        print("找不到相關新聞")
        return
    
    print("\n找到的新聞:")
    for i, news in enumerate(news_items, 1):
        print(f"{i}. {news}")
      # Generate comic script
    print("\n正在生成漫畫腳本...")
    try:
        comic_script = generate_comic_script(news_items)
        print("\n四格漫畫腳本:")
        print(comic_script)
        
        # Save the script to the output folder
        script_filename = os.path.join(output_folder, "comic_script.txt")
        with open(script_filename, 'w', encoding='utf-8') as f:
            f.write("四格漫畫腳本\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"關鍵字: {keyword}\n")
            f.write(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("新聞來源:\n")
            for i, news in enumerate(news_items, 1):
                f.write(f"{i}. {news}\n")
            f.write("\n" + "=" * 50 + "\n\n")
            f.write(comic_script)
        print(f"📝 腳本已儲存為: {script_filename}")
          # Ask user if they want to generate images
        generate_images = input("\n是否要生成漫畫圖像？(y/n): ").lower().strip()
        
        if generate_images in ['y', 'yes', '是', '好']:
            print("\n開始生成四格漫畫圖像...")
            image_files = generate_comic_images(comic_script, output_folder)
            
            # Double-check for actually existing files
            existing_image_files = []
            for i in range(1, 5):  # Check for panels 1-4
                panel_file = os.path.join(output_folder, f"comic_panel_{i}.png")
                if os.path.exists(panel_file):
                    existing_image_files.append(panel_file)
            
            print(f"\n✓ 實際檢查發現 {len(existing_image_files)} 張圖像檔案")
            
            if len(existing_image_files) >= 4:
                print("🎯 找到完整的4張圖像，繼續建立拼貼...")
                # Create a collage of all panels
                collage_file = create_comic_collage(existing_image_files, output_folder)
                
                if collage_file:
                    print(f"\n🎉 四格漫畫製作完成！")
                    print(f"📁 所有檔案儲存在: {output_folder}")
                    print(f"個別圖像檔案: {', '.join([os.path.basename(f) for f in existing_image_files])}")
                    print(f"完整四格漫畫: {os.path.basename(collage_file)}")
                else:
                    print(f"\n📁 所有檔案儲存在: {output_folder}")
                    print(f"個別圖像檔案: {', '.join([os.path.basename(f) for f in existing_image_files])}")
            elif len(existing_image_files) > 0:
                print(f"⚠️ 只找到 {len(existing_image_files)} 張圖像，無法建立完整的四格漫畫")
                print(f"📁 已生成的檔案儲存在: {output_folder}")
                print(f"可用圖像檔案: {', '.join([os.path.basename(f) for f in existing_image_files])}")
            else:
                print("\n❌ 無法生成圖像，請檢查 API 設定和網路連線")
        else:
            print("\n腳本生成完成！")
            
    except Exception as e:
        print(f"生成腳本時發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()

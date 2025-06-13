import os
import google.generativeai as genai
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

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
        # List available models        print("\n可用的模型：")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")        # Use the fully qualified model name
        model = genai.GenerativeModel(model_name='models/gemini-2.0-flash')
        
        prompt = f"""
        Based on these news items:
        {' '.join(news_items)}
        
        Create a funny 4-panel comic script in Chinese. For each panel, describe:
        1. The scene setting
        2. Character actions
        3. Dialogue (if any)
        
        Format the output as:
        第一格：
        [description]
        
        第二格：
        [description]
        
        第三格：
        [description]
        
        第四格：
        [description]
        
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

def main():
    # Get keyword from user
    keyword = input("輸入關鍵字來搜尋相關新聞: ")
    
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
    except Exception as e:
        print(f"生成腳本時發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()

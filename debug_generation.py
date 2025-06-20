import subprocess
import sys

print("🧪 測試漫畫生成器...")

# 模擬網頁 API 的方式呼叫 comic_generator.py
process = subprocess.Popen(
    [sys.executable, 'comic_generator.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8',
    errors='replace',  # 改為 replace 而不是 ignore
    cwd='.'
)

# 發送測試關鍵字
keyword = "測試"
print(f"📝 發送關鍵字: {keyword}")

stdout, stderr = process.communicate(input=keyword + '\n', timeout=300)

print(f"\n📊 返回碼: {process.returncode}")
print(f"📝 標準輸出:")
print(stdout if stdout else "(無)")
print(f"❌ 錯誤輸出:")
print(stderr if stderr else "(無)")

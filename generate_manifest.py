import os
import json
import re
import sys
from datetime import datetime

# 設定輸出編碼為 UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def scan_comic_outputs():
    """掃描 docs 目錄下的所有漫畫輸出資料夾，生成漫畫清單"""
    comics_list = []
    docs_dir = 'docs'
    
    if not os.path.exists(docs_dir):
        print(f"目錄 {docs_dir} 不存在")
        return comics_list
    
    # 尋找所有 comic_output_ 開頭的資料夾
    for item in os.listdir(docs_dir):
        item_path = os.path.join(docs_dir, item)
        
        if os.path.isdir(item_path) and item.startswith('comic_output_'):
            try:
                # 解析資料夾名稱
                # 格式: comic_output_{keyword}_{timestamp}
                parts = item.split('_')
                if len(parts) >= 4:
                    # 提取關鍵字和時間戳
                    keyword_parts = parts[2:-2] if len(parts) > 4 else [parts[2]]
                    keyword = '_'.join(keyword_parts)
                    timestamp = '_'.join(parts[-2:])
                      # 檢查是否有四格漫畫圖片或腳本
                    collage_path = os.path.join(item_path, 'four_panel_comic.png')
                    script_path = os.path.join(item_path, 'comic_script.txt')
                    
                    # 如果有圖片或腳本檔案，就包含這個漫畫
                    if os.path.exists(collage_path) or os.path.exists(script_path):
                        # 解析時間戳
                        try:
                            date_obj = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
                            formatted_date = date_obj.strftime('%Y年%m月%d日 %H:%M')
                        except:
                            formatted_date = timestamp
                          # 讀取腳本內容獲取更多信息
                        title = keyword
                        if os.path.exists(script_path):
                            try:
                                with open(script_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    # 嘗試提取第一個面板的標題作為漫畫標題
                                    lines = content.split('\n')
                                    for line in lines:
                                        if '面板 1:' in line or '第一格:' in line:
                                            # 提取描述作為標題
                                            title_match = re.search(r'面板 1[:：]\s*(.+)', line)
                                            if title_match:
                                                title = title_match.group(1)[:50] + '...' if len(title_match.group(1)) > 50 else title_match.group(1)
                                            break
                            except:
                                pass
                        
                        comic_info = {
                            'id': item,
                            'title': title,
                            'keyword': keyword,
                            'date': formatted_date,
                            'timestamp': timestamp,
                            'imagePath': f'{item}/four_panel_comic.png' if os.path.exists(collage_path) else None,
                            'scriptPath': f'{item}/comic_script.txt' if os.path.exists(script_path) else None,
                            'folder': item,
                            'hasImage': os.path.exists(collage_path),
                            'hasScript': os.path.exists(script_path)
                        }
                        
                        comics_list.append(comic_info)
                        print(f"找到漫畫: {keyword} - {formatted_date}")
                        
            except Exception as e:
                print(f"處理資料夾 {item} 時發生錯誤: {e}")
                continue
    
    # 按時間戳排序 (最新的在前面)
    comics_list.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return comics_list

def generate_comics_manifest():
    """生成漫畫清單的 JSON 文件"""
    comics = scan_comic_outputs()
    
    manifest = {
        'lastUpdated': datetime.now().isoformat(),
        'totalComics': len(comics),
        'comics': comics
    }
    
    # 儲存到 docs 目錄
    manifest_path = os.path.join('docs', 'comics_manifest.json')
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 漫畫清單已生成: {manifest_path}")
    print(f"📊 總共找到 {len(comics)} 個漫畫作品")
    
    return manifest_path

if __name__ == "__main__":
    generate_comics_manifest()

import os
import json
import re
import sys
from datetime import datetime

# 設定輸出編碼為 UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def safe_print(message):
    """安全的 print 函數，處理編碼問題"""
    try:
        print(message)
    except UnicodeEncodeError:
        # 使用安全的字串處理
        safe_message = str(message).encode('utf-8', errors='replace').decode('utf-8')
        print(safe_message)

def scan_comic_outputs():
    """掃描 docs 目錄下的所有漫畫輸出資料夾，生成漫畫清單"""
    comics_list = []
    docs_dir = 'docs'
    
    if not os.path.exists(docs_dir):
        safe_print(f"目錄 {docs_dir} 不存在")
        return comics_list
    
    # 尋找所有 comic_output_ 開頭的資料夾
    try:
        dir_items = os.listdir(docs_dir)
    except Exception as e:
        safe_print(f"無法讀取目錄 {docs_dir}: {e}")
        return comics_list
    
    for item in dir_items:
        # 先檢查檔案名稱是否包含有問題的字元
        try:
            # 嘗試安全處理檔案名稱
            if isinstance(item, bytes):
                # 如果是 bytes，嘗試解碼
                safe_item = item.decode('utf-8', errors='replace')
            else:
                # 如果是字串，確保編碼正確
                safe_item = str(item).encode('utf-8', errors='replace').decode('utf-8')
            
            # 檢查是否包含替換字元，如果有就跳過
            if '\ufffd' in safe_item or '\\udc' in repr(item):
                safe_print(f"跳過有編碼問題的檔案: {repr(item)}")
                continue
                
        except Exception as e:
            # 跳過任何處理失敗的檔案
            safe_print(f"跳過處理失敗的檔案: {repr(item)} (錯誤: {e})")
            continue
            
        # 使用安全的檔案名稱進行後續處理
        item_path = os.path.join(docs_dir, item)
        
        if os.path.isdir(item_path) and safe_item.startswith('comic_output_'):
            try:
                # 解析資料夾名稱 (使用安全的檔案名稱)
                # 格式: comic_output_{keyword}_{timestamp}
                parts = safe_item.split('_')
                if len(parts) >= 4:
                    # 提取關鍵字和時間戳
                    keyword_parts = parts[2:-2] if len(parts) > 4 else [parts[2]]
                    keyword = '_'.join(keyword_parts)
                    timestamp = '_'.join(parts[-2:])
                      # 檢查是否有四格漫畫圖片或腳本
                    collage_path = os.path.join(item_path, 'four_panel_comic.png')
                    script_path = os.path.join(item_path, 'comic_script.txt')
                    
                    # 只包含有完整四格漫畫圖片的漫畫（可以修改為 "or" 來包含只有腳本的）
                    if os.path.exists(collage_path):
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
                            'id': safe_item,  # 使用安全的檔案名稱
                            'title': title,
                            'keyword': keyword,
                            'date': formatted_date,
                            'timestamp': timestamp,
                            'imagePath': f'{safe_item}/four_panel_comic.png' if os.path.exists(collage_path) else None,
                            'scriptPath': f'{safe_item}/comic_script.txt' if os.path.exists(script_path) else None,
                            'folder': safe_item,
                            'hasImage': os.path.exists(collage_path),
                            'hasScript': os.path.exists(script_path)
                        }
                        
                        comics_list.append(comic_info)
                        safe_print(f"找到漫畫: {keyword} - {formatted_date}")
                        
            except Exception as e:
                safe_print(f"處理資料夾 {safe_item} 時發生錯誤: {e}")
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
    
    safe_print(f"\n✅ 漫畫清單已生成: {manifest_path}")
    safe_print(f"📊 總共找到 {len(comics)} 個漫畫作品")
    
    return manifest_path

if __name__ == "__main__":
    generate_comics_manifest()

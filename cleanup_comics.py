#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理沒有圖片的漫畫資料夾和條目
Clean up comic folders and entries that don't have images
"""

import os
import json
import shutil
from datetime import datetime

def scan_and_cleanup():
    """掃描並清理沒有圖片的漫畫資料夾"""
    docs_dir = 'docs'
    if not os.path.exists(docs_dir):
        print(f"目錄 {docs_dir} 不存在")
        return
    
    removed_folders = []
    kept_folders = []
    
    # 掃描所有 comic_output_ 資料夾
    for item in os.listdir(docs_dir):
        if item.startswith('comic_output_'):
            folder_path = os.path.join(docs_dir, item)
            if os.path.isdir(folder_path):
                # 檢查是否有四格漫畫圖片
                four_panel_comic = os.path.join(folder_path, 'four_panel_comic.png')
                
                if not os.path.exists(four_panel_comic):
                    # 沒有完整的四格漫畫，詢問是否刪除
                    script_file = os.path.join(folder_path, 'comic_script.txt')
                    has_script = os.path.exists(script_file)
                    
                    print(f"\n📁 資料夾: {item}")
                    print(f"   🖼️  四格漫畫: ❌ 沒有")
                    print(f"   📝 腳本文件: {'✅ 有' if has_script else '❌ 沒有'}")
                    
                    choice = input(f"   是否刪除此資料夾？(y/n): ").lower().strip()
                    
                    if choice in ['y', 'yes', '是']:
                        try:
                            shutil.rmtree(folder_path)
                            removed_folders.append(item)
                            print(f"   ✅ 已刪除資料夾: {item}")
                        except Exception as e:
                            print(f"   ❌ 刪除失敗: {e}")
                    else:
                        kept_folders.append(item)
                        print(f"   ⏭️  保留資料夾: {item}")
                else:
                    kept_folders.append(item)
    
    # 顯示結果
    print(f"\n📊 清理結果:")
    print(f"   🗑️  已刪除: {len(removed_folders)} 個資料夾")
    for folder in removed_folders:
        print(f"      - {folder}")
    
    print(f"   📁 保留: {len(kept_folders)} 個資料夾")
    
    if removed_folders:
        # 重新生成 manifest
        print(f"\n🔄 重新生成漫畫清單...")
        try:
            import generate_manifest
            generate_manifest.generate_comics_manifest()
            print(f"✅ 漫畫清單已更新")
        except Exception as e:
            print(f"❌ 更新清單失敗: {e}")
            print(f"請手動執行: python generate_manifest.py")

def auto_cleanup():
    """自動清理所有沒有圖片的資料夾（不詢問）"""
    docs_dir = 'docs'
    if not os.path.exists(docs_dir):
        print(f"目錄 {docs_dir} 不存在")
        return
    
    removed_folders = []
    
    # 掃描所有 comic_output_ 資料夾
    for item in os.listdir(docs_dir):
        if item.startswith('comic_output_'):
            folder_path = os.path.join(docs_dir, item)
            if os.path.isdir(folder_path):
                # 檢查是否有四格漫畫圖片
                four_panel_comic = os.path.join(folder_path, 'four_panel_comic.png')
                
                if not os.path.exists(four_panel_comic):
                    try:
                        shutil.rmtree(folder_path)
                        removed_folders.append(item)
                        print(f"🗑️  已刪除: {item}")
                    except Exception as e:
                        print(f"❌ 刪除失敗 {item}: {e}")
    
    if removed_folders:
        print(f"\n📊 自動清理完成，共刪除 {len(removed_folders)} 個資料夾")
        
        # 重新生成 manifest
        print(f"🔄 重新生成漫畫清單...")
        try:
            import generate_manifest
            generate_manifest.generate_comics_manifest()
            print(f"✅ 漫畫清單已更新")
        except Exception as e:
            print(f"❌ 更新清單失敗: {e}")
    else:
        print(f"✅ 沒有需要清理的資料夾")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'auto':
        print("🤖 自動清理模式")
        auto_cleanup()
    else:
        print("🧹 互動式清理模式")
        print("📝 這個腳本會幫您清理沒有完整四格漫畫圖片的資料夾")
        print("   (保留有完整 four_panel_comic.png 的資料夾)")
        print()
        scan_and_cleanup()

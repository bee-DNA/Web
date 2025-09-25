#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 互動式城市人口地圖系統測試腳本
"""

import os
import sys
import webbrowser
from pathlib import Path

def test_interactive_city_map():
    """測試互動式城市地圖系統"""
    print("🔍 互動式城市人口地圖系統測試")
    print("=" * 50)
    
    # 檢查主要檔案
    required_files = [
        "interactive_city_map.html",
        "start_city_map.bat", 
        "start_city_map_simple.ps1",
        "INTERACTIVE_CITY_MAP_GUIDE.md"
    ]
    
    print("\n📂 檔案完整性檢查:")
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            all_files_exist = False
    
    # 檢查 HTML 檔案內容
    print("\n🧪 功能測試:")
    try:
        with open("interactive_city_map.html", 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 檢查關鍵功能
        features = {
            "Mapbox GL JS": "mapboxgl.accessToken" in content,
            "城市資料": "CITY_DATA" in content and "population" in content,
            "動畫效果": "@keyframes" in content and "animation:" in content,
            "響應式設計": "@media" in content,
            "多語言支援": "name_zh" in content and "name_en" in content,
            "統計功能": "updateStats" in content,
            "互動功能": "onCityClick" in content
        }
        
        for feature, exists in features.items():
            status = "✅" if exists else "❌"
            print(f"  {status} {feature}")
            
    except Exception as e:
        print(f"  ❌ HTML 檔案讀取失敗: {e}")
        all_files_exist = False
    
    # 系統建議
    print(f"\n📊 測試摘要:")
    print(f"  檔案完整性: {'✅ 通過' if all_files_exist else '❌ 失敗'}")
    
    if all_files_exist:
        print(f"  系統狀態: 🟢 就緒")
        print(f"\n🚀 啟動建議:")
        print(f"  1. 雙擊開啟: interactive_city_map.html")
        print(f"  2. PowerShell: Invoke-Item 'interactive_city_map.html'")
        print(f"  3. 或執行: start_city_map_simple.ps1")
        
        print(f"\n🌟 系統特色:")
        print(f"  📍 全球 25 個主要城市人口資料")
        print(f"  🎨 5 種地圖樣式 (街道/衛星/簡約/暗色/戶外)")
        print(f"  🌐 中英文雙語切換")
        print(f"  📊 即時統計資訊")
        print(f"  🎬 豐富動畫效果")
        print(f"  📱 響應式設計")
        
    else:
        print(f"  系統狀態: 🔴 需要修復")
    
    return all_files_exist

def open_interactive_map():
    """開啟互動式地圖"""
    html_path = Path("interactive_city_map.html").absolute()
    if html_path.exists():
        print(f"🌍 開啟互動式城市人口地圖: {html_path}")
        webbrowser.open(f"file://{html_path}")
        return True
    else:
        print("❌ 找不到 interactive_city_map.html")
        return False

def show_help():
    """顯示使用說明"""
    print("""
🌍 互動式城市人口地圖系統使用指南

📋 可用命令:
  python test_city_map.py test     - 系統完整性測試
  python test_city_map.py open    - 開啟互動地圖
  python test_city_map.py help    - 顯示此說明

🚀 快速啟動方式:
  1. 雙擊開啟: interactive_city_map.html
  2. PowerShell: Invoke-Item "interactive_city_map.html"
  3. 執行腳本: python test_city_map.py open

🌟 主要功能:
  • 📍 全球 25 個主要城市人口資料視覺化
  • 🎨 5 種地圖樣式切換 (街道/衛星/簡約/暗色/戶外)
  • 🌐 中英文雙語城市名稱顯示
  • 📊 即時統計 - 城市數量、總人口、平均人口、最大城市
  • 🎯 點擊城市查看詳細人口資訊
  • 🔍 區域快速跳轉 (亞洲/歐洲/美洲/非洲/大洋洲)
  • 🎬 豐富動畫效果 - 載入動畫、懸停效果、彈窗動畫
  • 📱 響應式設計 - 支援各種螢幕尺寸

🎛️ 控制功能:
  • 地圖樣式切換
  • 語言切換 (中/英)
  • 點樣式模式 (按人口調整/統一大小)
  • 重置視圖
  • 全螢幕模式

💡 使用技巧:
  • 點擊城市圓點查看詳細資訊
  • 使用右側按鈕快速跳轉到各大洲
  • 滾輪縮放，拖拽移動地圖
  • 左側控制面板調整設定
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            test_interactive_city_map()
        elif command == "open":
            if not open_interactive_map():
                sys.exit(1)
        elif command == "help":
            show_help()
        else:
            print(f"❌ 未知命令: {command}")
            show_help()
    else:
        print("🌍 互動式城市人口地圖系統")
        print("執行 'python test_city_map.py help' 查看使用說明")
        test_interactive_city_map()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌍 全球天氣地圖系統測試腳本
測試各個組件的功能性
"""

import os
import sys
import json
import webbrowser
from pathlib import Path


def test_system():
    """測試系統完整性"""
    print("🔍 全球天氣地圖系統測試")
    print("=" * 50)

    # 檢查必要檔案
    required_files = [
        "global_weather_map.html",
        "global_weather_map_server.py",
        "weather_map_config.py",
        "start_weather_map.bat",
        "start_weather_map.ps1",
    ]

    print("\n📂 檔案完整性檢查:")
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            all_files_exist = False

    # 檢查配置檔案
    print("\n🔧 配置檔案檢查:")
    try:
        import weather_map_config as config

        if hasattr(config, "API_KEYS"):
            print("  ✅ API_KEYS 配置存在")
            if "openweather" in config.API_KEYS:
                print(
                    f"  ✅ OpenWeather API 金鑰: {config.API_KEYS['openweather'][:10]}..."
                )
            else:
                print("  ❌ OpenWeather API 金鑰未設定")
        else:
            print("  ❌ API_KEYS 配置缺失")
    except ImportError:
        print("  ❌ 無法載入 weather_map_config.py")

    # 檢查 Python 套件
    print("\n📦 Python 套件檢查:")
    required_packages = ["flask", "flask_cors", "requests", "pandas"]

    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (未安裝)")

    # 系統功能測試
    print("\n🧪 功能測試:")

    # 測試 HTML 檔案可讀性
    try:
        with open("global_weather_map.html", "r", encoding="utf-8") as f:
            content = f.read()
            if "mapboxgl.accessToken" in content:
                print("  ✅ HTML 檔案包含 Mapbox 配置")
            if "OpenWeather API" in content:
                print("  ✅ HTML 檔案包含天氣 API 整合")
    except Exception as e:
        print(f"  ❌ HTML 檔案讀取失敗: {e}")

    print("\n🎯 測試建議:")
    if all_files_exist:
        print("  1. 執行 start_weather_map.bat (Windows)")
        print("  2. 或直接開啟 global_weather_map.html")
        print("  3. 檢查瀏覽器是否正常顯示地圖")
    else:
        print("  ❌ 系統檔案不完整，請重新安裝")

    print(f"\n📊 測試摘要:")
    print(f"  檔案完整性: {'✅ 通過' if all_files_exist else '❌ 失敗'}")
    print(f"  系統狀態: {'🟢 就緒' if all_files_exist else '🔴 需要修復'}")


def open_weather_map():
    """開啟天氣地圖"""
    html_path = Path("global_weather_map.html").absolute()
    if html_path.exists():
        print(f"🌍 開啟天氣地圖: {html_path}")
        webbrowser.open(f"file://{html_path}")
        return True
    else:
        print("❌ 找不到 global_weather_map.html")
        return False


def show_help():
    """顯示使用說明"""
    print(
        """
🌍 全球天氣地圖系統使用指南

📋 可用命令:
  python test_system.py test     - 系統完整性測試
  python test_system.py open    - 開啟天氣地圖
  python test_system.py help    - 顯示此說明

🚀 快速啟動方式:
  1. Windows: 執行 start_weather_map.bat
  2. PowerShell: .\start_weather_map.ps1  
  3. 直接開啟: global_weather_map.html
  4. Python 服務: python global_weather_map_server.py

🌟 主要功能:
  • 全球 16 個主要城市即時天氣
  • 溫度、濕度、風速、氣壓監測
  • 雲圖和降雨圖層
  • 衛星影像切換
  • 3D 視角和全螢幕模式
  • 每 2 小時自動更新

🔧 故障排除:
  如果遇到問題，請先運行測試: python test_system.py test
    """
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "test":
            test_system()
        elif command == "open":
            if not open_weather_map():
                sys.exit(1)
        elif command == "help":
            show_help()
        else:
            print(f"❌ 未知命令: {command}")
            show_help()
    else:
        print("🌍 全球天氣地圖系統")
        print("執行 'python test_system.py help' 查看使用說明")
        test_system()

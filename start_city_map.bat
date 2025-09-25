@echo off
chcp 65001 >nul 2>&1
echo =====================================
echo 互動式城市人口地圖系統啟動器
echo =====================================
echo.

echo 正在開啟互動式城市地圖...
echo.
echo 系統功能：
echo    * 全球 25 個主要城市人口資料
echo    * 多種地圖樣式切換 (街道/衛星/暗色等)
echo    * 中英文語言切換
echo    * 即時統計資訊顯示
echo    * 點擊城市查看詳細人口
echo    * 區域快速跳轉功能
echo    * 響應式設計支援
echo.
echo 使用說明：
echo    - 點擊城市圓點查看人口資訊
echo    - 使用右側按鈕跳轉到各大洲
echo    - 左側面板控制地圖樣式和語言
echo    - 滾輪縮放，拖拽移動地圖
echo.

REM 檢查檔案是否存在
if not exist "interactive_city_map.html" (
    echo ❌ 錯誤：找不到 interactive_city_map.html 檔案
    echo 請確認檔案存在於當前目錄
    pause
    exit /b 1
)

echo 🚀 正在開啟地圖...
start "" "interactive_city_map.html"

echo.
echo 互動式城市人口地圖已在瀏覽器中開啟！
echo.
echo 特色功能：
echo    * 全新動畫效果 - 載入動畫、懸停效果、彈窗動畫
echo    * 即時統計 - 城市數量、總人口、平均人口、最大城市
echo    * 靈活控制 - 樣式切換、語言切換、點大小模式
echo    * 多樣化地圖 - 街道、衛星、簡約、暗色、戶外地圖
echo    * 響應式設計 - 支援各種螢幕尺寸
echo.
echo 提示：如果地圖沒有正確顯示，請檢查網路連線
echo.

set /p dummy="按 Enter 鍵退出..."
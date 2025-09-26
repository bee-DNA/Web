@echo off
echo 正在啟動 3D 互動城市地圖...

cd /d "D:\OneDrive\學校上課\課程\四上\科學大數據專題"

if not exist "interactive_city_map_enhanced.html" (
    echo 錯誤: 找不到 interactive_city_map_enhanced.html
    pause
    exit /b 1
)

echo 啟動 HTTP 服務器於端口 8086...
python -m http.server 8086

if errorlevel 1 (
    echo Python 服務器啟動失敗，直接開啟檔案...
    start "" "interactive_city_map_enhanced.html"
    pause
)
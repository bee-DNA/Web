@echo off
echo ================================================
echo        互動式城市人口地圖系統
echo ================================================

cd /d "D:\OneDrive\學校上課\課程\四上\科學大數據專題"

echo 正在啟動後端服務器 (端口 8086)...
start "互動城市地圖後端" cmd /c "echo 後端服務器正在運行於 http://localhost:8086 && python -m http.server 8086 && pause"

echo 等待服務器啟動...
timeout /t 3 /nobreak >nul

echo 正在開啟互動式城市人口地圖...
start "" "http://localhost:8086/interactive_city_map_enhanced.html"

echo.
echo ================================================
echo 系統啟動完成！
echo 地圖: http://localhost:8086/interactive_city_map_enhanced.html
echo 後端: HTTP 服務器運行於端口 8086
echo ================================================
echo.
echo 按任意鍵關閉此視窗...
pause >nul
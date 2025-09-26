@echo off
echo ================================================
echo        啟動虛擬環境 3D 互動城市地圖系統
echo ================================================

cd /d "D:\OneDrive\學校上課\課程\四上\科學大數據專題"

echo 正在激活虛擬環境...
call .\venv\Scripts\activate.bat

echo.
echo 檢查虛擬環境狀態...
python --version
echo 虛擬環境已激活: %VIRTUAL_ENV%

echo.
echo 正在啟動後端 HTTP 服務器 (端口 8086)...
start "後端服務器" cmd /c "echo 後端服務器正在運行於 http://localhost:8086 && python -m http.server 8086 && pause"

echo 等待後端服務器啟動...
timeout /t 3 /nobreak >nul

echo.
echo 正在開啟前端地圖...
start "" "http://localhost:8086/interactive_city_map_enhanced.html"

echo.
echo ================================================
echo 系統啟動完成！
echo 前端: http://localhost:8086/interactive_city_map_enhanced.html
echo 後端: HTTP 服務器運行於端口 8086
echo ================================================
echo.
echo 按任意鍵關閉此視窗...
pause >nul
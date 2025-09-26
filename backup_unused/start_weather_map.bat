@echo off
echo =====================================
echo 🌍 全球天氣地圖系統啟動器
echo =====================================
echo.

REM 檢查是否有 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤：未找到 Python，請先安裝 Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python 檢查通過

REM 創建虛擬環境（如果不存在）
if not exist "venv" (
    echo 🔧 創建虛擬環境...
    python -m venv venv
)

REM 啟動虛擬環境
echo 🚀 啟動虛擬環境...
call venv\Scripts\activate.bat

REM 安裝依賴
echo 📦 檢查並安裝依賴套件...
pip install flask flask-cors requests pandas numpy

echo.
echo =====================================
echo 🌐 可用的服務選項：
echo =====================================
echo [1] 啟動 Flask 後端服務器 (端口 5001)
echo [2] 開啟獨立 HTML 天氣地圖 (推薦)
echo [3] 啟動 Mapbox API 服務器 (端口 5000)
echo [4] 退出
echo.

set /p choice="請選擇 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 啟動 Flask 後端服務器...
    echo 📍 網址: http://localhost:5001
    echo 🗺️ 全球地圖: http://localhost:5001/map/global
    echo 💡 按 Ctrl+C 停止服務器
    echo.
    python global_weather_map_server.py
) else if "%choice%"=="2" (
    echo.
    echo 🌍 開啟全球天氣地圖 HTML...
    echo 💡 這將在您的預設瀏覽器中開啟天氣地圖
    echo 📊 包含即時天氣、雲圖、衛星影像等功能
    echo.
    start "" "global_weather_map.html"
    echo ✅ 地圖已在瀏覽器中開啟！
) else if "%choice%"=="3" (
    echo.
    echo 🗺️ 啟動 Mapbox API 服務器...
    echo 📍 網址: http://localhost:5000
    echo 🌊 互動地圖: http://localhost:5000/map
    echo 💡 按 Ctrl+C 停止服務器
    echo.
    python mapbox_api_server.py
) else if "%choice%"=="4" (
    echo 👋 再見！
    exit /b 0
) else (
    echo ❌ 無效選擇，請重新執行腳本
)

echo.
echo ✨ 感謝使用全球天氣地圖系統！
pause
@echo off
echo =====================================
echo 🌍 整合世界地圖 & 天氣系統啟動器
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
echo 📦 安裝必要套件...
pip install dash plotly pandas requests numpy

echo.
echo =====================================
echo 🌐 整合世界地圖系統功能：
echo =====================================
echo 📊 模式一：世界國家統計資料
echo    • 人口分布地圖
echo    • GDP 分布地圖
echo    • 互動資料表
echo.
echo 🌦️ 模式二：全球天氣監測
echo    • 18個主要城市即時天氣
echo    • 溫度、濕度、風速、雲量
echo    • 地區篩選功能
echo    • 自動每2小時更新
echo.

set /p confirm="按 Enter 啟動整合系統..."

echo 🚀 啟動整合世界地圖應用...
echo 📍 網址: http://localhost:8050
echo 💡 功能切換: 使用網頁上方的模式選擇器
echo 🔄 天氣更新: 點擊「手動更新天氣」按鈕
echo 🌏 地區篩選: 選擇不同地區查看天氣
echo.
echo 💡 按 Ctrl+C 停止服務器
echo.

python integrated_world_weather_map.py

echo.
echo ✨ 感謝使用整合世界地圖系統！
pause
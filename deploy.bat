@echo off
echo 🐳 世界地圖專案 Docker 部署腳本
echo ==================================

REM 檢查 Docker 是否安裝
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker 未安裝，請先安裝 Docker Desktop
    pause
    exit /b 1
)

REM 檢查 Docker Compose 是否安裝  
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose 未安裝，請先安裝 Docker Compose
    pause
    exit /b 1
)

echo ✅ Docker 環境檢查完成
echo.

echo 請選擇部署模式：
echo 1^) 基本版 ^(端口 8050^)
echo 2^) 進階版 ^(端口 8051^)
echo 3^) 兩個版本都部署

set /p choice=輸入選項 (1-3): 

if "%choice%"=="1" (
    echo 🚀 部署基本版世界地圖應用...
    docker-compose up --build world-map-app
) else if "%choice%"=="2" (
    echo 🚀 部署進階版世界地圖應用...
    docker-compose --profile advanced up --build advanced-world-map-app
) else if "%choice%"=="3" (
    echo 🚀 部署所有應用...
    docker-compose --profile advanced up --build
) else (
    echo ❌ 無效選項
    pause
    exit /b 1
)

echo.
echo 🎉 部署完成！
echo 📍 基本版: http://localhost:8050
echo 📍 進階版: http://localhost:8051
pause
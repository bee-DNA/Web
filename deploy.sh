#!/bin/bash
# Docker 部署腳本

echo "🐳 世界地圖專案 Docker 部署腳本"
echo "=================================="

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安裝，請先安裝 Docker"
    exit 1
fi

# 檢查 Docker Compose 是否安裝
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安裝，請先安裝 Docker Compose"
    exit 1
fi

echo "✅ Docker 環境檢查完成"

# 選擇部署模式
echo ""
echo "請選擇部署模式："
echo "1) 基本版 (端口 8050)"
echo "2) 進階版 (端口 8051)"  
echo "3) 兩個版本都部署"

read -p "輸入選項 (1-3): " choice

case $choice in
    1)
        echo "🚀 部署基本版世界地圖應用..."
        docker-compose up --build world-map-app
        ;;
    2)
        echo "🚀 部署進階版世界地圖應用..."
        docker-compose --profile advanced up --build advanced-world-map-app
        ;;
    3)
        echo "🚀 部署所有應用..."
        docker-compose --profile advanced up --build
        ;;
    *)
        echo "❌ 無效選項"
        exit 1
        ;;
esac

echo ""
echo "🎉 部署完成！"
echo "📍 基本版: http://localhost:8050"
echo "📍 進階版: http://localhost:8051"
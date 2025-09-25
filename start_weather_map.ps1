# 全球天氣地圖系統 PowerShell 啟動器
# 執行策略：Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🌍 全球天氣地圖系統啟動器" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Python
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python 檢查通過: $pythonVersion" -ForegroundColor Green
    }
    else {
        throw "Python not found"
    }
}
catch {
    Write-Host "❌ 錯誤：未找到 Python，請先安裝 Python 3.7+" -ForegroundColor Red
    Read-Host "按 Enter 鍵退出"
    exit 1
}

# 創建虛擬環境
if (-not (Test-Path "venv")) {
    Write-Host "🔧 創建虛擬環境..." -ForegroundColor Yellow
    python -m venv venv
}

# 啟動虛擬環境
Write-Host "🚀 啟動虛擬環境..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# 安裝依賴
Write-Host "📦 檢查並安裝依賴套件..." -ForegroundColor Yellow
pip install flask flask-cors requests pandas numpy | Out-Host

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🌐 可用的服務選項：" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "[1] 啟動 Flask 後端服務器 (端口 5001)" -ForegroundColor White
Write-Host "[2] 開啟獨立 HTML 天氣地圖 (推薦)" -ForegroundColor Green
Write-Host "[3] 啟動 Mapbox API 服務器 (端口 5000)" -ForegroundColor White
Write-Host "[4] 檢查系統狀態" -ForegroundColor Cyan
Write-Host "[5] 退出" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "請選擇 (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 啟動 Flask 後端服務器..." -ForegroundColor Green
        Write-Host "📍 網址: http://localhost:5001" -ForegroundColor Cyan
        Write-Host "🗺️ 全球地圖: http://localhost:5001/map/global" -ForegroundColor Cyan
        Write-Host "💡 按 Ctrl+C 停止服務器" -ForegroundColor Yellow
        Write-Host ""
        python global_weather_map_server.py
    }
    "2" {
        Write-Host ""
        Write-Host "🌍 開啟全球天氣地圖 HTML..." -ForegroundColor Green
        Write-Host "💡 這將在您的預設瀏覽器中開啟天氣地圖" -ForegroundColor Yellow
        Write-Host "📊 包含即時天氣、雲圖、衛星影像等功能" -ForegroundColor Cyan
        Write-Host ""
        
        $htmlPath = Join-Path (Get-Location) "global_weather_map.html"
        Start-Process $htmlPath
        
        Write-Host "✅ 地圖已在瀏覽器中開啟！" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔧 功能說明：" -ForegroundColor Yellow
        Write-Host "• 全球 16 個主要城市即時天氣" -ForegroundColor White
        Write-Host "• 溫度、濕度、風速、氣壓監測" -ForegroundColor White
        Write-Host "• 雲圖和降雨圖層" -ForegroundColor White
        Write-Host "• 衛星影像切換" -ForegroundColor White
        Write-Host "• 地區篩選 (亞洲、歐洲、美洲等)" -ForegroundColor White
        Write-Host "• 3D 視角切換" -ForegroundColor White
        Write-Host "• 每 2 小時自動更新" -ForegroundColor White
    }
    "3" {
        Write-Host ""
        Write-Host "🗺️ 啟動 Mapbox API 服務器..." -ForegroundColor Green
        Write-Host "📍 網址: http://localhost:5000" -ForegroundColor Cyan
        Write-Host "🌊 互動地圖: http://localhost:5000/map" -ForegroundColor Cyan
        Write-Host "💡 按 Ctrl+C 停止服務器" -ForegroundColor Yellow
        Write-Host ""
        python mapbox_api_server.py
    }
    "4" {
        Write-Host ""
        Write-Host "🔍 系統狀態檢查..." -ForegroundColor Yellow
        Write-Host ""
        
        # 檢查檔案
        $files = @(
            "global_weather_map.html",
            "global_weather_map_server.py", 
            "weather_map_config.py",
            "mapbox_api_server.py"
        )
        
        foreach ($file in $files) {
            if (Test-Path $file) {
                Write-Host "✅ $file" -ForegroundColor Green
            }
            else {
                Write-Host "❌ $file (缺失)" -ForegroundColor Red
            }
        }
        
        Write-Host ""
        Write-Host "📊 Python 套件檢查：" -ForegroundColor Yellow
        $packages = @("flask", "flask-cors", "requests", "pandas")
        
        foreach ($package in $packages) {
            try {
                $result = pip show $package 2>$null
                if ($result) {
                    Write-Host "✅ $package" -ForegroundColor Green
                }
                else {
                    Write-Host "❌ $package (未安裝)" -ForegroundColor Red
                }
            }
            catch {
                Write-Host "❌ $package (檢查失敗)" -ForegroundColor Red
            }
        }
        
        Write-Host ""
        Write-Host "🌐 API 金鑰檢查：" -ForegroundColor Yellow
        if (Test-Path "weather_map_config.py") {
            $config = Get-Content "weather_map_config.py" -Raw
            if ($config -match "openweather.*c3021b469b0ad866b2e96b3e5676347f") {
                Write-Host "✅ OpenWeather API 金鑰已設定" -ForegroundColor Green
            }
            else {
                Write-Host "❌ OpenWeather API 金鑰未設定" -ForegroundColor Red
            }
        }
    }
    "5" {
        Write-Host "👋 再見！" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "❌ 無效選擇，請重新執行腳本" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✨ 感謝使用全球天氣地圖系統！" -ForegroundColor Magenta
Read-Host "按 Enter 鍵退出"
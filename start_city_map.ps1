# 互動式城市人口地圖系統 PowerShell 啟動器

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🌍 互動式城市人口地圖系統啟動器" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ 正在開啟互動式城市地圖..." -ForegroundColor Green
Write-Host ""

Write-Host "🌟 系統功能：" -ForegroundColor Yellow
Write-Host "   📍 全球 25 個主要城市人口資料" -ForegroundColor White
Write-Host "   🎨 多種地圖樣式切換 (街道/衛星/暗色等)" -ForegroundColor White
Write-Host "   🌐 中英文語言切換" -ForegroundColor White
Write-Host "   📊 即時統計資訊顯示" -ForegroundColor White
Write-Host "   🎯 點擊城市查看詳細人口" -ForegroundColor White
Write-Host "   🔍 區域快速跳轉功能" -ForegroundColor White
Write-Host "   📱 響應式設計支援" -ForegroundColor White
Write-Host ""

Write-Host "💡 使用說明：" -ForegroundColor Cyan
Write-Host "   • 點擊城市圓點查看人口資訊" -ForegroundColor Gray
Write-Host "   • 使用右側按鈕跳轉到各大洲" -ForegroundColor Gray
Write-Host "   • 左側面板控制地圖樣式和語言" -ForegroundColor Gray
Write-Host "   • 滾輪縮放，拖拽移動地圖" -ForegroundColor Gray
Write-Host ""

# 檢查檔案是否存在
if (-not (Test-Path "interactive_city_map.html")) {
    Write-Host "❌ 錯誤：找不到 interactive_city_map.html 檔案" -ForegroundColor Red
    Write-Host "請確認檔案存在於當前目錄" -ForegroundColor Red
    Read-Host "按 Enter 鍵退出"
    exit 1
}

Write-Host "🚀 正在開啟地圖..." -ForegroundColor Green

# 開啟地圖檔案
$mapPath = Join-Path (Get-Location) "interactive_city_map.html"
Start-Process $mapPath

Write-Host ""
Write-Host "✅ 互動式城市人口地圖已在瀏覽器中開啟！" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 特色功能：" -ForegroundColor Yellow
Write-Host "   ✨ 全新動畫效果 - 載入動畫、懸停效果、彈窗動畫" -ForegroundColor White
Write-Host "   📈 即時統計 - 城市數量、總人口、平均人口、最大城市" -ForegroundColor White
Write-Host "   🎛️ 靈活控制 - 樣式切換、語言切換、點大小模式" -ForegroundColor White
Write-Host "   🗺️ 多樣化地圖 - 街道、衛星、簡約、暗色、戶外地圖" -ForegroundColor White
Write-Host "   📱 響應式設計 - 支援各種螢幕尺寸" -ForegroundColor White
Write-Host ""

Write-Host "💡 提示：如果地圖沒有正確顯示，請檢查網路連線" -ForegroundColor Cyan
Write-Host "🌐 地圖使用 Mapbox GL JS，需要網路連線載入地圖底圖" -ForegroundColor Gray
Write-Host ""

Write-Host "📊 技術特點：" -ForegroundColor Magenta
Write-Host "   • 基於 Mapbox GL JS 的現代地圖技術" -ForegroundColor White
Write-Host "   • CSS3 動畫和過渡效果" -ForegroundColor White
Write-Host "   • 響應式 RWD 設計" -ForegroundColor White
Write-Host "   • 無需後端服務器，純前端實現" -ForegroundColor White
Write-Host ""

Read-Host "按 Enter 鍵退出"
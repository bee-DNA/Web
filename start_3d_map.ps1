# 快速啟動 3D 互動城市地圖
# 作者: GitHub Copilot
# 日期: 2025-09-26

Write-Host "正在啟動 3D 互動城市地圖..." -ForegroundColor Green

# 設定工作目錄
Set-Location "D:\OneDrive\學校上課\課程\四上\科學大數據專題"

# 檢查檔案是否存在
if (-not (Test-Path "interactive_city_map_enhanced.html")) {
    Write-Host "錯誤: 找不到 interactive_city_map_enhanced.html" -ForegroundColor Red
    Read-Host "按任意鍵退出..."
    exit 1
}

# 啟動本地 HTTP 服務器
Write-Host "啟動 HTTP 服務器於端口 8086..." -ForegroundColor Yellow
python -m http.server 8086

# 如果 Python 失敗，嘗試其他方法
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python 服務器啟動失敗，嘗試其他方法..." -ForegroundColor Yellow
    
    # 嘗試直接開啟檔案
    Write-Host "直接在瀏覽器中開啟檔案..." -ForegroundColor Cyan
    Start-Process "interactive_city_map_enhanced.html"
}
# 虛擬環境 3D 互動城市地圖啟動腳本
# PowerShell 版本

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "        啟動虛擬環境 3D 互動城市地圖系統" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

Set-Location "D:\OneDrive\學校上課\課程\四上\科學大數據專題"

Write-Host "`n正在激活虛擬環境..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host "`n檢查虛擬環境狀態..." -ForegroundColor Green
python --version
Write-Host "虛擬環境路徑: $env:VIRTUAL_ENV" -ForegroundColor Green

Write-Host "`n正在啟動後端 HTTP 服務器 (端口 8086)..." -ForegroundColor Yellow

# 啟動後端服務器在背景
$job = Start-Job -ScriptBlock {
    Set-Location "D:\OneDrive\學校上課\課程\四上\科學大數據專題"
    & ".\venv\Scripts\Activate.ps1"
    python -m http.server 8086
}

Write-Host "後端服務器工作 ID: $($job.Id)" -ForegroundColor Green

# 等待服務器啟動
Write-Host "等待後端服務器啟動..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 測試服務器是否可用
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8086" -TimeoutSec 5 -ErrorAction SilentlyContinue
    Write-Host "後端服務器啟動成功！" -ForegroundColor Green
} catch {
    Write-Host "後端服務器可能還在啟動中..." -ForegroundColor Yellow
}

Write-Host "`n正在開啟前端地圖..." -ForegroundColor Cyan
Start-Process "http://localhost:8086/interactive_city_map_enhanced.html"

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "系統啟動完成！" -ForegroundColor Green
Write-Host "前端: http://localhost:8086/interactive_city_map_enhanced.html" -ForegroundColor White
Write-Host "後端: HTTP 服務器運行於端口 8086" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`n輸入 'stop' 來停止服務器，或按 Ctrl+C 退出" -ForegroundColor Yellow

# 等待用戶輸入
do {
    $input = Read-Host "輸入指令 (stop/status/help)"
    
    switch ($input.ToLower()) {
        "stop" {
            Write-Host "正在停止後端服務器..." -ForegroundColor Red
            Stop-Job -Job $job -ErrorAction SilentlyContinue
            Remove-Job -Job $job -ErrorAction SilentlyContinue
            Write-Host "服務器已停止" -ForegroundColor Red
            break
        }
        "status" {
            Write-Host "服務器狀態: $($job.State)" -ForegroundColor Cyan
            Write-Host "工作 ID: $($job.Id)" -ForegroundColor Cyan
        }
        "help" {
            Write-Host "可用指令:" -ForegroundColor Cyan
            Write-Host "  stop   - 停止後端服務器" -ForegroundColor White
            Write-Host "  status - 檢查服務器狀態" -ForegroundColor White
            Write-Host "  help   - 顯示此說明" -ForegroundColor White
        }
        default {
            if ($input -ne "") {
                Write-Host "未知指令: $input (輸入 'help' 查看可用指令)" -ForegroundColor Red
            }
        }
    }
} while ($input.ToLower() -ne "stop" -and $input -ne "")

Write-Host "腳本結束" -ForegroundColor Green
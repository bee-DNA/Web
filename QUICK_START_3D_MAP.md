# 3D 互動城市地圖快速啟動指南

## 🚀 快速啟動方法

### 方法 1: 使用啟動腳本 (推薦)

```bash
# PowerShell 版本
.\start_3d_map.ps1

# 或 批次檔版本
.\start_3d_map.bat
```

### 方法 2: 手動啟動

```bash
# 1. 進入專案目錄
cd "D:\OneDrive\學校上課\課程\四上\科學大數據專題"

# 2. 啟動 HTTP 服務器
python -m http.server 8086

# 3. 在瀏覽器中開啟
# http://localhost:8086/interactive_city_map_enhanced.html
```

### 方法 3: 直接開啟檔案

```bash
# 直接在檔案總管中雙擊
interactive_city_map_enhanced.html
```

## 📋 檔案說明

### 主要檔案 (Git 追蹤)

- **`interactive_city_map_enhanced.html`** - 主要的 3D 互動城市地圖 ✅
  - 包含 3D 視角功能
  - 建築物圖層視覺化
  - 25 個全球城市人口資料
  - 多語言支援 (中文/英文)
  - 地圖樣式切換

### 功能特色

- 🌍 **25 個全球主要城市**：東京、上海、德里、聖保羅等
- 📊 **人口統計資訊**：即時顯示城市人口數據
- 🎯 **3D 視角控制**：2D、3D-低、3D-中、3D-高
- 🏢 **3D 建築物圖層**：可切換的建築物視覺化
- 🗺️ **多種地圖樣式**：街道、衛星、地形等
- 🌐 **多語言介面**：中英文切換
- 🔍 **智慧搜尋**：城市快速定位

### Git 版本資訊

```
最新提交: 7bffec7
訊息: feat: 新增 3D 視角功能 - 包含建築物圖層和視角控制
分支: master (與遠端同步)
```

## 🛠️ 故障排除

### 如果無法啟動 HTTP 服務器

1. 檢查 Python 是否已安裝
2. 嘗試不同端口：`python -m http.server 8087`
3. 直接在瀏覽器中開啟 HTML 檔案

### 如果地圖無法載入

1. 檢查網路連接
2. 確認 Mapbox API Token 有效
3. 檢查瀏覽器控制台錯誤訊息

### 如果 3D 功能無法使用

1. 確保使用現代瀏覽器 (Chrome、Firefox、Safari、Edge)
2. 檢查 WebGL 支援
3. 嘗試重新整理頁面

## 📁 備份檔案

- `interactive_city_map_test.html` - 測試版本
- `interactive_city_map_fixed.html` - 修復版本
- `interactive_city_weather_map.html` - 天氣地圖版本

這些是未追蹤的測試檔案，可以安全刪除或保留作為備份。

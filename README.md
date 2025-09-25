# 🌍 全球天氣海洋地圖專案

科學大數據專題 - 整合多源資料的即時天氣與海洋環境視覺化系統

## ⚡ 快速啟動

### 方法一：使用啟動腳本 (推薦)

```bash
# Windows CMD
start_weather_map.bat

# Windows PowerShell
.\start_weather_map.ps1
```

### 方法二：直接開啟 HTML

雙擊 `global_weather_map.html` 即可在瀏覽器中開啟完整的天氣地圖系統！

### 方法三：Python 後端服務

```bash
python global_weather_map_server.py
# 訪問: http://localhost:5001/map/global
```

## 🌟 主要功能

### 🌦️ 即時天氣監測

- **全球覆蓋**: 16 個主要城市實時天氣資料
- **多元資料**: 溫度、濕度、風速、氣壓、能見度、雲量
- **自動更新**: 每 2 小時自動刷新資料
- **地區篩選**: 亞洲、歐洲、美洲、大洋洲、非洲分區顯示

### 🗺️ 視覺化圖層

- **溫度地圖**: 彩色編碼溫度分布
- **雲圖覆蓋**: OpenWeather 雲層資料
- **降雨圖**: 即時降水強度顯示
- **衛星影像**: Mapbox 高解析度衛星圖
- **海洋資料**: 海表溫度監測 (開發中)

### 🎛️ 互動控制

- **3D 視角**: 立體地形顯示
- **全螢幕**: 沉浸式體驗
- **圖層透明度**: 自定義顯示效果
- **地點跳轉**: 快速定位到感興趣區域
- **詳細資訊**: 點擊氣象站查看詳細資料

## 📊 技術架構

### 前端技術

- **Mapbox GL JS**: 高效能地圖渲染引擎
- **響應式設計**: 支援桌面與行動裝置
- **即時更新**: WebSocket 連接 (規劃中)

### 後端技術

- **Flask**: Python Web 框架
- **多 API 整合**: OpenWeather、NASA、NOAA
- **資料處理**: Pandas、NumPy
- **並發處理**: 多線程資料更新

### 資料來源

- **OpenWeather API**: 全球天氣資料
- **NASA Earthdata**: 衛星影像與海洋資料
- **NOAA**: 海洋環境與颱風路徑
- **Mapbox**: 地圖底圖與衛星影像

## 🚀 系統架構與功能

### 🌟 核心系統

#### 🌍 整合世界地圖 & 天氣系統 (主要系統)

- **檔案**: `integrated_world_weather_map.py`
- **啟動**: `start_integrated_map.bat`
- **網址**: http://localhost:8050/

**雙模式設計：**

1. **📊 國家統計模式**：人口分布、GDP 分析、互動資料表
2. **🌦️ 全球天氣模式**：18 個主要城市即時天氣監測

### 📊 使用技術

- **後端**: Python + Flask + Dash + Plotly
- **前端**: HTML5 + CSS3 + JavaScript + Mapbox GL JS
- **資料處理**: Pandas + NumPy + Requests
- **視覺化**: Plotly + Mapbox GL JS
- **API 整合**: OpenWeather + NASA + NOAA

### 🎯 主要特色

- **即時資料**: 每 2 小時自動更新天氣資料
- **全球覆蓋**: 亞洲、歐洲、美洲、大洋洲、非洲 18 個主要城市
- **互動視覺化**: 可縮放、篩選、排序的動態地圖
- **響應式設計**: 支援桌面與行動裝置
- **模組化架構**: 易於擴展和維護

## 🚀 快速啟動

### 🎯 推薦方式：整合系統

```bash
# 執行整合系統啟動腳本
start_integrated_map.bat

# 或直接執行 Python
python integrated_world_weather_map.py
# 訪問: http://localhost:8050/
```

### ⚡ 替代方式：獨立天氣地圖

```bash
# 直接開啟 HTML (最簡單)
# 雙擊 global_weather_map.html

# 或使用啟動腳本
start_weather_map.bat
```

## 🌍 監測範圍

### 全球 18 個主要城市

- 🏯 **亞洲** (7 城): 台北、東京、首爾、北京、香港、新加坡、孟買
- 🏰 **歐洲** (5 城): 倫敦、巴黎、柏林、羅馬、莫斯科
- 🗽 **美洲** (3 城): 紐約、洛杉磯、聖保羅
- 🦘 **大洋洲** (1 城): 雪梨
- 🦁 **非洲** (2 城): 開普敦、開羅

## 📋 使用說明

詳細文件請參考：

- `INTEGRATED_SYSTEM_GUIDE.md` - 🌍 整合系統完整使用指南
- `PROJECT_SUMMARY.md` - 📊 專案完成總結報告

## 🛠️ 故障排除

```bash
# 安裝依賴
pip install dash plotly pandas requests numpy flask flask-cors

# 系統測試
python test_system.py test
```

## 作者

- 季正偉 - 科學大數據專題課程

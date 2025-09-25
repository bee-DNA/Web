# 🌍 簡潔地圖系統使用指南

## 📋 系統概述

這是一個基於 Mapbox GL JS 的簡潔互動式地圖系統，提供基本的地圖瀏覽功能。

## 🚀 快速啟動

### 1. 啟動服務

```bash
python mapbox_api_server.py
```

### 2. 訪問地圖

在瀏覽器中開啟：`http://localhost:5000/map`

## 📁 核心文件

### 必需文件：

- `mapbox_api_server.py` - Flask 後端服務器
- `mapbox_interactive_map.html` - 地圖前端頁面
- `requirements.txt` - Python 依賴包

### 可選文件：

- `mapbox_config.py` - 配置設定
- `data/` - 資料目錄

## 🌟 功能特色

✅ **基本功能**：

- 🗺️ 互動式地圖瀏覽
- 🔍 縮放和平移操作
- 📍 地圖資料點顯示
- 🌍 全球城市資料展示

✅ **API 端點**：

- `/api/cities` - 城市資料
- `/api/cities/geojson` - GeoJSON 格式
- `/api/heatmap` - 熱力圖資料
- `/api/statistics` - 統計資訊

## 🛠️ 技術架構

- **前端**: Mapbox GL JS + HTML/CSS/JavaScript
- **後端**: Flask + Python
- **資料**: JSON/GeoJSON 格式

## 📝 使用說明

1. **地圖操作**：

   - 滑鼠拖拽：移動地圖
   - 滾輪：縮放地圖
   - 點擊標記：查看詳細資訊

2. **API 使用**：
   ```javascript
   // 取得城市資料
   fetch("/api/cities")
     .then((response) => response.json())
     .then((data) => console.log(data));
   ```

## 🔧 系統需求

- Python 3.7+
- Flask 2.0+
- 現代瀏覽器（支援 WebGL）

---

✨ **簡潔而強大的地圖解決方案！**

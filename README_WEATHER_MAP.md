# 🌦️ 即時天氣海洋地圖系統

## 📋 專案概述

這是一個整合了**天氣、雲圖、洋流、衛星影像**等多種即時資料源的互動式地圖系統，專為科學大數據分析和氣象海洋研究而設計。

## ✨ 新增功能特色

### 🎯 **即時資料整合**
- **☁️ 天氣資料**: OpenWeatherMap API 整合
- **🛰️ 衛星雲圖**: NASA EOSDIS Worldview
- **🌊 海洋資料**: NOAA 海表溫度、洋流資料
- **🌀 颱風追蹤**: JMA、CWB、JTWC 颱風路徑

### 🌍 **多圖層視覺化**
- **📍 氣象站標記**: 顏色編碼溫度顯示
- **🌡️ 溫度等高線**: 即時溫度分布
- **💧 降雨雲圖**: 降雨強度視覺化
- **💨 風場向量**: 風速風向動態顯示

### 🎨 **進階介面功能**
- **響應式側邊欄**: 圖層控制和即時資料
- **多地圖樣式**: 明亮/深色/衛星/街道樣式
- **圖層透明度控制**: 自定義圖層顯示
- **全螢幕模式**: 沉浸式地圖體驗

## 🚀 快速開始

### 1. 啟動天氣地圖服務

```powershell
# 啟動後端 API 服務
python weather_map_server.py
```

📍 **訪問地址**:
- **🌐 天氣地圖介面**: http://localhost:5000/map/weather
- **📄 獨立 HTML 介面**: 直接開啟 `realtime_weather_map.html`
- **📡 API 文件**: http://localhost:5000

### 2. API Key 設定 (可選)

#### **取得 OpenWeather API Key**
1. 註冊 [OpenWeatherMap 帳號](https://openweathermap.org/api)
2. 申請免費 API Key
3. 在地圖介面中輸入 API Key

#### **取得中央氣象署 API Key** 
1. 註冊 [氣象資料開放平台](https://opendata.cwb.gov.tw/)
2. 申請 API 授權碼
3. 在配置檔案中設定

> 💡 **注意**: 不設定 API Key 將使用內建示範資料

## 📁 檔案結構

```
weather-map-system/
├── weather_map_config.py          # 設定檔案
├── weather_map_server.py          # 後端 API 服務
├── weather_map_template.py        # HTML 模板
├── realtime_weather_map.html      # 獨立前端介面
└── README_WEATHER_MAP.md          # 說明文件
```

## 🔧 配置選項

### **資料來源配置**
```python
# OpenWeatherMap
OPENWEATHER_API_KEY = 'your_api_key_here'

# 中央氣象署  
CWB_API_KEY = 'your_cwb_api_key_here'

# 更新頻率設定
UPDATE_INTERVALS = {
    'weather_current': 600,    # 10分鐘
    'satellite_images': 1800,  # 30分鐘
    'ocean_data': 21600        # 6小時
}
```

### **地圖樣式**
- **明亮樣式**: 適合白天使用的清晰地圖
- **深色樣式**: 適合夜間或專業展示
- **衛星樣式**: 高解析度衛星影像
- **街道樣式**: 詳細的街道和地標資訊

## 📊 支援的資料類型

### **天氣資料**
- ✅ 即時溫度、濕度、氣壓
- ✅ 風速、風向
- ✅ 天氣狀況描述
- 🔄 5天天氣預報

### **雲圖和衛星影像**
- 🔄 可見光雲圖
- 🔄 紅外線雲圖
- 🔄 水汽影像
- 🔄 真彩色衛星影像

### **海洋資料**
- 🔄 海表溫度
- 🔄 洋流方向和速度
- 🔄 海浪高度
- 🔄 海流模式

### **颱風資訊**
- 🔄 颱風即時位置
- 🔄 預測路徑
- 🔄 強度變化
- 🔄 警報範圍

> ✅ = 已實作 | 🔄 = 規劃中/需 API Key

## 🎛️ 使用說明

### **基本操作**
1. **🔑 設定 API Key**: 在側邊欄輸入 OpenWeather API Key
2. **🗺️ 選擇地圖樣式**: 使用下拉選單切換樣式
3. **📍 查看氣象站**: 點擊地圖上的圓點查看詳細資訊
4. **🎨 調整圖層**: 使用側邊欄控制項開關圖層

### **進階功能**
- **🔄 自動更新**: 每10分鐘自動更新資料
- **💾 資料匯出**: 將當前資料匯出為 JSON 格式
- **📺 全螢幕模式**: 適合簡報展示
- **📊 統計資訊**: 查看全台氣象統計

### **互動操作**
- **🖱️ 點擊氣象站**: 顯示詳細天氣資訊彈窗
- **📱 點擊側邊欄卡片**: 快速定位到該氣象站
- **🔍 滾輪縮放**: 地圖縮放操作
- **🖐️ 拖拽平移**: 移動地圖視窗

## 📡 API 端點

```http
GET /api/weather/current          # 指定位置當前天氣
GET /api/weather/stations         # 台灣氣象站資料
GET /api/layers/weather           # 天氣圖層資訊
GET /api/layers/ocean             # 海洋圖層資訊
GET /api/layers/satellite         # 衛星圖層資訊
GET /api/config                   # 地圖配置資訊
```

## 🔮 未來擴展計劃

### **短期目標**
- [ ] 整合更多即時天氣圖層
- [ ] 添加颱風路徑預測
- [ ] 支援歷史資料查詢
- [ ] 增加手機 App 響應式設計

### **中期目標**
- [ ] 3D 地形和大氣可視化
- [ ] 機器學習天氣預測模型
- [ ] 多語言介面支援
- [ ] 資料分析儀表板

### **長期目標**
- [ ] 整合物聯網感測器資料
- [ ] 即時災害預警系統
- [ ] 氣候變遷長期趨勢分析
- [ ] 國際資料源整合

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request 來改善此專案！

### **開發環境設置**
```powershell
# 安裝相依套件
pip install flask flask-cors requests pandas

# 啟動開發服務器
python weather_map_server.py
```

## 📄 授權條款

此專案採用 MIT 授權條款。

---

## 🆘 常見問題

**Q: 為什麼地圖上沒有顯示天氣資料？**
A: 請確認已設定有效的 OpenWeather API Key，或使用示範資料模式。

**Q: 如何添加更多氣象站？**
A: 編輯 `weather_map_server.py` 中的 `get_taiwan_weather_stations()` 函數。

**Q: 資料多久更新一次？**
A: 預設每10分鐘自動更新一次，您也可以手動點擊更新按鈕。

**Q: 支援哪些瀏覽器？**
A: 支援所有現代瀏覽器，建議使用 Chrome、Firefox、Safari 或 Edge。

---

**📧 如有問題，請聯繫專案維護者或提交 GitHub Issue。**
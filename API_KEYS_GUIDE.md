# API Keys 配置檔案使用指南

## 📋 已建立的配置檔案

### 1. Python 配置檔案
**檔案：** `api_keys.py`

**使用方式：**
```python
# 引用方式 1：直接導入
from api_keys import get_mapbox_token, get_openweather_key, get_noaa_key

mapbox_token = get_mapbox_token()
weather_key = get_openweather_key() 
noaa_key = get_noaa_key()

# 引用方式 2：配置字典
from api_keys import API_CONFIG

mapbox_config = API_CONFIG["MAPBOX"]
weather_config = API_CONFIG["OPENWEATHER"]

# 引用方式 3：直接導入常數
from api_keys import MAPBOX_ACCESS_TOKEN, OPENWEATHER_API_KEY
```

### 2. JavaScript 配置檔案  
**檔案：** `api_keys.js`

**使用方式：**
```html
<!-- 在 HTML 中引用 -->
<script src="api_keys.js"></script>
<script>
    // Mapbox 自動設置完成
    console.log('Mapbox Token:', API_KEYS.MAPBOX_ACCESS_TOKEN);
    
    // 取得天氣 API URL
    const weatherUrl = getWeatherApiUrl('current', {
        lat: 25.0330, 
        lon: 121.5654
    });
    
    // 使用地圖樣式
    const map = new mapboxgl.Map({
        style: API_CONFIG.MAPBOX.STYLES.light
    });
</script>
```

## 🔑 包含的 API Keys

### Mapbox API (地圖服務)
- **Token:** `pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w`
- **用途:** 地圖顯示、地圖樣式、3D 建築物

### OpenWeatherMap API (天氣資料)  
- **Key:** `c3021b469b0ad866b2e96b3e5676347f`
- **用途:** 即時天氣、天氣預報、天氣圖層

### NOAA API (海洋/氣象資料)
- **Key:** `qFQyVggGGRNuYyKAiNvJYJfoOyONaDpwG`  
- **用途:** 海表溫度、洋流、氣象資料

## 🚀 快速整合現有專案

### 更新 HTML 檔案
```html
<!-- 替換原有的 mapbox token 設置 -->
<script src="api_keys.js"></script>
<!-- mapboxgl.accessToken 會自動設置 -->
```

### 更新 Python 檔案
```python
# 替換原有的 API key 設置
from api_keys import API_CONFIG

# 使用統一配置
openweather_key = API_CONFIG["OPENWEATHER"]["API_KEY"] 
mapbox_token = API_CONFIG["MAPBOX"]["ACCESS_TOKEN"]
```

## 🛠️ 便捷功能

### JavaScript 輔助函數
```javascript
// 取得完整的天氣 API URL
getWeatherApiUrl('current', {lat: 25.033, lon: 121.565})

// 取得天氣圖層 URL
getWeatherLayerUrl('precipitation')

// 驗證 API Keys
validateApiKeys()
```

### Python 輔助函數  
```python
# 驗證 API Keys 有效性
from api_keys import validate_keys
validation_results = validate_keys()

# 取得天氣圖層 URL
from api_keys import get_weather_layer_url
layer_url = get_weather_layer_url('clouds')
```

## 📁 檔案結構
```
api_keys.py           # Python 配置檔案
api_keys.js           # JavaScript 配置檔案  
API_KEYS_GUIDE.md     # 使用說明 (本檔案)
```

## ⚠️ 安全提醒
- 這些 API Keys 已在程式碼中使用
- 建議定期檢查 API 使用量
- 如需更高安全性，考慮使用環境變數
- 不要將此檔案上傳到公開的 Git 儲存庫

## 🎯 下次使用
直接引用 `api_keys.py` 或 `api_keys.js`，不需要再手動複製貼上 API Keys！
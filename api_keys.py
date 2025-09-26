"""
統一 API Keys 配置檔案
所有專案使用的 API Keys 集中管理
作者: GitHub Copilot
日期: 2025-09-26
"""

# ==================================
#           主要 API Keys
# ==================================

# Mapbox API (地圖服務)
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w"

# OpenWeatherMap API (天氣資料)
OPENWEATHER_API_KEY = "c3021b469b0ad866b2e96b3e5676347f"

# NOAA API (海洋/氣象資料)
NOAA_API_KEY = "qFQyVggGGRNuYyKAiNvJYJfoOyONaDpwG"

# ==================================
#        API 配置字典
# ==================================

API_CONFIG = {
    # Mapbox 地圖服務
    "MAPBOX": {
        "ACCESS_TOKEN": MAPBOX_ACCESS_TOKEN,
        "BASE_URL": "https://api.mapbox.com",
        "STYLES": {
            "streets": "mapbox://styles/mapbox/streets-v12",
            "satellite": "mapbox://styles/mapbox/satellite-v9",
            "light": "mapbox://styles/mapbox/light-v11",
            "dark": "mapbox://styles/mapbox/dark-v11",
            "outdoors": "mapbox://styles/mapbox/outdoors-v12",
            "navigation": "mapbox://styles/mapbox/navigation-day-v1"
        }
    },
    
    # OpenWeatherMap 天氣 API
    "OPENWEATHER": {
        "API_KEY": OPENWEATHER_API_KEY,
        "BASE_URL": "https://api.openweathermap.org/data/2.5",
        "ENDPOINTS": {
            "current": "/weather",
            "forecast": "/forecast",
            "onecall": "/onecall",
            "air_pollution": "/air_pollution"
        },
        "LAYERS": {
            "precipitation": "https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid={api_key}",
            "clouds": "https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid={api_key}",
            "pressure": "https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid={api_key}",
            "wind": "https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid={api_key}",
            "temp": "https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid={api_key}"
        }
    },
    
    # NOAA 海洋/氣象資料
    "NOAA": {
        "API_KEY": NOAA_API_KEY,
        "BASE_URL": "https://www.ncdc.noaa.gov/cdo-web/api/v2",
        "DATASETS": {
            "sea_surface_temp": "satellite/avhrr_pathfinder-pds-v52/pathfinder",
            "ocean_currents": "ocean_atlas_2009/woa09/temperature_monthly_1deg.nc"
        }
    },
    
    # 中央氣象署 (需要申請)
    "CWB": {
        "API_KEY": "YOUR_CWB_API_KEY",  # 請到 https://opendata.cwb.gov.tw/ 申請
        "BASE_URL": "https://opendata.cwb.gov.tw/api",
        "NOTE": "請到中央氣象署開放資料平台申請 API Key"
    }
}

# ==================================
#        JavaScript 匯出
# ==================================

def get_js_config():
    """生成 JavaScript 配置字串"""
    return f"""
// API Keys 配置 (由 Python 生成)
const API_CONFIG = {{
    MAPBOX: {{
        ACCESS_TOKEN: '{MAPBOX_ACCESS_TOKEN}',
        STYLES: {{
            streets: 'mapbox://styles/mapbox/streets-v12',
            satellite: 'mapbox://styles/mapbox/satellite-v9',
            light: 'mapbox://styles/mapbox/light-v11',
            dark: 'mapbox://styles/mapbox/dark-v11',
            outdoors: 'mapbox://styles/mapbox/outdoors-v12',
            navigation: 'mapbox://styles/mapbox/navigation-day-v1'
        }}
    }},
    OPENWEATHER: {{
        API_KEY: '{OPENWEATHER_API_KEY}',
        BASE_URL: 'https://api.openweathermap.org/data/2.5'
    }},
    NOAA: {{
        API_KEY: '{NOAA_API_KEY}',
        BASE_URL: 'https://www.ncdc.noaa.gov/cdo-web/api/v2'
    }}
}};

// 設置 Mapbox Access Token
mapboxgl.accessToken = API_CONFIG.MAPBOX.ACCESS_TOKEN;
"""

# ==================================
#        便捷函數
# ==================================

def get_mapbox_token():
    """取得 Mapbox Access Token"""
    return MAPBOX_ACCESS_TOKEN

def get_openweather_key():
    """取得 OpenWeather API Key"""
    return OPENWEATHER_API_KEY

def get_noaa_key():
    """取得 NOAA API Key"""
    return NOAA_API_KEY

def get_weather_layer_url(layer_type, api_key=None):
    """取得天氣圖層 URL"""
    if api_key is None:
        api_key = OPENWEATHER_API_KEY
    
    layers = API_CONFIG["OPENWEATHER"]["LAYERS"]
    if layer_type in layers:
        return layers[layer_type].format(api_key=api_key)
    return None

def validate_keys():
    """驗證 API Keys 是否有效"""
    results = {
        "mapbox": len(MAPBOX_ACCESS_TOKEN) > 50 and MAPBOX_ACCESS_TOKEN.startswith("pk."),
        "openweather": len(OPENWEATHER_API_KEY) == 32,
        "noaa": len(NOAA_API_KEY) > 10
    }
    return results

# ==================================
#        使用說明
# ==================================

USAGE_GUIDE = """
使用方法:

1. Python 中引用:
   from api_keys import get_mapbox_token, get_openweather_key
   
2. JavaScript 中引用:
   // 在 HTML 中加入以下腳本
   <script>
   // 從 Python 生成配置
   """ + get_js_config() + """
   </script>
   
3. 直接取得配置:
   from api_keys import API_CONFIG
   mapbox_token = API_CONFIG["MAPBOX"]["ACCESS_TOKEN"]
"""

if __name__ == "__main__":
    print("=== API Keys 配置檔案 ===")
    print(f"Mapbox Token: {MAPBOX_ACCESS_TOKEN[:20]}...")
    print(f"OpenWeather Key: {OPENWEATHER_API_KEY[:10]}...")
    print(f"NOAA Key: {NOAA_API_KEY[:10]}...")
    print("\nAPI Keys 驗證結果:")
    validation = validate_keys()
    for api, valid in validation.items():
        status = "✅ 有效" if valid else "❌ 無效"
        print(f"  {api}: {status}")
"""
即時天氣地圖配置檔案
整合天氣、雲圖、洋流等即時資料源
"""

# API Keys 配置 (用於測試腳本)
API_KEYS = {
    "openweather": "c3021b469b0ad866b2e96b3e5676347f",
    "nasa": "your_nasa_jwt_token_here",
    "noaa": "qFQyVggGGRNuYyKAiNvJYJfoOyONaDpwG",
}

# 天氣資料 API 配置
WEATHER_CONFIG = {
    # OpenWeatherMap API
    "OPENWEATHER": {
        "BASE_URL": "https://api.openweathermap.org/data/2.5",
        "API_KEY": "c3021b469b0ad866b2e96b3e5676347f",
        "ENDPOINTS": {
            "current": "/weather",
            "forecast": "/forecast",
            "onecall": "/onecall",
        },
    },
    # 天氣雲圖和雷達圖
    "WEATHER_LAYERS": {
        "precipitation": "https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid={api_key}",
        "clouds": "https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid={api_key}",
        "pressure": "https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid={api_key}",
        "wind": "https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid={api_key}",
        "temp": "https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid={api_key}",
    },
}

# 海洋資料配置
OCEAN_CONFIG = {
    # NOAA 海洋資料
    "NOAA": {
        "BASE_URL": "https://www.ncdc.noaa.gov/cdo-web/api/v2",
        "API_KEY": "qFQyVggGGRNuYyKAiNvJYJfoOyONaDpwG",
        "DATASETS": {
            "sea_surface_temp": "satellite/avhrr_pathfinder-pds-v52/pathfinder",
            "ocean_currents": "ocean_atlas_2009/woa09/temperature_monthly_1deg.nc",
        },
    },
    # 海洋圖層
    "OCEAN_LAYERS": {
        "sea_surface_temperature": {
            "name": "海表溫度",
            "type": "wms",
            "url": "https://coastwatch.pfeg.noaa.gov/erddap/wms/jplAvisoSlaDaily/request",
            "layers": "sla",
            "format": "image/png",
            "transparent": True,
        },
        "ocean_currents": {
            "name": "洋流",
            "type": "vector",
            "description": "海流方向和速度",
        },
    },
}

# 衛星和雲圖配置
SATELLITE_CONFIG = {
    # NASA EOSDIS Worldview
    "NASA_WORLDVIEW": {
        "BASE_URL": "https://map1.vis.earthdata.nasa.gov/wmts-geo/1.0.0",
        "API_TOKEN": "eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImJlZWRuYSIsImV4cCI6MTc2NDAyODc5OSwiaWF0IjoxNzU4ODI3MDYwLCJpc3MiOiJodHRwczovL3Vycy5lYXJ0aGRhdGEubmFzYS5nb3YiLCJpZGVudGl0eV9wcm92aWRlciI6ImVkbF9vcHMiLCJhY3IiOiJlZGwiLCJhc3N1cmFuY2VfbGV2ZWwiOjN9.HCCOQu2FkAD3kOsmHCabqROWVJg1d1-lqVWGEk29QxesT02_oCIBB-ILwxVloZUNaoWj3ihShvZKEvtbiBqKDJtRFvnsfTD4Ar1WwdXfV5Cw55U-Z6Lp_dwE77bSmF6VC2wl5AgZBLzNbIU5nJkHPoeURA68hu-EmTQxmxe217SJHNZaLQqowATYnX6gEDD1ENRPaLZR7pIQug4JlYxHHmPRPfK4HozMQ_VEAKGYr2cS4lAqcUOQ0eJLgM4_PY-pXMT3QNwBgYbInL8mXcMLRmgvgpbtMoluyXjmOmL4psA76uudOmh5Lfi8MpgdhOcXh52nWnOtq3Fps5Z5IqfJxQ",
        "LAYERS": {
            "modis_terra": "MODIS_Terra_CorrectedReflectance_TrueColor",
            "modis_aqua": "MODIS_Aqua_CorrectedReflectance_TrueColor",
            "viirs_snpp": "VIIRS_SNPP_CorrectedReflectance_TrueColor",
        },
    },
    # 中央氣象署衛星雲圖
    "CWB_SATELLITE": {
        "BASE_URL": "https://www.cwb.gov.tw/Data/satellite",
        "LAYERS": {"ir1": "紅外線雲圖", "vis": "可見光雲圖", "color": "彩色雲圖"},
    },
}

# 颱風和極端天氣配置
TYPHOON_CONFIG = {
    # 日本氣象廳 JMA
    "JMA": {
        "BASE_URL": "https://www.jma.go.jp/bosai/forecast/data/forecast",
        "TYPHOON_URL": "https://www.jma.go.jp/bosai/forecast/data/typhoon",
    },
    # 中央氣象署
    "CWB": {
        "BASE_URL": "https://opendata.cwb.gov.tw/api",
        "API_KEY": "YOUR_CWB_API_KEY",  # 請到 https://opendata.cwb.gov.tw/ 申請
        "TYPHOON_ENDPOINT": "/v1/rest/datastore/W-C0034-001",
    },
    # JTWC (Joint Typhoon Warning Center)
    "JTWC": {
        "BASE_URL": "https://www.metoc.navy.mil/jtwc/products",
        "KML_URL": "https://www.metoc.navy.mil/jtwc/products/sh{year}{basin}.dat",
    },
}

# 地圖樣式配置
MAP_STYLES = {
    "weather": {
        "name": "天氣地圖",
        "style": "mapbox://styles/mapbox/light-v11",
        "default_layers": ["precipitation", "clouds"],
    },
    "ocean": {
        "name": "海洋地圖",
        "style": "mapbox://styles/mapbox/satellite-v9",
        "default_layers": ["sea_surface_temperature", "ocean_currents"],
    },
    "satellite": {
        "name": "衛星雲圖",
        "style": "mapbox://styles/mapbox/satellite-streets-v12",
        "default_layers": ["modis_terra", "typhoon_tracks"],
    },
}

# 更新頻率設定 (按您的要求每2小時更新)
UPDATE_INTERVALS = {
    "weather_current": 7200,  # 2 小時
    "weather_forecast": 7200,  # 2 小時
    "satellite_images": 7200,  # 2 小時
    "ocean_data": 7200,  # 2 小時
    "typhoon_tracks": 7200,  # 2 小時
}

# 全球地區預設視窗
GLOBAL_BOUNDS = {
    "center": {"lng": 0, "lat": 20},
    "zoom": 2,
    "bounds": [[-180, -85], [180, 85]],  # 西南角  # 東北角
}

# 台灣地區預設視窗
TAIWAN_BOUNDS = {
    "center": {"lng": 121.0, "lat": 23.8},
    "zoom": 7,
    "bounds": [[118.0, 21.5], [124.0, 26.5]],  # 西南角  # 東北角
}

# 全球主要城市氣象站
GLOBAL_WEATHER_STATIONS = {
    "asia": [
        {"name": "東京", "lat": 35.6762, "lng": 139.6503, "country": "JP"},
        {"name": "首爾", "lat": 37.5665, "lng": 126.9780, "country": "KR"},
        {"name": "北京", "lat": 39.9042, "lng": 116.4074, "country": "CN"},
        {"name": "上海", "lat": 31.2304, "lng": 121.4737, "country": "CN"},
        {"name": "香港", "lat": 22.3193, "lng": 114.1694, "country": "HK"},
        {"name": "新加坡", "lat": 1.3521, "lng": 103.8198, "country": "SG"},
        {"name": "曼谷", "lat": 13.7563, "lng": 100.5018, "country": "TH"},
        {"name": "孟買", "lat": 19.0760, "lng": 72.8777, "country": "IN"},
        {"name": "德里", "lat": 28.7041, "lng": 77.1025, "country": "IN"},
    ],
    "europe": [
        {"name": "倫敦", "lat": 51.5074, "lng": -0.1278, "country": "GB"},
        {"name": "巴黎", "lat": 48.8566, "lng": 2.3522, "country": "FR"},
        {"name": "柏林", "lat": 52.5200, "lng": 13.4050, "country": "DE"},
        {"name": "羅馬", "lat": 41.9028, "lng": 12.4964, "country": "IT"},
        {"name": "馬德里", "lat": 40.4168, "lng": -3.7038, "country": "ES"},
        {"name": "莫斯科", "lat": 55.7558, "lng": 37.6176, "country": "RU"},
    ],
    "americas": [
        {"name": "紐約", "lat": 40.7128, "lng": -74.0060, "country": "US"},
        {"name": "洛杉磯", "lat": 34.0522, "lng": -118.2437, "country": "US"},
        {"name": "芝加哥", "lat": 41.8781, "lng": -87.6298, "country": "US"},
        {"name": "多倫多", "lat": 43.6532, "lng": -79.3832, "country": "CA"},
        {"name": "墨西哥城", "lat": 19.4326, "lng": -99.1332, "country": "MX"},
        {"name": "聖保羅", "lat": -23.5505, "lng": -46.6333, "country": "BR"},
        {"name": "布宜諾斯艾利斯", "lat": -34.6037, "lng": -58.3816, "country": "AR"},
    ],
    "oceania": [
        {"name": "雪梨", "lat": -33.8688, "lng": 151.2093, "country": "AU"},
        {"name": "墨爾本", "lat": -37.8136, "lng": 144.9631, "country": "AU"},
        {"name": "奧克蘭", "lat": -36.8485, "lng": 174.7633, "country": "NZ"},
    ],
    "africa": [
        {"name": "開羅", "lat": 30.0444, "lng": 31.2357, "country": "EG"},
        {"name": "拉哥斯", "lat": 6.5244, "lng": 3.3792, "country": "NG"},
        {"name": "開普敦", "lat": -33.9249, "lng": 18.4241, "country": "ZA"},
        {"name": "約翰尼斯堡", "lat": -26.2041, "lng": 28.0473, "country": "ZA"},
    ],
    "taiwan": [
        {"name": "台北", "lat": 25.0330, "lng": 121.5654, "country": "TW"},
        {"name": "新竹", "lat": 24.8138, "lng": 120.9675, "country": "TW"},
        {"name": "台中", "lat": 24.1477, "lng": 120.6736, "country": "TW"},
        {"name": "嘉義", "lat": 23.4801, "lng": 120.4491, "country": "TW"},
        {"name": "台南", "lat": 22.9999, "lng": 120.2269, "country": "TW"},
        {"name": "高雄", "lat": 22.6273, "lng": 120.3014, "country": "TW"},
        {"name": "花蓮", "lat": 23.9871, "lng": 121.6015, "country": "TW"},
        {"name": "台東", "lat": 22.7972, "lng": 121.1713, "country": "TW"},
    ],
}

# 圖層控制配置
LAYER_CONTROLS = {
    "weather": {
        "precipitation": {"name": "降雨量", "default": True, "opacity": 0.7},
        "clouds": {"name": "雲層", "default": True, "opacity": 0.6},
        "wind": {"name": "風場", "default": False, "opacity": 0.8},
        "temperature": {"name": "溫度", "default": False, "opacity": 0.7},
        "pressure": {"name": "氣壓", "default": False, "opacity": 0.6},
    },
    "ocean": {
        "sea_temp": {"name": "海表溫度", "default": True, "opacity": 0.7},
        "currents": {"name": "洋流", "default": True, "opacity": 0.8},
        "waves": {"name": "海浪", "default": False, "opacity": 0.6},
    },
    "satellite": {
        "visible": {"name": "可見光", "default": True, "opacity": 1.0},
        "infrared": {"name": "紅外線", "default": False, "opacity": 0.8},
        "water_vapor": {"name": "水汽", "default": False, "opacity": 0.7},
    },
}

# 資料快取設定
CACHE_CONFIG = {
    "enable": True,
    "ttl": {
        "weather": 600,  # 10 分鐘
        "satellite": 1800,  # 30 分鐘
        "ocean": 3600,  # 1 小時
    },
    "max_size": 100,  # MB
}

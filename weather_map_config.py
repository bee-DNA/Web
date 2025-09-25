"""
即時天氣地圖配置檔案
整合天氣、雲圖、洋流等即時資料源
"""

# 天氣資料 API 配置
WEATHER_CONFIG = {
    # OpenWeatherMap API (需要申請免費 API Key)
    'OPENWEATHER': {
        'BASE_URL': 'https://api.openweathermap.org/data/2.5',
        'API_KEY': 'YOUR_OPENWEATHER_API_KEY',  # 請在 https://openweathermap.org/api 申請
        'ENDPOINTS': {
            'current': '/weather',
            'forecast': '/forecast',
            'onecall': '/onecall'
        }
    },
    
    # 天氣雲圖和雷達圖
    'WEATHER_LAYERS': {
        'precipitation': 'https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid={api_key}',
        'clouds': 'https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid={api_key}',
        'pressure': 'https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid={api_key}',
        'wind': 'https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid={api_key}',
        'temp': 'https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid={api_key}'
    }
}

# 海洋資料配置
OCEAN_CONFIG = {
    # NOAA 海洋資料
    'NOAA': {
        'BASE_URL': 'https://www.ncei.noaa.gov/thredds/wms',
        'DATASETS': {
            'sea_surface_temp': 'satellite/avhrr_pathfinder-pds-v52/pathfinder',
            'ocean_currents': 'ocean_atlas_2009/woa09/temperature_monthly_1deg.nc'
        }
    },
    
    # 海洋圖層
    'OCEAN_LAYERS': {
        'sea_surface_temperature': {
            'name': '海表溫度',
            'type': 'wms',
            'url': 'https://coastwatch.pfeg.noaa.gov/erddap/wms/jplAvisoSlaDaily/request',
            'layers': 'sla',
            'format': 'image/png',
            'transparent': True
        },
        'ocean_currents': {
            'name': '洋流',
            'type': 'vector',
            'description': '海流方向和速度'
        }
    }
}

# 衛星和雲圖配置
SATELLITE_CONFIG = {
    # NASA EOSDIS Worldview
    'NASA_WORLDVIEW': {
        'BASE_URL': 'https://map1.vis.earthdata.nasa.gov/wmts-geo/1.0.0',
        'LAYERS': {
            'modis_terra': 'MODIS_Terra_CorrectedReflectance_TrueColor',
            'modis_aqua': 'MODIS_Aqua_CorrectedReflectance_TrueColor',
            'viirs_snpp': 'VIIRS_SNPP_CorrectedReflectance_TrueColor'
        }
    },
    
    # 中央氣象署衛星雲圖
    'CWB_SATELLITE': {
        'BASE_URL': 'https://www.cwb.gov.tw/Data/satellite',
        'LAYERS': {
            'ir1': '紅外線雲圖',
            'vis': '可見光雲圖',
            'color': '彩色雲圖'
        }
    }
}

# 颱風和極端天氣配置
TYPHOON_CONFIG = {
    # 日本氣象廳 JMA
    'JMA': {
        'BASE_URL': 'https://www.jma.go.jp/bosai/forecast/data/forecast',
        'TYPHOON_URL': 'https://www.jma.go.jp/bosai/forecast/data/typhoon'
    },
    
    # 中央氣象署
    'CWB': {
        'BASE_URL': 'https://opendata.cwb.gov.tw/api',
        'API_KEY': 'YOUR_CWB_API_KEY',  # 請到 https://opendata.cwb.gov.tw/ 申請
        'TYPHOON_ENDPOINT': '/v1/rest/datastore/W-C0034-001'
    },
    
    # JTWC (Joint Typhoon Warning Center)
    'JTWC': {
        'BASE_URL': 'https://www.metoc.navy.mil/jtwc/products',
        'KML_URL': 'https://www.metoc.navy.mil/jtwc/products/sh{year}{basin}.dat'
    }
}

# 地圖樣式配置
MAP_STYLES = {
    'weather': {
        'name': '天氣地圖',
        'style': 'mapbox://styles/mapbox/light-v11',
        'default_layers': ['precipitation', 'clouds']
    },
    'ocean': {
        'name': '海洋地圖', 
        'style': 'mapbox://styles/mapbox/satellite-v9',
        'default_layers': ['sea_surface_temperature', 'ocean_currents']
    },
    'satellite': {
        'name': '衛星雲圖',
        'style': 'mapbox://styles/mapbox/satellite-streets-v12',
        'default_layers': ['modis_terra', 'typhoon_tracks']
    }
}

# 更新頻率設定
UPDATE_INTERVALS = {
    'weather_current': 600,    # 10 分鐘
    'weather_forecast': 3600,  # 1 小時
    'satellite_images': 1800,  # 30 分鐘
    'ocean_data': 21600,       # 6 小時
    'typhoon_tracks': 3600     # 1 小時
}

# 台灣地區預設視窗
TAIWAN_BOUNDS = {
    'center': {'lng': 121.0, 'lat': 23.8},
    'zoom': 7,
    'bounds': [
        [118.0, 21.5],  # 西南角
        [124.0, 26.5]   # 東北角
    ]
}

# 圖層控制配置
LAYER_CONTROLS = {
    'weather': {
        'precipitation': {'name': '降雨量', 'default': True, 'opacity': 0.7},
        'clouds': {'name': '雲層', 'default': True, 'opacity': 0.6},
        'wind': {'name': '風場', 'default': False, 'opacity': 0.8},
        'temperature': {'name': '溫度', 'default': False, 'opacity': 0.7},
        'pressure': {'name': '氣壓', 'default': False, 'opacity': 0.6}
    },
    'ocean': {
        'sea_temp': {'name': '海表溫度', 'default': True, 'opacity': 0.7},
        'currents': {'name': '洋流', 'default': True, 'opacity': 0.8},
        'waves': {'name': '海浪', 'default': False, 'opacity': 0.6}
    },
    'satellite': {
        'visible': {'name': '可見光', 'default': True, 'opacity': 1.0},
        'infrared': {'name': '紅外線', 'default': False, 'opacity': 0.8},
        'water_vapor': {'name': '水汽', 'default': False, 'opacity': 0.7}
    }
}

# 資料快取設定
CACHE_CONFIG = {
    'enable': True,
    'ttl': {
        'weather': 600,      # 10 分鐘
        'satellite': 1800,   # 30 分鐘  
        'ocean': 3600       # 1 小時
    },
    'max_size': 100  # MB
}
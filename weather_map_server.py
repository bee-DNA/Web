"""
即時天氣地圖後端 API 服務
整合多種氣象和海洋資料源
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from weather_map_config import *

app = Flask(__name__)
CORS(app)

class WeatherDataProcessor:
    """天氣資料處理器"""
    
    def __init__(self):
        self.cache = {}
        self.last_update = {}
    
    def is_cache_valid(self, data_type):
        """檢查快取是否有效"""
        if data_type not in self.last_update:
            return False
        
        ttl = CACHE_CONFIG['ttl'].get(data_type, 3600)
        return (time.time() - self.last_update[data_type]) < ttl
    
    def get_openweather_data(self, lat, lon, api_key):
        """取得 OpenWeatherMap 資料"""
        try:
            # 當前天氣
            current_url = f"{WEATHER_CONFIG['OPENWEATHER']['BASE_URL']}/weather"
            current_params = {
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'units': 'metric',
                'lang': 'zh_tw'
            }
            
            current_response = requests.get(current_url, params=current_params, timeout=10)
            current_data = current_response.json() if current_response.status_code == 200 else {}
            
            # 5天預報
            forecast_url = f"{WEATHER_CONFIG['OPENWEATHER']['BASE_URL']}/forecast"
            forecast_response = requests.get(forecast_url, params=current_params, timeout=10)
            forecast_data = forecast_response.json() if forecast_response.status_code == 200 else {}
            
            return {
                'current': current_data,
                'forecast': forecast_data,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"OpenWeather API 錯誤: {e}")
            return {'error': str(e)}
    
    def get_taiwan_weather_stations(self):
        """取得台灣主要氣象站資料"""
        stations = [
            {'name': '台北', 'lat': 25.0375, 'lng': 121.5625, 'id': 'taipei'},
            {'name': '新竹', 'lat': 24.8138, 'lng': 120.9675, 'id': 'hsinchu'},
            {'name': '台中', 'lat': 24.1477, 'lng': 120.6736, 'id': 'taichung'},
            {'name': '嘉義', 'lat': 23.4801, 'lng': 120.4491, 'id': 'chiayi'},
            {'name': '台南', 'lat': 22.9999, 'lng': 120.2269, 'id': 'tainan'},
            {'name': '高雄', 'lat': 22.6273, 'lng': 120.3014, 'id': 'kaohsiung'},
            {'name': '花蓮', 'lat': 23.9871, 'lng': 121.6015, 'id': 'hualien'},
            {'name': '台東', 'lat': 22.7972, 'lng': 121.1713, 'id': 'taitung'}
        ]
        
        return stations
    
    def create_weather_geojson(self, stations_data):
        """建立天氣資料的 GeoJSON 格式"""
        features = []
        
        for station in stations_data:
            if 'weather' in station and station['weather']:
                weather = station['weather']['current']
                
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [station['lng'], station['lat']]
                    },
                    "properties": {
                        "name": station['name'],
                        "station_id": station['id'],
                        "temperature": weather.get('main', {}).get('temp', 'N/A'),
                        "humidity": weather.get('main', {}).get('humidity', 'N/A'),
                        "pressure": weather.get('main', {}).get('pressure', 'N/A'),
                        "wind_speed": weather.get('wind', {}).get('speed', 'N/A'),
                        "wind_direction": weather.get('wind', {}).get('deg', 'N/A'),
                        "weather_main": weather.get('weather', [{}])[0].get('main', 'N/A'),
                        "weather_description": weather.get('weather', [{}])[0].get('description', 'N/A'),
                        "icon": weather.get('weather', [{}])[0].get('icon', '01d'),
                        "timestamp": station['weather']['timestamp']
                    }
                }
                features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features
        }

# 建立資料處理器實例
weather_processor = WeatherDataProcessor()

@app.route('/')
def index():
    """API 首頁"""
    return jsonify({
        "name": "即時天氣地圖 API",
        "version": "1.0.0",
        "description": "整合天氣、海洋、衛星資料的即時地圖 API",
        "endpoints": {
            "/api/weather/current": "當前天氣資料",
            "/api/weather/stations": "台灣氣象站資料", 
            "/api/layers/weather": "天氣圖層資訊",
            "/api/layers/ocean": "海洋圖層資訊",
            "/api/layers/satellite": "衛星圖層資訊",
            "/map/weather": "天氣地圖介面"
        }
    })

@app.route('/api/weather/current')
def get_current_weather():
    """取得指定位置的當前天氣"""
    lat = request.args.get('lat', 25.0375, type=float)  # 預設台北
    lon = request.args.get('lon', 121.5625, type=float)
    api_key = request.args.get('api_key', 'demo')  # 使用者需提供 API key
    
    if api_key == 'demo':
        return jsonify({
            "error": "需要 OpenWeather API Key",
            "message": "請在 https://openweathermap.org/api 申請免費 API Key"
        })
    
    weather_data = weather_processor.get_openweather_data(lat, lon, api_key)
    return jsonify(weather_data)

@app.route('/api/weather/stations')
def get_weather_stations():
    """取得台灣主要氣象站的天氣資料"""
    api_key = request.args.get('api_key', 'demo')
    
    if api_key == 'demo':
        # 提供模擬資料用於展示
        stations = weather_processor.get_taiwan_weather_stations()
        for station in stations:
            station['weather'] = {
                'current': {
                    'main': {
                        'temp': 25 + (hash(station['name']) % 10),
                        'humidity': 60 + (hash(station['name']) % 30),
                        'pressure': 1013 + (hash(station['name']) % 20)
                    },
                    'wind': {
                        'speed': 2 + (hash(station['name']) % 5),
                        'deg': hash(station['name']) % 360
                    },
                    'weather': [{
                        'main': '晴天',
                        'description': '晴朗',
                        'icon': '01d'
                    }]
                },
                'timestamp': datetime.now().isoformat()
            }
        
        geojson_data = weather_processor.create_weather_geojson(stations)
        return jsonify(geojson_data)
    
    # 實際 API 調用邏輯
    stations = weather_processor.get_taiwan_weather_stations()
    for station in stations:
        weather_data = weather_processor.get_openweather_data(
            station['lat'], station['lng'], api_key
        )
        station['weather'] = weather_data
    
    geojson_data = weather_processor.create_weather_geojson(stations)
    return jsonify(geojson_data)

@app.route('/api/layers/weather')
def get_weather_layers():
    """取得天氣圖層資訊"""
    return jsonify({
        "layers": WEATHER_CONFIG['WEATHER_LAYERS'],
        "controls": LAYER_CONTROLS['weather'],
        "update_interval": UPDATE_INTERVALS['weather_current']
    })

@app.route('/api/layers/ocean')
def get_ocean_layers():
    """取得海洋圖層資訊"""
    return jsonify({
        "layers": OCEAN_CONFIG['OCEAN_LAYERS'],
        "controls": LAYER_CONTROLS['ocean'],
        "update_interval": UPDATE_INTERVALS['ocean_data']
    })

@app.route('/api/layers/satellite')
def get_satellite_layers():
    """取得衛星圖層資訊"""
    return jsonify({
        "layers": SATELLITE_CONFIG['NASA_WORLDVIEW']['LAYERS'],
        "controls": LAYER_CONTROLS['satellite'],
        "update_interval": UPDATE_INTERVALS['satellite_images']
    })

@app.route('/api/config')
def get_map_config():
    """取得地圖配置資訊"""
    return jsonify({
        "map_styles": MAP_STYLES,
        "taiwan_bounds": TAIWAN_BOUNDS,
        "update_intervals": UPDATE_INTERVALS,
        "layer_controls": LAYER_CONTROLS
    })

@app.route('/map/weather')
def weather_map():
    """天氣地圖介面"""
    return render_template_string(WEATHER_MAP_TEMPLATE)

# HTML 模板
WEATHER_MAP_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>即時天氣海洋地圖</title>
    <script src='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.js'></script>
    <link href='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.css' rel='stylesheet' />
    <style>
        body { margin: 0; padding: 0; }
        .map-container { height: 100vh; width: 100%; position: relative; }
        #map { height: 100%; width: 100%; }
        .control-panel {
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            max-width: 300px;
        }
        .layer-control {
            margin: 5px 0;
        }
        .status-bar {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="map-container">
        <div id="map"></div>
        <div class="control-panel">
            <h3>🌦️ 圖層控制</h3>
            <div id="layer-controls"></div>
            <button onclick="refreshData()">🔄 更新資料</button>
        </div>
        <div class="status-bar" id="status">
            載入中...
        </div>
    </div>

    <script>
        // 注意：您需要設定 Mapbox Access Token
        mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w';
        
        const map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/light-v11',
            center: [121.0, 23.8], // 台灣中心
            zoom: 7
        });

        map.on('load', async () => {
            await loadWeatherStations();
            updateStatus('地圖載入完成');
        });

        async function loadWeatherStations() {
            try {
                const response = await fetch('/api/weather/stations');
                const geojsonData = await response.json();
                
                // 添加氣象站資料源
                map.addSource('weather-stations', {
                    'type': 'geojson',
                    'data': geojsonData
                });

                // 添加氣象站點圖層
                map.addLayer({
                    'id': 'weather-points',
                    'type': 'circle',
                    'source': 'weather-stations',
                    'paint': {
                        'circle-radius': 8,
                        'circle-color': [
                            'interpolate',
                            ['linear'],
                            ['get', 'temperature'],
                            10, '#0000ff',  // 藍色 (低溫)
                            25, '#00ff00',  // 綠色 (適中)
                            35, '#ff0000'   // 紅色 (高溫)
                        ],
                        'circle-stroke-width': 2,
                        'circle-stroke-color': '#ffffff'
                    }
                });

                // 添加溫度標籤
                map.addLayer({
                    'id': 'weather-labels',
                    'type': 'symbol',
                    'source': 'weather-stations',
                    'layout': {
                        'text-field': '{temperature}°C',
                        'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
                        'text-size': 12,
                        'text-offset': [0, -2]
                    },
                    'paint': {
                        'text-color': '#000000',
                        'text-halo-color': '#ffffff',
                        'text-halo-width': 1
                    }
                });

                // 添加點擊事件
                map.on('click', 'weather-points', (e) => {
                    const properties = e.features[0].properties;
                    new mapboxgl.Popup()
                        .setLngLat(e.lngLat)
                        .setHTML(`
                            <h3>${properties.name}</h3>
                            <p><strong>溫度:</strong> ${properties.temperature}°C</p>
                            <p><strong>濕度:</strong> ${properties.humidity}%</p>
                            <p><strong>氣壓:</strong> ${properties.pressure} hPa</p>
                            <p><strong>風速:</strong> ${properties.wind_speed} m/s</p>
                            <p><strong>天氣:</strong> ${properties.weather_description}</p>
                        `)
                        .addTo(map);
                });

                updateStatus('氣象站資料載入完成');
            } catch (error) {
                console.error('載入氣象站資料失敗:', error);
                updateStatus('載入失敗: ' + error.message);
            }
        }

        function updateStatus(message) {
            document.getElementById('status').textContent = `${new Date().toLocaleTimeString()} - ${message}`;
        }

        function refreshData() {
            updateStatus('更新資料中...');
            loadWeatherStations();
        }

        // 自動更新資料 (每10分鐘)
        setInterval(refreshData, 10 * 60 * 1000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("🌦️ 即時天氣地圖 API 服務啟動中...")
    print("📍 地圖介面: http://localhost:5000/map/weather")
    print("📡 API 文件: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
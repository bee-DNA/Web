"""
全球即時天氣海洋地圖系統後端 API 服務
整合天氣、雲圖、洋流、颱風、衛星影像等多種資料源
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from weather_map_config import *
import threading

app = Flask(__name__)
CORS(app)


class GlobalWeatherProcessor:
    """全球天氣資料處理器"""

    def __init__(self):
        self.cache = {}
        self.last_update = {}
        self.api_keys = {
            "openweather": WEATHER_CONFIG["OPENWEATHER"]["API_KEY"],
            "noaa": OCEAN_CONFIG["NOAA"]["API_KEY"],
            "nasa": SATELLITE_CONFIG["NASA_WORLDVIEW"]["API_TOKEN"],
        }

    def is_cache_valid(self, data_type):
        """檢查快取是否有效"""
        if data_type not in self.last_update:
            return False

        ttl = UPDATE_INTERVALS.get(data_type, 7200)  # 預設2小時
        return (time.time() - self.last_update[data_type]) < ttl

    def get_global_weather_stations(self):
        """取得全球主要城市氣象站列表"""
        all_stations = []

        for region, stations in GLOBAL_WEATHER_STATIONS.items():
            for station in stations:
                station["region"] = region
                station["id"] = f"{region}_{station['name'].replace(' ', '_').lower()}"
                all_stations.append(station)

        return all_stations

    def get_openweather_data(self, lat, lon, station_id=None):
        """取得 OpenWeatherMap 資料"""
        try:
            api_key = self.api_keys["openweather"]

            # 當前天氣
            current_url = f"{WEATHER_CONFIG['OPENWEATHER']['BASE_URL']}/weather"
            current_params = {
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "units": "metric",
                "lang": "zh_tw",
            }

            current_response = requests.get(
                current_url, params=current_params, timeout=10
            )
            current_data = (
                current_response.json() if current_response.status_code == 200 else {}
            )

            # 5天預報
            forecast_url = f"{WEATHER_CONFIG['OPENWEATHER']['BASE_URL']}/forecast"
            forecast_response = requests.get(
                forecast_url, params=current_params, timeout=10
            )
            forecast_data = (
                forecast_response.json() if forecast_response.status_code == 200 else {}
            )

            # One Call API (包含更詳細資訊)
            onecall_url = f"{WEATHER_CONFIG['OPENWEATHER']['BASE_URL']}/onecall"
            onecall_params = {
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "units": "metric",
                "exclude": "minutely,alerts",
            }
            onecall_response = requests.get(
                onecall_url, params=onecall_params, timeout=10
            )
            onecall_data = (
                onecall_response.json() if onecall_response.status_code == 200 else {}
            )

            return {
                "current": current_data,
                "forecast": forecast_data,
                "onecall": onecall_data,
                "timestamp": datetime.now().isoformat(),
                "station_id": station_id,
            }

        except Exception as e:
            print(f"OpenWeather API 錯誤 ({lat}, {lon}): {e}")
            return {"error": str(e), "station_id": station_id}

    def get_weather_layers_data(self):
        """取得天氣圖層資料"""
        api_key = self.api_keys["openweather"]

        layers = {}
        for layer_name, layer_config in WEATHER_CONFIG["WEATHER_LAYERS"].items():
            layers[layer_name] = {
                "url": layer_config.format(api_key=api_key),
                "name": layer_name,
                "opacity": LAYER_CONTROLS["weather"]
                .get(layer_name, {})
                .get("opacity", 0.7),
            }

        return layers

    def get_satellite_layers_data(self):
        """取得衛星圖層資料"""
        layers = {}
        base_url = SATELLITE_CONFIG["NASA_WORLDVIEW"]["BASE_URL"]

        for layer_id, layer_name in SATELLITE_CONFIG["NASA_WORLDVIEW"][
            "LAYERS"
        ].items():
            today = datetime.now().strftime("%Y-%m-%d")
            layers[layer_id] = {
                "url": f"{base_url}/{layer_name}/default/{today}/GoogleMapsCompatible_Level9/{{z}}/{{y}}/{{x}}.jpg",
                "name": layer_id,
                "opacity": 1.0,
                "attribution": "© NASA Worldview",
            }

        return layers

    def get_ocean_data(self):
        """取得海洋資料 (模擬)"""
        # 這裡可以整合實際的 NOAA API 資料
        return {
            "sea_surface_temperature": {
                "url": "https://coastwatch.pfeg.noaa.gov/erddap/wms/jplMURSST41/request",
                "layers": "analysed_sst",
                "format": "image/png",
                "transparent": True,
                "attribution": "© NOAA",
            },
            "ocean_currents": {
                "type": "vector",
                "description": "海流資料需要進一步整合",
            },
        }

    def create_global_weather_geojson(self, weather_data_list):
        """建立全球天氣資料的 GeoJSON 格式"""
        features = []

        for data in weather_data_list:
            if data.get("error"):
                continue

            station = data.get("station_info", {})
            weather = data.get("current", {})

            if not weather or "main" not in weather:
                continue

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [station.get("lng", 0), station.get("lat", 0)],
                },
                "properties": {
                    "name": station.get("name", "Unknown"),
                    "country": station.get("country", "Unknown"),
                    "region": station.get("region", "Unknown"),
                    "station_id": station.get("id", ""),
                    "temperature": weather.get("main", {}).get("temp", "N/A"),
                    "feels_like": weather.get("main", {}).get("feels_like", "N/A"),
                    "humidity": weather.get("main", {}).get("humidity", "N/A"),
                    "pressure": weather.get("main", {}).get("pressure", "N/A"),
                    "wind_speed": weather.get("wind", {}).get("speed", "N/A"),
                    "wind_direction": weather.get("wind", {}).get("deg", "N/A"),
                    "visibility": weather.get("visibility", "N/A"),
                    "weather_main": weather.get("weather", [{}])[0].get("main", "N/A"),
                    "weather_description": weather.get("weather", [{}])[0].get(
                        "description", "N/A"
                    ),
                    "icon": weather.get("weather", [{}])[0].get("icon", "01d"),
                    "timestamp": data.get("timestamp", ""),
                    "uv_index": data.get("onecall", {})
                    .get("current", {})
                    .get("uvi", "N/A"),
                    "clouds": weather.get("clouds", {}).get("all", "N/A"),
                },
            }
            features.append(feature)

        return {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "total_stations": len(features),
                "last_update": datetime.now().isoformat(),
                "coverage": "global",
            },
        }


# 建立全球資料處理器實例
weather_processor = GlobalWeatherProcessor()


@app.route("/")
def index():
    """API 首頁"""
    return jsonify(
        {
            "name": "全球即時天氣海洋地圖 API",
            "version": "2.0.0",
            "description": "整合全球天氣、海洋、衛星、颱風資料的即時地圖 API",
            "features": [
                "🌍 全球範圍天氣資料",
                "☁️ 即時雲圖和衛星影像",
                "🌊 海表溫度和洋流資料",
                "🌀 颱風路徑追蹤",
                "🌡️ 即時天氣 (溫度、風速、降雨)",
                "⏰ 每2小時定時更新",
            ],
            "endpoints": {
                "/api/weather/global": "全球氣象站資料",
                "/api/weather/current": "指定位置當前天氣",
                "/api/layers/weather": "天氣圖層資訊",
                "/api/layers/satellite": "衛星圖層資訊",
                "/api/layers/ocean": "海洋圖層資訊",
                "/api/typhoon/tracks": "颱風路徑資料",
                "/map/global": "全球天氣地圖介面",
            },
            "api_keys_status": {
                "openweather": "✅ 已配置",
                "nasa_earthdata": "✅ 已配置",
                "noaa": "✅ 已配置",
            },
        }
    )


@app.route("/api/weather/global")
def get_global_weather():
    """取得全球主要城市的天氣資料"""
    try:
        # 檢查快取
        if weather_processor.is_cache_valid("weather_current"):
            cached_data = weather_processor.cache.get("weather_current")
            if cached_data:
                return jsonify(cached_data)

        stations = weather_processor.get_global_weather_stations()
        weather_data_list = []

        # 限制並發請求數量以避免API限制
        for station in stations[:30]:  # 限制前30個城市
            try:
                weather_data = weather_processor.get_openweather_data(
                    station["lat"], station["lng"], station["id"]
                )
                weather_data["station_info"] = station
                weather_data_list.append(weather_data)

                # 避免API請求過於頻繁
                time.sleep(0.1)

            except Exception as e:
                print(f"獲取 {station['name']} 天氣資料失敗: {e}")
                continue

        geojson_data = weather_processor.create_global_weather_geojson(
            weather_data_list
        )

        # 快取資料
        weather_processor.cache["weather_current"] = geojson_data
        weather_processor.last_update["weather_current"] = time.time()

        return jsonify(geojson_data)

    except Exception as e:
        print(f"全球天氣資料獲取失敗: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/weather/current")
def get_current_weather():
    """取得指定位置的當前天氣"""
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "需要提供 lat 和 lon 參數"}), 400

    weather_data = weather_processor.get_openweather_data(lat, lon)
    return jsonify(weather_data)


@app.route("/api/layers/weather")
def get_weather_layers():
    """取得天氣圖層資訊"""
    layers = weather_processor.get_weather_layers_data()
    return jsonify(
        {
            "layers": layers,
            "controls": LAYER_CONTROLS["weather"],
            "update_interval": UPDATE_INTERVALS["weather_current"],
        }
    )


@app.route("/api/layers/satellite")
def get_satellite_layers():
    """取得衛星圖層資訊"""
    layers = weather_processor.get_satellite_layers_data()
    return jsonify(
        {
            "layers": layers,
            "controls": LAYER_CONTROLS["satellite"],
            "update_interval": UPDATE_INTERVALS["satellite_images"],
        }
    )


@app.route("/api/layers/ocean")
def get_ocean_layers():
    """取得海洋圖層資訊"""
    layers = weather_processor.get_ocean_data()
    return jsonify(
        {
            "layers": layers,
            "controls": LAYER_CONTROLS["ocean"],
            "update_interval": UPDATE_INTERVALS["ocean_data"],
        }
    )


@app.route("/api/typhoon/tracks")
def get_typhoon_tracks():
    """取得颱風路徑資料 (模擬)"""
    # 這裡可以整合實際的颱風追蹤API
    return jsonify(
        {
            "message": "颱風路徑追蹤功能開發中",
            "features": [],
            "last_update": datetime.now().isoformat(),
        }
    )


@app.route("/api/config/global")
def get_global_config():
    """取得全球地圖配置資訊"""
    return jsonify(
        {
            "global_bounds": GLOBAL_BOUNDS,
            "taiwan_bounds": TAIWAN_BOUNDS,
            "map_styles": MAP_STYLES,
            "update_intervals": UPDATE_INTERVALS,
            "layer_controls": LAYER_CONTROLS,
            "global_stations": GLOBAL_WEATHER_STATIONS,
        }
    )


@app.route("/map/global")
def global_weather_map():
    """全球天氣地圖介面"""
    return render_template_string(GLOBAL_MAP_TEMPLATE)


# 自動更新背景任務
def auto_update_task():
    """背景自動更新任務"""
    while True:
        try:
            print(
                f"🔄 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 開始自動更新全球天氣資料"
            )

            # 清除舊快取
            weather_processor.cache.clear()
            weather_processor.last_update.clear()

            # 預先載入資料
            with app.test_request_context():
                get_global_weather()

            print("✅ 全球天氣資料更新完成")

            # 等待2小時
            time.sleep(UPDATE_INTERVALS["weather_current"])

        except Exception as e:
            print(f"❌ 自動更新失敗: {e}")
            time.sleep(300)  # 失敗後等待5分鐘再試


# HTML 模板
GLOBAL_MAP_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌍 全球即時天氣海洋地圖</title>
    <script src='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.js'></script>
    <link href='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.css' rel='stylesheet' />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f5f7fa; }
        .container { display: flex; height: 100vh; }
        
        .sidebar {
            width: 380px; background: white;
            box-shadow: 2px 0 15px rgba(0,0,0,0.1);
            overflow-y: auto; z-index: 1000;
        }
        
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 25px;
        }
        
        .sidebar-header h1 { font-size: 1.6rem; margin-bottom: 0.5rem; }
        .sidebar-header p { opacity: 0.9; font-size: 0.95rem; }
        
        .sidebar-content { padding: 25px; }
        .section { margin-bottom: 30px; }
        .section-title {
            font-size: 1.1rem; font-weight: 600; margin-bottom: 15px;
            color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;
        }
        
        .map-container { flex: 1; position: relative; }
        #map { height: 100%; width: 100%; }
        
        .map-controls {
            position: absolute; top: 15px; right: 15px;
            display: flex; flex-direction: column; gap: 10px;
        }
        
        .control-button {
            background: white; border: none; padding: 12px 16px;
            border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            cursor: pointer; font-size: 0.9rem; transition: all 0.2s;
        }
        
        .control-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .status-bar {
            position: absolute; bottom: 15px; left: 15px;
            background: rgba(0,0,0,0.85); color: white;
            padding: 10px 20px; border-radius: 25px;
            font-size: 0.85rem; backdrop-filter: blur(10px);
        }
        
        .legend {
            position: absolute; bottom: 15px; right: 15px;
            background: white; padding: 20px; border-radius: 10px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1); min-width: 220px;
        }
        
        .legend-title { font-weight: bold; margin-bottom: 12px; color: #2c3e50; }
        .legend-item { display: flex; align-items: center; margin-bottom: 8px; }
        .legend-color { width: 25px; height: 18px; margin-right: 10px; border-radius: 4px; }
        
        .weather-card {
            background: #f8f9fa; border-radius: 10px; padding: 18px;
            margin-bottom: 15px; border-left: 4px solid #3498db;
            cursor: pointer; transition: all 0.2s;
        }
        
        .weather-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .weather-station { font-weight: bold; margin-bottom: 10px; color: #2c3e50; }
        .weather-data {
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 10px; font-size: 0.9rem;
        }
        
        .loading {
            display: inline-block; width: 24px; height: 24px;
            border: 3px solid rgba(52,152,219,0.3); border-radius: 50%;
            border-top-color: #3498db; animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .region-filter {
            display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;
        }
        
        .region-btn {
            padding: 6px 12px; border: 1px solid #3498db; background: white;
            color: #3498db; border-radius: 20px; font-size: 0.8rem;
            cursor: pointer; transition: all 0.2s;
        }
        
        .region-btn.active, .region-btn:hover {
            background: #3498db; color: white;
        }
        
        .stats-grid {
            display: grid; grid-template-columns: 1fr 1fr; gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: white; padding: 15px; border-radius: 8px;
            text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .stat-value { font-size: 1.8rem; font-weight: bold; color: #3498db; }
        .stat-label { font-size: 0.8rem; color: #7f8c8d; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="sidebar-header">
                <h1>🌍 全球天氣地圖</h1>
                <p>即時天氣、雲圖、海洋資料視覺化</p>
            </div>

            <div class="sidebar-content">
                <div class="section">
                    <div class="section-title">📊 全球統計</div>
                    <div class="stats-grid" id="global-stats">
                        <div class="stat-card">
                            <div class="stat-value" id="total-stations">--</div>
                            <div class="stat-label">監測站點</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="avg-temp">--°C</div>
                            <div class="stat-label">平均溫度</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">🌏 地區篩選</div>
                    <div class="region-filter">
                        <button class="region-btn active" onclick="filterByRegion('all')">全部</button>
                        <button class="region-btn" onclick="filterByRegion('asia')">亞洲</button>
                        <button class="region-btn" onclick="filterByRegion('europe')">歐洲</button>
                        <button class="region-btn" onclick="filterByRegion('americas')">美洲</button>
                        <button class="region-btn" onclick="filterByRegion('oceania')">大洋洲</button>
                        <button class="region-btn" onclick="filterByRegion('africa')">非洲</button>
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">🌦️ 即時天氣</div>
                    <div id="weather-data">
                        <div class="loading"></div> 載入全球天氣資料中...
                    </div>
                </div>
            </div>
        </div>

        <div class="map-container">
            <div id="map"></div>

            <div class="map-controls">
                <button class="control-button" onclick="refreshAllData()">🔄 更新資料</button>
                <button class="control-button" onclick="toggleFullscreen()">📺 全螢幕</button>
                <button class="control-button" onclick="showGlobalView()">🌍 全球視圖</button>
                <button class="control-button" onclick="showTaiwanView()">🇹🇼 台灣視圖</button>
            </div>

            <div class="status-bar" id="status">初始化全球地圖中...</div>

            <div class="legend">
                <div class="legend-title">溫度圖例</div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #0000ff;"></div>
                    <span>< 0°C (極寒)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #00ffff;"></div>
                    <span>0-10°C (寒冷)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #00ff00;"></div>
                    <span>10-20°C (涼爽)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ffff00;"></div>
                    <span>20-30°C (溫暖)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff8000;"></div>
                    <span>30-40°C (炎熱)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff0000;"></div>
                    <span>> 40°C (酷熱)</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w';
        
        let map, globalWeatherData, currentFilter = 'all';

        function initMap() {
            map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/light-v11',
                center: [0, 20], // 全球中心
                zoom: 2,
                pitch: 0,
                bearing: 0
            });

            map.on('load', () => {
                updateStatus('全球地圖載入完成');
                loadGlobalWeatherData();
                setupMapLayers();
            });

            map.addControl(new mapboxgl.NavigationControl());
            map.addControl(new mapboxgl.ScaleControl());
        }

        async function loadGlobalWeatherData() {
            try {
                updateStatus('載入全球天氣資料...');
                
                const response = await fetch('/api/weather/global');
                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                globalWeatherData = data;
                
                if (map.getSource('global-weather')) {
                    map.getSource('global-weather').setData(data);
                } else {
                    map.addSource('global-weather', {
                        'type': 'geojson',
                        'data': data
                    });
                }

                updateWeatherSidebar(data);
                updateGlobalStats(data);
                updateStatus('全球天氣資料載入完成');

            } catch (error) {
                console.error('載入全球天氣資料失敗:', error);
                updateStatus('載入失敗: ' + error.message);
            }
        }

        function setupMapLayers() {
            if (!globalWeatherData) return;

            // 氣象站點圖層
            if (!map.getLayer('weather-points')) {
                map.addLayer({
                    'id': 'weather-points',
                    'type': 'circle',
                    'source': 'global-weather',
                    'paint': {
                        'circle-radius': [
                            'interpolate', ['linear'], ['zoom'],
                            2, 4, 8, 8, 12, 12
                        ],
                        'circle-color': [
                            'interpolate', ['linear'], ['get', 'temperature'],
                            -20, '#0000ff', 0, '#00ffff', 10, '#00ff00',
                            20, '#ffff00', 30, '#ff8000', 40, '#ff0000'
                        ],
                        'circle-stroke-width': 2,
                        'circle-stroke-color': '#ffffff',
                        'circle-opacity': 0.8
                    }
                });
            }

            // 溫度標籤
            if (!map.getLayer('temperature-labels')) {
                map.addLayer({
                    'id': 'temperature-labels',
                    'type': 'symbol',
                    'source': 'global-weather',
                    'layout': {
                        'text-field': '{temperature}°',
                        'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
                        'text-size': ['interpolate', ['linear'], ['zoom'], 2, 8, 8, 12],
                        'text-offset': [0, -2], 'text-anchor': 'center'
                    },
                    'paint': {
                        'text-color': '#2c3e50',
                        'text-halo-color': '#ffffff',
                        'text-halo-width': 2
                    }
                });
            }

            // 城市名稱標籤
            if (!map.getLayer('city-labels')) {
                map.addLayer({
                    'id': 'city-labels',
                    'type': 'symbol',
                    'source': 'global-weather',
                    'layout': {
                        'text-field': '{name}',
                        'text-font': ['Open Sans Regular', 'Arial Unicode MS Regular'],
                        'text-size': ['interpolate', ['linear'], ['zoom'], 2, 8, 8, 11],
                        'text-offset': [0, 2], 'text-anchor': 'center'
                    },
                    'paint': {
                        'text-color': '#34495e',
                        'text-halo-color': '#ffffff',
                        'text-halo-width': 1.5
                    }
                });
            }

            map.on('click', 'weather-points', handleWeatherPointClick);
            map.on('mouseenter', 'weather-points', () => map.getCanvas().style.cursor = 'pointer');
            map.on('mouseleave', 'weather-points', () => map.getCanvas().style.cursor = '');
        }

        function handleWeatherPointClick(e) {
            const props = e.features[0].properties;
            
            const popup = new mapboxgl.Popup({ offset: [0, -15] })
                .setLngLat(e.lngLat)
                .setHTML(`
                    <div style="min-width: 280px; font-family: Arial;">
                        <h3 style="margin: 0 0 15px 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;">
                            🌍 ${props.name}, ${props.country}
                        </h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 15px;">
                            <div style="background: #ecf0f1; padding: 10px; border-radius: 6px; text-align: center;">
                                <strong>🌡️ 溫度</strong><br>
                                <span style="font-size: 20px; color: #e74c3c;">${props.temperature}°C</span><br>
                                <small>體感 ${props.feels_like}°C</small>
                            </div>
                            <div style="background: #ecf0f1; padding: 10px; border-radius: 6px; text-align: center;">
                                <strong>💧 濕度</strong><br>
                                <span style="font-size: 18px; color: #3498db;">${props.humidity}%</span>
                            </div>
                            <div style="background: #ecf0f1; padding: 10px; border-radius: 6px; text-align: center;">
                                <strong>📊 氣壓</strong><br>
                                <span style="font-size: 14px;">${props.pressure} hPa</span>
                            </div>
                            <div style="background: #ecf0f1; padding: 10px; border-radius: 6px; text-align: center;">
                                <strong>💨 風速</strong><br>
                                <span style="font-size: 14px;">${props.wind_speed} m/s</span>
                            </div>
                        </div>
                        <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
                            <strong>☁️ 天氣:</strong> ${props.weather_description}<br>
                            <strong>👁️ 能見度:</strong> ${props.visibility}m<br>
                            <strong>☀️ UV指數:</strong> ${props.uv_index}
                        </div>
                        <small style="color: #7f8c8d;">
                            📅 ${new Date(props.timestamp).toLocaleString('zh-TW')}
                        </small>
                    </div>
                `)
                .addTo(map);
        }

        function updateWeatherSidebar(data) {
            const weatherDataDiv = document.getElementById('weather-data');
            
            if (!data.features || data.features.length === 0) {
                weatherDataDiv.innerHTML = '<p>暫無天氣資料</p>';
                return;
            }

            let filteredFeatures = data.features;
            if (currentFilter !== 'all') {
                filteredFeatures = data.features.filter(f => f.properties.region === currentFilter);
            }

            const weatherCards = filteredFeatures.map(feature => {
                const props = feature.properties;
                return `
                    <div class="weather-card" onclick="focusOnStation(${feature.geometry.coordinates[0]}, ${feature.geometry.coordinates[1]})">
                        <div class="weather-station">${props.name}, ${props.country}</div>
                        <div class="weather-data">
                            <div><strong>溫度:</strong> ${props.temperature}°C</div>
                            <div><strong>體感:</strong> ${props.feels_like}°C</div>
                            <div><strong>濕度:</strong> ${props.humidity}%</div>
                            <div><strong>風速:</strong> ${props.wind_speed} m/s</div>
                        </div>
                    </div>
                `;
            }).join('');

            weatherDataDiv.innerHTML = weatherCards || '<p>此地區暫無資料</p>';
        }

        function updateGlobalStats(data) {
            if (!data.features) return;

            const temperatures = data.features
                .map(f => f.properties.temperature)
                .filter(t => t !== 'N/A' && !isNaN(t));
            
            const totalStations = data.features.length;
            const avgTemp = temperatures.length > 0 ? 
                (temperatures.reduce((a, b) => a + b, 0) / temperatures.length).toFixed(1) : '--';

            document.getElementById('total-stations').textContent = totalStations;
            document.getElementById('avg-temp').textContent = avgTemp + '°C';
        }

        function filterByRegion(region) {
            currentFilter = region;
            
            // 更新按鈕狀態
            document.querySelectorAll('.region-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // 更新地圖篩選
            if (region === 'all') {
                map.setFilter('weather-points', null);
                map.setFilter('temperature-labels', null);
                map.setFilter('city-labels', null);
            } else {
                const filter = ['==', ['get', 'region'], region];
                map.setFilter('weather-points', filter);
                map.setFilter('temperature-labels', filter);
                map.setFilter('city-labels', filter);
            }
            
            updateWeatherSidebar(globalWeatherData);
        }

        function focusOnStation(lng, lat) {
            map.flyTo({
                center: [lng, lat],
                zoom: 8,
                duration: 1500
            });
        }

        function refreshAllData() {
            updateStatus('刷新全球資料中...');
            loadGlobalWeatherData();
        }

        function showGlobalView() {
            map.flyTo({
                center: [0, 20],
                zoom: 2,
                duration: 2000
            });
        }

        function showTaiwanView() {
            map.flyTo({
                center: [121.0, 23.8],
                zoom: 7,
                duration: 2000
            });
        }

        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }

        function updateStatus(message) {
            const now = new Date().toLocaleTimeString('zh-TW');
            document.getElementById('status').textContent = `${now} - ${message}`;
        }

        // 初始化
        window.addEventListener('load', initMap);

        // 自動更新 (每2小時)
        setInterval(refreshAllData, 2 * 60 * 60 * 1000);
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    print("🌍 全球即時天氣海洋地圖系統啟動中...")
    print("📍 全球地圖介面: http://localhost:5001/map/global")
    print("📡 API 文件: http://localhost:5001")
    print("🔑 已配置 API Keys:")
    print("   ✅ OpenWeather API")
    print("   ✅ NASA Earthdata API")
    print("   ✅ NOAA API")
    print("⏰ 自動更新間隔: 每2小時")

    # 啟動背景自動更新任務
    update_thread = threading.Thread(target=auto_update_task, daemon=True)
    update_thread.start()

    app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)

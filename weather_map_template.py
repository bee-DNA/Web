"""
進階天氣地圖 HTML 介面
包含完整的圖層控制和即時資料顯示
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-TW">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌦️ 即時天氣海洋地圖系統</title>

    <!-- Mapbox GL JS -->
    <script src='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.js'></script>
    <link href='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.css' rel='stylesheet' />

    <!-- 樣式 -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
        }

        .container {
            display: flex;
            height: 100vh;
        }

        .sidebar {
            width: 350px;
            background: white;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            overflow-y: auto;
        }

        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }

        .sidebar-header h1 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }

        .sidebar-content {
            padding: 20px;
        }

        .section {
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }

        .layer-group {
            margin-bottom: 20px;
        }

        .layer-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #ecf0f1;
        }

        .layer-checkbox {
            margin-right: 10px;
        }

        .layer-name {
            flex: 1;
            font-size: 0.9rem;
        }

        .opacity-slider {
            width: 60px;
            margin-left: 10px;
        }

        .weather-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
        }

        .weather-station {
            font-weight: bold;
            margin-bottom: 8px;
            color: #2c3e50;
        }

        .weather-data {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            font-size: 0.85rem;
        }

        .map-container {
            flex: 1;
            position: relative;
        }

        #map {
            height: 100%;
            width: 100%;
        }

        .map-controls {
            position: absolute;
            top: 15px;
            right: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .control-button {
            background: white;
            border: none;
            padding: 10px 15px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .control-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        .status-bar {
            position: absolute;
            bottom: 15px;
            left: 15px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            backdrop-filter: blur(10px);
        }

        .legend {
            position: absolute;
            bottom: 15px;
            right: 15px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            min-width: 200px;
        }

        .legend-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }

        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }

        .legend-color {
            width: 20px;
            height: 15px;
            margin-right: 8px;
            border-radius: 3px;
        }

        .api-key-input {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        .btn-primary {
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin-bottom: 10px;
        }

        .btn-primary:hover {
            background: #2980b9;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(52, 152, 219, 0.3);
            border-radius: 50%;
            border-top-color: #3498db;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .error-message {
            background: #e74c3c;
            color: white;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: 250px;
            }
            
            .map-container {
                height: calc(100vh - 250px);
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <!-- 側邊欄 -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h1>🌦️ 天氣海洋地圖</h1>
                <p>即時氣象與海洋資料視覺化</p>
            </div>

            <div class="sidebar-content">
                <!-- API 金鑰設定 -->
                <div class="section">
                    <div class="section-title">🔑 API 設定</div>
                    <input type="password" 
                           id="api-key-input" 
                           class="api-key-input" 
                           placeholder="輸入 OpenWeather API Key (可選)">
                    <button class="btn-primary" onclick="updateApiKey()">
                        設定 API Key
                    </button>
                    <small>💡 不設定將使用示範資料</small>
                </div>

                <!-- 圖層控制 -->
                <div class="section">
                    <div class="section-title">🗺️ 圖層控制</div>
                    
                    <!-- 天氣圖層 -->
                    <div class="layer-group">
                        <h4>☁️ 天氣圖層</h4>
                        <div id="weather-layers"></div>
                    </div>

                    <!-- 海洋圖層 -->
                    <div class="layer-group">
                        <h4>🌊 海洋圖層</h4>
                        <div id="ocean-layers"></div>
                    </div>

                    <!-- 衛星圖層 -->
                    <div class="layer-group">
                        <h4>🛰️ 衛星圖層</h4>
                        <div id="satellite-layers"></div>
                    </div>
                </div>

                <!-- 即時資料 -->
                <div class="section">
                    <div class="section-title">📊 即時資料</div>
                    <div id="weather-data">
                        <div class="loading"></div> 載入中...
                    </div>
                </div>
            </div>
        </div>

        <!-- 地圖容器 -->
        <div class="map-container">
            <div id="map"></div>

            <!-- 地圖控制按鈕 -->
            <div class="map-controls">
                <button class="control-button" onclick="refreshAllData()">
                    🔄 更新資料
                </button>
                <button class="control-button" onclick="toggleFullscreen()">
                    📺 全螢幕
                </button>
                <button class="control-button" onclick="centerOnTaiwan()">
                    🇹🇼 回到台灣
                </button>
            </div>

            <!-- 狀態列 -->
            <div class="status-bar" id="status">
                初始化地圖中...
            </div>

            <!-- 圖例 -->
            <div class="legend">
                <div class="legend-title">溫度圖例</div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #0000ff;"></div>
                    <span>< 15°C (低溫)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #00ff00;"></div>
                    <span>15-30°C (適中)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff0000;"></div>
                    <span>> 30°C (高溫)</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Mapbox 設定
        mapboxgl.accessToken = 'pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w';
        
        // 全域變數
        let map;
        let currentApiKey = null;
        let weatherStationsData = null;
        let updateInterval = null;

        // 初始化地圖
        function initMap() {
            map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/light-v11',
                center: [121.0, 23.8], // 台灣中心
                zoom: 7,
                pitch: 0,
                bearing: 0
            });

            map.on('load', () => {
                updateStatus('地圖載入完成');
                loadInitialData();
                setupMapLayers();
                startAutoUpdate();
            });

            // 添加導航控制
            map.addControl(new mapboxgl.NavigationControl());
            
            // 添加比例尺
            map.addControl(new mapboxgl.ScaleControl());
        }

        // 載入初始資料
        async function loadInitialData() {
            try {
                await loadWeatherStations();
                await loadMapConfig();
                updateStatus('初始資料載入完成');
            } catch (error) {
                console.error('載入初始資料失敗:', error);
                updateStatus('載入失敗: ' + error.message);
            }
        }

        // 載入氣象站資料
        async function loadWeatherStations() {
            try {
                updateStatus('載入氣象站資料...');
                
                let url = '/api/weather/stations';
                if (currentApiKey) {
                    url += '?api_key=' + encodeURIComponent(currentApiKey);
                }

                const response = await fetch(url);
                const geojsonData = await response.json();

                if (geojsonData.error) {
                    throw new Error(geojsonData.message || geojsonData.error);
                }

                weatherStationsData = geojsonData;

                // 更新或添加資料源
                if (map.getSource('weather-stations')) {
                    map.getSource('weather-stations').setData(geojsonData);
                } else {
                    map.addSource('weather-stations', {
                        'type': 'geojson',
                        'data': geojsonData
                    });
                }

                // 更新側邊欄天氣資料
                updateWeatherSidebar(geojsonData);
                
                updateStatus('氣象站資料更新完成');
            } catch (error) {
                console.error('載入氣象站資料失敗:', error);
                updateStatus('載入氣象站資料失敗: ' + error.message);
                showError('載入氣象站資料失敗: ' + error.message);
            }
        }

        // 設定地圖圖層
        function setupMapLayers() {
            if (!weatherStationsData) return;

            try {
                // 氣象站點圖層
                if (!map.getLayer('weather-points')) {
                    map.addLayer({
                        'id': 'weather-points',
                        'type': 'circle',
                        'source': 'weather-stations',
                        'paint': {
                            'circle-radius': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                6, 8,
                                12, 15
                            ],
                            'circle-color': [
                                'interpolate',
                                ['linear'],
                                ['get', 'temperature'],
                                0, '#0000ff',   // 藍色 (極低溫)
                                15, '#00ffff',  // 青色 (低溫)
                                25, '#00ff00',  // 綠色 (適中)
                                30, '#ffff00',  // 黃色 (偏高)
                                35, '#ff8000',  // 橙色 (高溫)
                                40, '#ff0000'   // 紅色 (極高溫)
                            ],
                            'circle-stroke-width': 2,
                            'circle-stroke-color': '#ffffff',
                            'circle-opacity': 0.8
                        }
                    });
                }

                // 溫度標籤圖層
                if (!map.getLayer('weather-labels')) {
                    map.addLayer({
                        'id': 'weather-labels',
                        'type': 'symbol',
                        'source': 'weather-stations',
                        'layout': {
                            'text-field': '{temperature}°C',
                            'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
                            'text-size': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                6, 10,
                                12, 14
                            ],
                            'text-offset': [0, -2.5],
                            'text-anchor': 'center'
                        },
                        'paint': {
                            'text-color': '#2c3e50',
                            'text-halo-color': '#ffffff',
                            'text-halo-width': 2
                        }
                    });
                }

                // 城市名稱標籤圖層
                if (!map.getLayer('city-labels')) {
                    map.addLayer({
                        'id': 'city-labels',
                        'type': 'symbol',
                        'source': 'weather-stations',
                        'layout': {
                            'text-field': '{name}',
                            'text-font': ['Open Sans Regular', 'Arial Unicode MS Regular'],
                            'text-size': 12,
                            'text-offset': [0, 2],
                            'text-anchor': 'center'
                        },
                        'paint': {
                            'text-color': '#34495e',
                            'text-halo-color': '#ffffff',
                            'text-halo-width': 1
                        }
                    });
                }

                // 添加點擊事件
                map.on('click', 'weather-points', handleStationClick);
                
                // 添加滑鼠懸停效果
                map.on('mouseenter', 'weather-points', () => {
                    map.getCanvas().style.cursor = 'pointer';
                });

                map.on('mouseleave', 'weather-points', () => {
                    map.getCanvas().style.cursor = '';
                });

            } catch (error) {
                console.error('設定地圖圖層失敗:', error);
            }
        }

        // 處理氣象站點擊事件
        function handleStationClick(e) {
            const properties = e.features[0].properties;
            
            const popupContent = `
                <div style="font-family: Arial; min-width: 200px;">
                    <h3 style="margin: 0 0 10px 0; color: #2c3e50;">🏙️ ${properties.name}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 14px;">
                        <div><strong>🌡️ 溫度:</strong> ${properties.temperature}°C</div>
                        <div><strong>💧 濕度:</strong> ${properties.humidity}%</div>
                        <div><strong>📊 氣壓:</strong> ${properties.pressure} hPa</div>
                        <div><strong>💨 風速:</strong> ${properties.wind_speed} m/s</div>
                        <div colspan="2"><strong>☁️ 天氣:</strong> ${properties.weather_description}</div>
                    </div>
                    <hr style="margin: 10px 0;">
                    <small style="color: #7f8c8d;">
                        📅 更新時間: ${new Date(properties.timestamp).toLocaleString('zh-TW')}
                    </small>
                </div>
            `;

            new mapboxgl.Popup({ closeOnClick: true })
                .setLngLat(e.lngLat)
                .setHTML(popupContent)
                .addTo(map);
        }

        // 更新側邊欄天氣資料
        function updateWeatherSidebar(geojsonData) {
            const weatherDataDiv = document.getElementById('weather-data');
            
            if (!geojsonData.features || geojsonData.features.length === 0) {
                weatherDataDiv.innerHTML = '<p>暫無天氣資料</p>';
                return;
            }

            const weatherCards = geojsonData.features.map(feature => {
                const props = feature.properties;
                return `
                    <div class="weather-card">
                        <div class="weather-station">${props.name}</div>
                        <div class="weather-data">
                            <div><strong>溫度:</strong> ${props.temperature}°C</div>
                            <div><strong>濕度:</strong> ${props.humidity}%</div>
                            <div><strong>氣壓:</strong> ${props.pressure} hPa</div>
                            <div><strong>風速:</strong> ${props.wind_speed} m/s</div>
                        </div>
                    </div>
                `;
            }).join('');

            weatherDataDiv.innerHTML = weatherCards;
        }

        // 載入地圖配置
        async function loadMapConfig() {
            try {
                const response = await fetch('/api/config');
                const config = await response.json();
                
                // 設定圖層控制
                setupLayerControls(config.layer_controls);
            } catch (error) {
                console.error('載入地圖配置失敗:', error);
            }
        }

        // 設定圖層控制介面
        function setupLayerControls(layerControls) {
            // 天氣圖層控制
            const weatherLayersDiv = document.getElementById('weather-layers');
            if (layerControls.weather) {
                weatherLayersDiv.innerHTML = Object.entries(layerControls.weather).map(([key, layer]) => `
                    <div class="layer-item">
                        <input type="checkbox" class="layer-checkbox" id="weather-${key}" ${layer.default ? 'checked' : ''}>
                        <label class="layer-name" for="weather-${key}">${layer.name}</label>
                        <input type="range" class="opacity-slider" min="0" max="100" value="${layer.opacity * 100}">
                    </div>
                `).join('');
            }

            // 海洋圖層控制
            const oceanLayersDiv = document.getElementById('ocean-layers');
            if (layerControls.ocean) {
                oceanLayersDiv.innerHTML = Object.entries(layerControls.ocean).map(([key, layer]) => `
                    <div class="layer-item">
                        <input type="checkbox" class="layer-checkbox" id="ocean-${key}" ${layer.default ? 'checked' : ''}>
                        <label class="layer-name" for="ocean-${key}">${layer.name}</label>
                        <input type="range" class="opacity-slider" min="0" max="100" value="${layer.opacity * 100}">
                    </div>
                `).join('');
            }

            // 衛星圖層控制
            const satelliteLayersDiv = document.getElementById('satellite-layers');
            if (layerControls.satellite) {
                satelliteLayersDiv.innerHTML = Object.entries(layerControls.satellite).map(([key, layer]) => `
                    <div class="layer-item">
                        <input type="checkbox" class="layer-checkbox" id="satellite-${key}" ${layer.default ? 'checked' : ''}>
                        <label class="layer-name" for="satellite-${key}">${layer.name}</label>
                        <input type="range" class="opacity-slider" min="0" max="100" value="${layer.opacity * 100}">
                    </div>
                `).join('');
            }
        }

        // 更新 API Key
        function updateApiKey() {
            const apiKeyInput = document.getElementById('api-key-input');
            currentApiKey = apiKeyInput.value.trim() || null;
            
            updateStatus('更新 API Key，重新載入資料...');
            loadWeatherStations();
        }

        // 更新所有資料
        function refreshAllData() {
            updateStatus('刷新所有資料中...');
            loadWeatherStations();
        }

        // 回到台灣視窗
        function centerOnTaiwan() {
            map.flyTo({
                center: [121.0, 23.8],
                zoom: 7,
                pitch: 0,
                bearing: 0
            });
            updateStatus('已回到台灣視窗');
        }

        // 切換全螢幕
        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
                updateStatus('進入全螢幕模式');
            } else {
                document.exitFullscreen();
                updateStatus('退出全螢幕模式');
            }
        }

        // 開始自動更新
        function startAutoUpdate() {
            // 每10分鐘自動更新一次
            updateInterval = setInterval(() => {
                updateStatus('自動更新資料中...');
                loadWeatherStations();
            }, 10 * 60 * 1000);
        }

        // 更新狀態列
        function updateStatus(message) {
            const now = new Date().toLocaleTimeString('zh-TW');
            document.getElementById('status').textContent = `${now} - ${message}`;
        }

        // 顯示錯誤訊息
        function showError(message) {
            const weatherDataDiv = document.getElementById('weather-data');
            weatherDataDiv.innerHTML = `
                <div class="error-message">
                    ❌ ${message}
                </div>
            `;
        }

        // 頁面載入完成後初始化地圖
        window.addEventListener('load', () => {
            initMap();
        });

        // 頁面卸載時清理
        window.addEventListener('beforeunload', () => {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
        });
    </script>
</body>

</html>
'''

def create_weather_map_html():
    """建立完整的天氣地圖 HTML 檔案"""
    return HTML_TEMPLATE
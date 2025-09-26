/* 
 * API Keys JavaScript 配置檔案
 * 可直接在 HTML 中引用
 * 作者: GitHub Copilot  
 * 日期: 2025-09-26
 */

// ===========================
//       API 配置常數
// ===========================

const API_KEYS = {
    // Mapbox 地圖服務
    MAPBOX_ACCESS_TOKEN: "pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w",
    
    // OpenWeatherMap 天氣 API  
    OPENWEATHER_API_KEY: "c3021b469b0ad866b2e96b3e5676347f",
    
    // NOAA 海洋/氣象資料
    NOAA_API_KEY: "qFQyVggGGRNuYyKAiNvJYJfoOyONaDpwG"
};

// ===========================
//       API 服務配置
// ===========================

const API_CONFIG = {
    // Mapbox 配置
    MAPBOX: {
        ACCESS_TOKEN: API_KEYS.MAPBOX_ACCESS_TOKEN,
        BASE_URL: "https://api.mapbox.com",
        STYLES: {
            streets: "mapbox://styles/mapbox/streets-v12",
            satellite: "mapbox://styles/mapbox/satellite-v9", 
            light: "mapbox://styles/mapbox/light-v11",
            dark: "mapbox://styles/mapbox/dark-v11",
            outdoors: "mapbox://styles/mapbox/outdoors-v12",
            navigation: "mapbox://styles/mapbox/navigation-day-v1"
        }
    },
    
    // OpenWeatherMap 配置
    OPENWEATHER: {
        API_KEY: API_KEYS.OPENWEATHER_API_KEY,
        BASE_URL: "https://api.openweathermap.org/data/2.5",
        ENDPOINTS: {
            current: "/weather",
            forecast: "/forecast", 
            onecall: "/onecall",
            air_pollution: "/air_pollution"
        },
        LAYERS: {
            precipitation: `https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${API_KEYS.OPENWEATHER_API_KEY}`,
            clouds: `https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${API_KEYS.OPENWEATHER_API_KEY}`,
            pressure: `https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=${API_KEYS.OPENWEATHER_API_KEY}`,
            wind: `https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=${API_KEYS.OPENWEATHER_API_KEY}`,
            temp: `https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${API_KEYS.OPENWEATHER_API_KEY}`
        }
    },
    
    // NOAA 配置  
    NOAA: {
        API_KEY: API_KEYS.NOAA_API_KEY,
        BASE_URL: "https://www.ncdc.noaa.gov/cdo-web/api/v2"
    }
};

// ===========================
//       初始化設定
// ===========================

// 設置 Mapbox Access Token (如果 mapboxgl 已載入)
if (typeof mapboxgl !== 'undefined') {
    mapboxgl.accessToken = API_CONFIG.MAPBOX.ACCESS_TOKEN;
    console.log('✅ Mapbox Access Token 已設置');
}

// ===========================
//       便捷函數  
// ===========================

/**
 * 取得天氣 API URL
 * @param {string} endpoint - API 端點 (current, forecast, onecall)
 * @param {Object} params - 查詢參數
 * @returns {string} 完整的 API URL
 */
function getWeatherApiUrl(endpoint, params = {}) {
    const baseUrl = API_CONFIG.OPENWEATHER.BASE_URL;
    const endpointPath = API_CONFIG.OPENWEATHER.ENDPOINTS[endpoint];
    
    if (!endpointPath) {
        console.error(`未知的天氣 API 端點: ${endpoint}`);
        return null;
    }
    
    // 自動添加 API key
    params.appid = API_CONFIG.OPENWEATHER.API_KEY;
    
    // 建構查詢字串
    const queryString = new URLSearchParams(params).toString();
    
    return `${baseUrl}${endpointPath}?${queryString}`;
}

/**
 * 取得天氣圖層 URL  
 * @param {string} layerType - 圖層類型 (precipitation, clouds, etc.)
 * @returns {string} 圖層 URL 模板
 */
function getWeatherLayerUrl(layerType) {
    const layers = API_CONFIG.OPENWEATHER.LAYERS;
    
    if (layerType in layers) {
        return layers[layerType];
    }
    
    console.error(`未知的天氣圖層類型: ${layerType}`);
    return null;
}

/**
 * 驗證 API Keys 格式
 * @returns {Object} 驗證結果
 */
function validateApiKeys() {
    const results = {
        mapbox: API_KEYS.MAPBOX_ACCESS_TOKEN.length > 50 && API_KEYS.MAPBOX_ACCESS_TOKEN.startsWith("pk."),
        openweather: API_KEYS.OPENWEATHER_API_KEY.length === 32,
        noaa: API_KEYS.NOAA_API_KEY.length > 10
    };
    
    console.log("API Keys 驗證結果:", results);
    return results;
}

// ===========================
//       使用說明
// ===========================

console.log(`
🔑 API Keys 配置已載入

使用方法:
1. 直接引用: API_KEYS.MAPBOX_ACCESS_TOKEN
2. 使用配置: API_CONFIG.MAPBOX.STYLES.light  
3. 取得 URL: getWeatherApiUrl('current', {lat: 25.0330, lon: 121.5654})
4. 天氣圖層: getWeatherLayerUrl('precipitation')
5. 驗證密鑰: validateApiKeys()

地圖樣式:
- streets: 街道地圖
- satellite: 衛星地圖  
- light: 淺色地圖
- dark: 深色地圖
- outdoors: 戶外地圖
- navigation: 導航地圖
`);

// 自動驗證 API Keys
validateApiKeys();
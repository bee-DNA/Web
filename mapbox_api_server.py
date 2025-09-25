"""
Mapbox GL JS 地圖資料後端 API
提供地理資料的 RESTful API 服務
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 建立範例地理資料
def create_geographic_data():
    """建立豐富的地理散點資料"""
    
    locations_data = {
        "city": [
            "台北", "東京", "首爾", "北京", "上海", "香港", "新加坡", "曼谷", 
            "吉隆坡", "雅加達", "馬尼拉", "胡志明市", "河內", "金邊",
            "倫敦", "巴黎", "柏林", "羅馬", "馬德里", "阿姆斯特丹",
            "紐約", "洛杉磯", "芝加哥", "多倫多", "溫哥華", "墨西哥城",
            "聖保羅", "布宜諾斯艾利斯", "利馬", "波哥大", "卡拉卡斯",
            "雪梨", "墨爾本", "奧克蘭", "開普敦", "約翰尼斯堡", "開羅", 
            "拉哥斯", "奈洛比", "卡薩布蘭卡", "莫斯科", "基輔", "華沙",
            "布拉格", "維也納", "哥本哈根", "斯德哥爾摩", "雷克雅維克"
        ],
        "latitude": [
            25.0330, 35.6895, 37.5665, 39.9042, 31.2304, 22.3193, 1.3521, 13.7563,
            3.1390, -6.1751, 14.5995, 10.8231, 21.0285, 11.5449,
            51.5074, 48.8566, 52.5200, 41.9028, 40.4168, 52.3676,
            40.7128, 34.0522, 41.8781, 43.6532, 49.2827, 19.4326,
            -23.5505, -34.6037, -12.0464, 4.7110, 10.4806,
            -33.8688, -37.8136, -36.8485, -33.9249, -26.2041, 30.0444,
            6.5244, -1.2921, 33.5731, 55.7558, 50.4501, 52.2297,
            50.0755, 48.2082, 55.6761, 59.3293, 64.1466
        ],
        "longitude": [
            121.5654, 139.6917, 126.9780, 116.4074, 121.4737, 114.1694, 103.8198, 100.5018,
            101.6869, 106.8650, 120.9842, 106.6297, 105.8542, 104.9160,
            -0.1276, 2.3522, 13.4050, 12.4964, -3.7038, 4.9041,
            -74.0060, -118.2437, -87.6298, -79.3832, -123.1207, -99.1332,
            -46.6333, -58.3816, -77.0428, -74.0721, -66.9036,
            151.2093, 144.9631, 174.7633, 18.4241, 28.0473, 31.2357,
            3.3792, 36.8219, -7.5898, 37.6173, 30.5234, 21.0122,
            14.4378, 16.3738, 12.5683, 18.0686, -21.9426
        ],
        "country": [
            "台灣", "日本", "韓國", "中國", "中國", "香港", "新加坡", "泰國",
            "馬來西亞", "印尼", "菲律賓", "越南", "越南", "柬埔寨",
            "英國", "法國", "德國", "義大利", "西班牙", "荷蘭",
            "美國", "美國", "美國", "加拿大", "加拿大", "墨西哥",
            "巴西", "阿根廷", "秘魯", "哥倫比亞", "委內瑞拉",
            "澳洲", "澳洲", "紐西蘭", "南非", "南非", "埃及",
            "奈及利亞", "肯亞", "摩洛哥", "俄羅斯", "烏克蘭", "波蘭",
            "捷克", "奧地利", "丹麥", "瑞典", "冰島"
        ]
    }
    
    # 加入隨機數值和分類
    np.random.seed(42)
    n_cities = len(locations_data["city"])
    
    locations_data["value"] = np.random.randint(50, 100, n_cities).tolist()
    locations_data["category"] = np.random.choice(["A", "B", "C"], n_cities).tolist()
    locations_data["population"] = (np.random.exponential(2, n_cities) * 1000000).astype(int).tolist()
    locations_data["temperature"] = (np.random.normal(20, 15, n_cities)).round(1).tolist()
    
    return pd.DataFrame(locations_data)

# 全域資料變數
geographic_data = create_geographic_data()

@app.route('/')
def index():
    """主頁面"""
    return '''
    <h1>🗺️ Mapbox GL JS 地圖資料 API</h1>
    <p>提供地理資料的 RESTful API 服務</p>
    
    <h2>📍 可用的 API 端點：</h2>
    <ul>
        <li><a href="/api/cities">/api/cities</a> - 取得所有城市資料</li>
        <li><a href="/api/cities/geojson">/api/cities/geojson</a> - GeoJSON 格式的城市資料</li>
        <li><a href="/api/heatmap">/api/heatmap</a> - 熱力圖資料</li>
        <li><a href="/api/statistics">/api/statistics</a> - 統計摘要</li>
        <li><a href="/map">/map</a> - 互動式地圖頁面</li>
    </ul>
    
    <h2>🌍 範例查詢：</h2>
    <ul>
        <li><code>/api/cities?country=台灣</code> - 篩選特定國家</li>
        <li><code>/api/cities?min_value=80</code> - 數值大於 80 的城市</li>
        <li><code>/api/cities?category=A</code> - 特定分類的城市</li>
    </ul>
    '''

@app.route('/map')
def map_page():
    """返回地圖 HTML 頁面"""
    try:
        with open('mapbox_interactive_map.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "地圖檔案未找到，請確保 mapbox_interactive_map.html 存在於同一目錄中。"

@app.route('/api/cities')
def get_cities():
    """取得城市資料 API"""
    try:
        # 取得查詢參數
        country = request.args.get('country')
        min_value = request.args.get('min_value', type=int)
        max_value = request.args.get('max_value', type=int)
        category = request.args.get('category')
        
        # 篩選資料
        filtered_data = geographic_data.copy()
        
        if country:
            filtered_data = filtered_data[filtered_data['country'].str.contains(country, na=False)]
        
        if min_value is not None:
            filtered_data = filtered_data[filtered_data['value'] >= min_value]
            
        if max_value is not None:
            filtered_data = filtered_data[filtered_data['value'] <= max_value]
            
        if category:
            filtered_data = filtered_data[filtered_data['category'] == category]
        
        # 轉換為字典格式
        result = filtered_data.to_dict('records')
        
        return jsonify({
            'status': 'success',
            'count': len(result),
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/cities/geojson')
def get_cities_geojson():
    """取得 GeoJSON 格式的城市資料"""
    try:
        # 取得查詢參數
        country = request.args.get('country')
        min_value = request.args.get('min_value', type=int)
        category = request.args.get('category')
        
        # 篩選資料
        filtered_data = geographic_data.copy()
        
        if country:
            filtered_data = filtered_data[filtered_data['country'].str.contains(country, na=False)]
        
        if min_value is not None:
            filtered_data = filtered_data[filtered_data['value'] >= min_value]
            
        if category:
            filtered_data = filtered_data[filtered_data['category'] == category]
        
        # 建立 GeoJSON 格式
        features = []
        for _, row in filtered_data.iterrows():
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['longitude'], row['latitude']]
                },
                "properties": {
                    "name": row['city'],
                    "country": row['country'],
                    "value": row['value'],
                    "category": row['category'],
                    "population": row['population'],
                    "temperature": row['temperature']
                }
            }
            features.append(feature)
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return jsonify(geojson)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/heatmap')
def get_heatmap_data():
    """取得熱力圖資料"""
    try:
        heatmap_data = []
        
        for _, row in geographic_data.iterrows():
            heatmap_data.append([
                row['longitude'],
                row['latitude'],
                row['value'] / 100.0  # 標準化為 0-1 之間
            ])
        
        return jsonify({
            'status': 'success',
            'count': len(heatmap_data),
            'data': heatmap_data,
            'description': '熱力圖資料格式: [經度, 緯度, 強度]'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/statistics')
def get_statistics():
    """取得統計摘要"""
    try:
        stats = {
            'total_cities': len(geographic_data),
            'countries_count': geographic_data['country'].nunique(),
            'value_stats': {
                'min': float(geographic_data['value'].min()),
                'max': float(geographic_data['value'].max()),
                'mean': float(geographic_data['value'].mean().round(2)),
                'std': float(geographic_data['value'].std().round(2))
            },
            'population_stats': {
                'min': int(geographic_data['population'].min()),
                'max': int(geographic_data['population'].max()),
                'mean': int(geographic_data['population'].mean())
            },
            'temperature_stats': {
                'min': float(geographic_data['temperature'].min()),
                'max': float(geographic_data['temperature'].max()),
                'mean': float(geographic_data['temperature'].mean().round(1))
            },
            'category_distribution': geographic_data['category'].value_counts().to_dict(),
            'country_distribution': geographic_data['country'].value_counts().head(10).to_dict(),
            'bounds': {
                'north': float(geographic_data['latitude'].max()),
                'south': float(geographic_data['latitude'].min()),
                'east': float(geographic_data['longitude'].max()),
                'west': float(geographic_data['longitude'].min())
            }
        }
        
        return jsonify({
            'status': 'success',
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/cities/<city_name>')
def get_city_detail(city_name):
    """取得特定城市的詳細資料"""
    try:
        city_data = geographic_data[geographic_data['city'].str.contains(city_name, na=False)]
        
        if city_data.empty:
            return jsonify({
                'status': 'error',
                'message': f'找不到城市: {city_name}'
            }), 404
        
        result = city_data.iloc[0].to_dict()
        
        return jsonify({
            'status': 'success',
            'city': result
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_data():
    """上傳新的地理資料"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': '沒有檔案被上傳'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': '沒有選擇檔案'
            }), 400
        
        if file and file.filename.endswith('.csv'):
            # 讀取 CSV 檔案
            new_data = pd.read_csv(file)
            
            # 驗證必要欄位
            required_columns = ['city', 'latitude', 'longitude']
            missing_columns = [col for col in required_columns if col not in new_data.columns]
            
            if missing_columns:
                return jsonify({
                    'status': 'error',
                    'message': f'缺少必要欄位: {missing_columns}'
                }), 400
            
            # 更新全域資料 (這裡只是範例，實際應用中應該儲存到資料庫)
            global geographic_data
            geographic_data = pd.concat([geographic_data, new_data], ignore_index=True)
            
            return jsonify({
                'status': 'success',
                'message': f'成功上傳 {len(new_data)} 筆資料',
                'total_records': len(geographic_data)
            })
        
        else:
            return jsonify({
                'status': 'error',
                'message': '只支援 CSV 檔案格式'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("🗺️ 啟動 Mapbox GL JS 地圖資料 API 服務...")
    print("📍 主頁面: http://localhost:5000")
    print("🌍 地圖頁面: http://localhost:5000/map")
    print("📊 API 文件: http://localhost:5000")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
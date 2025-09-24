import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 建立真正可用的衛星地圖應用
app = dash.Dash(__name__)

# 建立範例地理散點資料
def create_geographic_scatter_data():
    """建立地理散點資料"""
    
    locations_data = {
        'city': [
            'Reykjavik', 'Oslo', 'Stockholm', 'Helsinki', 'Copenhagen',
            'London', 'Paris', 'Berlin', 'Madrid', 'Rome',
            'Moscow', 'Kiev', 'Warsaw', 'Prague', 'Vienna',
            'New York', 'Los Angeles', 'Chicago', 'Toronto', 'Vancouver',
            'Mexico City', 'Lima', 'Buenos Aires', 'Sao Paulo', 'Brasilia',
            'Cairo', 'Lagos', 'Johannesburg', 'Nairobi', 'Casablanca',
            'Tokyo', 'Beijing', 'Shanghai', 'Mumbai', 'Delhi',
            'Bangkok', 'Jakarta', 'Manila', 'Seoul', 'Sydney',
            'Singapore', 'Kuala Lumpur', 'Ho Chi Minh', 'Hanoi', 'Phnom Penh'
        ],
        'latitude': [
            64.1466, 59.9139, 59.3293, 60.1699, 55.6761,
            51.5074, 48.8566, 52.5200, 40.4168, 41.9028,
            55.7558, 50.4501, 52.2297, 50.0755, 48.2082,
            40.7128, 34.0522, 41.8781, 43.6532, 49.2827,
            19.4326, -12.0464, -34.6118, -23.5558, -15.8267,
            30.0444, 6.5244, -26.2041, -1.2921, 33.5731,
            35.6762, 39.9042, 31.2304, 19.0760, 28.7041,
            13.7563, -6.2088, 14.5995, 37.5665, -33.8688,
            1.3521, 3.1390, 10.8231, 21.0285, 11.5449
        ],
        'longitude': [
            -21.9426, 10.7522, 18.0686, 24.9384, 12.5683,
            -0.1278, 2.3522, 13.4050, -3.7038, 12.4964,
            37.6173, 30.5234, 21.0122, 14.4378, 16.3738,
            -74.0060, -118.2437, -87.6298, -79.3832, -123.1207,
            -99.1332, -77.0428, -58.3816, -46.6333, -47.8828,
            31.2357, 3.3792, 28.0473, 36.8219, -7.5898,
            139.6503, 116.4074, 121.4737, 72.8777, 77.1025,
            100.5018, 106.8456, 120.9842, 126.9780, 151.2093,
            103.8198, 101.6869, 106.6297, 105.8542, 104.9160
        ]
    }
    
    np.random.seed(42)
    values = np.random.randint(0, 101, len(locations_data['city']))
    
    special_values = {
        'New York': 94, 'London': 11, 'Tokyo': 15, 'Beijing': 1, 'Shanghai': 1,
        'Moscow': 2, 'Paris': 1, 'Berlin': 3, 'Sydney': 3, 'Toronto': 34,
        'Los Angeles': 24, 'Mumbai': 13, 'Delhi': 5, 'Bangkok': 3
    }
    
    for i, city in enumerate(locations_data['city']):
        if city in special_values:
            values[i] = special_values[city]
    
    locations_data['value'] = values
    
    return pd.DataFrame(locations_data)

# 建立資料
df = create_geographic_scatter_data()

# 定義顏色映射
def get_color_and_range(value):
    if 0 <= value <= 25:
        return '#3498db', '0-25'
    elif 26 <= value <= 50:
        return '#2ecc71', '26-50'
    elif 51 <= value <= 75:
        return '#f39c12', '51-75'
    elif 76 <= value <= 100:
        return '#e74c3c', '76-100'
    else:
        return '#95a5a6', 'Unknown'

df['color'] = df['value'].apply(lambda x: get_color_and_range(x)[0])
df['range'] = df['value'].apply(lambda x: get_color_and_range(x)[1])
df['size'] = df['value'].apply(lambda x: max(8, x * 0.3 + 15))

# 應用程式佈局
app.layout = html.Div([
    # 標題
    html.Div([
        html.H1("🛰️ 真實衛星地圖系統", 
               style={
                   'textAlign': 'center',
                   'marginBottom': '20px',
                   'color': '#2c3e50',
                   'fontFamily': 'Arial, sans-serif'
               }),
        html.P("🌍 使用可靠的地圖 API - 確保地圖正常顯示", 
               style={
                   'textAlign': 'center',
                   'fontSize': '16px',
                   'color': '#27ae60',
                   'marginBottom': '20px',
                   'fontWeight': 'bold'
               })
    ], style={
        'backgroundColor': '#ecf0f1',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px'
    }),
    
    # 控制面板
    html.Div([
        html.Div([
            html.Label("🗺️ 選擇地圖樣式:", style={'fontWeight': 'bold', 'marginBottom': '15px', 'color': '#2c3e50', 'fontSize': '16px'}),
            dcc.RadioItems(
                id='real-map-style',
                options=[
                    # 確保可用的地圖樣式
                    {'label': ' 🗺️ OpenStreetMap（標準地圖）', 'value': 'open-street-map'},
                    {'label': ' 🌫️ CartoDB Positron（簡約風格）', 'value': 'carto-positron'},  
                    {'label': ' 🌙 CartoDB Dark Matter（深色主題）', 'value': 'carto-darkmatter'},
                    {'label': ' 🚀 基礎衛星圖（Plotly 內建）', 'value': 'basic'},
                    
                    # 需要 Mapbox Token 的選項
                    {'label': ' 🛰️ Mapbox 衛星圖（需要 Token）', 'value': 'satellite'},
                    {'label': ' 🛰️ Mapbox 衛星街道（需要 Token）', 'value': 'satellite-streets'}
                ],
                value='open-street-map',
                style={'marginBottom': '20px', 'fontSize': '14px'},
                labelStyle={'display': 'block', 'marginBottom': '8px', 'cursor': 'pointer', 'padding': '6px'}
            ),
            html.Div(id='real-map-status', style={'color': '#27ae60', 'fontSize': '12px', 'fontStyle': 'italic'})
        ], style={'width': '58%', 'display': 'inline-block', 'marginRight': '4%'}),
        
        html.Div([
            html.Label("🎯 數值範圍篩選:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'color': '#2c3e50', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='real-range-filter',
                options=[
                    {'label': '🌍 顯示全部範圍', 'value': 'all'},
                    {'label': '🔵 0-25 (低數值)', 'value': '0-25'},
                    {'label': '🟢 26-50 (中低數值)', 'value': '26-50'},
                    {'label': '🟠 51-75 (中高數值)', 'value': '51-75'},
                    {'label': '🔴 76-100 (高數值)', 'value': '76-100'}
                ],
                value='all',
                style={'marginBottom': '20px'}
            ),
            
            # Mapbox Token 輸入框
            html.Label("🔑 Mapbox Access Token (可選):", style={'fontWeight': 'bold', 'marginBottom': '10px', 'color': '#2c3e50', 'fontSize': '14px'}),
            dcc.Input(
                id='real-mapbox-token',
                type='text',
                placeholder='輸入你的 Mapbox Token...',
                style={'width': '100%', 'padding': '8px', 'marginBottom': '10px', 'fontSize': '12px'},
                value=''
            ),
            html.P([
                "💡 免費獲取 Token: ",
                html.A("Mapbox 官網", href="https://www.mapbox.com/", target="_blank", style={'color': '#3498db'})
            ], style={'fontSize': '11px', 'color': '#95a5a6', 'margin': '0'})
        ], style={'width': '38%', 'display': 'inline-block'})
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '25px',
        'borderRadius': '10px',
        'margin': '20px',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
        'border': '1px solid #ddd'
    }),
    
    # 地圖狀態提示
    html.Div([
        html.Div(id='real-map-info', style={'marginBottom': '20px'}),
        html.Div(id='real-stats-info')
    ], style={'margin': '20px'}),
    
    # 地圖
    html.Div([
        dcc.Graph(id='real-satellite-map', style={'height': '700px'})
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
    })
])

# 地圖狀態回調
@app.callback(
    Output('real-map-status', 'children'),
    [Input('real-map-style', 'value'),
     Input('real-mapbox-token', 'value')]
)
def update_real_map_status(map_style, token):
    if map_style in ['satellite', 'satellite-streets']:
        if token and len(token) > 20:
            return '✅ Mapbox 衛星圖已配置'
        else:
            return '⚠️ 需要 Mapbox Token 才能使用衛星圖'
    
    status_map = {
        'open-street-map': '✅ OpenStreetMap 已載入 - 全世界最詳細的免費地圖',
        'carto-positron': '✅ CartoDB 簡約地圖已載入 - 清潔的白色風格',
        'carto-darkmatter': '✅ CartoDB 深色地圖已載入 - 現代化黑色主題',
        'basic': '✅ Plotly 基礎地圖已載入 - 內建地圖樣式',
        'satellite': '✅ Mapbox 衛星圖已載入',
        'satellite-streets': '✅ Mapbox 衛星街道圖已載入'
    }
    return status_map.get(map_style, '✅ 地圖已載入')

# 地圖資訊回調
@app.callback(
    Output('real-map-info', 'children'),
    [Input('real-map-style', 'value'),
     Input('real-range-filter', 'value'),
     Input('real-mapbox-token', 'value')]
)
def show_real_map_info(map_style, range_filter, token):
    map_descriptions = {
        'open-street-map': {
            'name': '🗺️ OpenStreetMap',
            'desc': '全世界協作製作的詳細地圖，包含道路、建築、地標等豐富資訊',
            'color': '#3498db',
            'quality': '高品質 (免費)'
        },
        'carto-positron': {
            'name': '🌫️ CartoDB Positron',
            'desc': '簡潔的白色風格地圖，適合數據視覺化和分析',
            'color': '#95a5a6',
            'quality': '優質 (免費)'
        },
        'carto-darkmatter': {
            'name': '🌙 CartoDB Dark Matter',
            'desc': '現代化深色主題地圖，適合夜間使用和專業展示',
            'color': '#34495e',
            'quality': '優質 (免費)'
        },
        'basic': {
            'name': '🚀 Plotly 基礎地圖',
            'desc': 'Plotly 內建的基礎地圖樣式，簡單可靠',
            'color': '#2ecc71',
            'quality': '標準 (免費)'
        },
        'satellite': {
            'name': '🛰️ Mapbox 衛星圖',
            'desc': '真正的高解析度衛星影像，展示地球真實面貌',
            'color': '#e74c3c',
            'quality': '最高品質 (需要 Token)'
        },
        'satellite-streets': {
            'name': '🛰️ Mapbox 衛星街道圖',
            'desc': '高解析度衛星影像結合詳細的街道標籤',
            'color': '#c0392b',
            'quality': '最高品質 (需要 Token)'
        }
    }
    
    map_info = map_descriptions.get(map_style, map_descriptions['open-street-map'])
    
    # 檢查 token 狀態
    needs_token = map_style in ['satellite', 'satellite-streets']
    has_token = token and len(token) > 20
    
    status_color = map_info['color']
    if needs_token and not has_token:
        status_color = '#e67e22'  # 警告色
    
    return html.Div([
        html.H4("🗺️ 當前地圖資訊", style={'marginBottom': '15px', 'color': '#2c3e50'}),
        html.Div([
            html.Div([
                html.H5(map_info['name'], style={'margin': '0', 'color': status_color}),
                html.P(map_info['desc'], style={'margin': '5px 0', 'color': '#7f8c8d', 'fontSize': '14px'}),
                html.Div([
                    html.Span(f"品質等級: {map_info['quality']}", style={'fontSize': '12px', 'color': '#34495e', 'marginRight': '15px'}),
                    html.Span(f"篩選範圍: {range_filter}", style={'fontSize': '12px', 'color': '#34495e'})
                ], style={'marginTop': '8px'}),
                
                # Token 狀態提示
                html.Div([
                    html.P([
                        '🔑 Token 狀態: ',
                        html.Span('✅ 已配置' if has_token else ('⚠️ 需要配置' if needs_token else '✅ 不需要'), 
                                style={'color': '#27ae60' if (has_token or not needs_token) else '#e74c3c', 'fontWeight': 'bold'})
                    ], style={'margin': '5px 0', 'fontSize': '12px'}) if needs_token else None
                ]) if needs_token else None
                
            ], style={
                'padding': '15px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'border': f'2px solid {status_color}'
            })
        ])
    ])

# 統計資訊回調
@app.callback(
    Output('real-stats-info', 'children'),
    [Input('real-range-filter', 'value')]
)
def update_real_stats(range_filter):
    if range_filter == 'all':
        filtered_df = df
        title = "全部地點"
    else:
        filtered_df = df[df['range'] == range_filter]
        title = f"範圍 {range_filter} 的地點"
    
    total_locations = len(filtered_df)
    avg_value = filtered_df['value'].mean() if len(filtered_df) > 0 else 0
    max_value = filtered_df['value'].max() if len(filtered_df) > 0 else 0
    min_value = filtered_df['value'].min() if len(filtered_df) > 0 else 0
    
    stats_cards = [
        html.Div([
            html.H4("📍", style={'margin': '0', 'fontSize': '24px'}),
            html.H3(f"{total_locations}", style={'margin': '5px 0', 'color': '#3498db'}),
            html.P("總地點數", style={'margin': '0', 'fontSize': '12px', 'color': '#7f8c8d'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 6px rgba(52, 152, 219, 0.2)',
            'border': '2px solid #3498db',
            'minWidth': '120px'
        }),
        
        html.Div([
            html.H4("📊", style={'margin': '0', 'fontSize': '24px'}),
            html.H3(f"{avg_value:.1f}", style={'margin': '5px 0', 'color': '#2ecc71'}),
            html.P("平均數值", style={'margin': '0', 'fontSize': '12px', 'color': '#7f8c8d'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 6px rgba(46, 204, 113, 0.2)',
            'border': '2px solid #2ecc71',
            'minWidth': '120px'
        }),
        
        html.Div([
            html.H4("🔺", style={'margin': '0', 'fontSize': '24px'}),
            html.H3(f"{max_value}", style={'margin': '5px 0', 'color': '#e74c3c'}),
            html.P("最高數值", style={'margin': '0', 'fontSize': '12px', 'color': '#7f8c8d'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 6px rgba(231, 76, 60, 0.2)',
            'border': '2px solid #e74c3c',
            'minWidth': '120px'
        }),
        
        html.Div([
            html.H4("🔻", style={'margin': '0', 'fontSize': '24px'}),
            html.H3(f"{min_value}", style={'margin': '5px 0', 'color': '#f39c12'}),
            html.P("最低數值", style={'margin': '0', 'fontSize': '12px', 'color': '#7f8c8d'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 6px rgba(243, 156, 18, 0.2)',
            'border': '2px solid #f39c12',
            'minWidth': '120px'
        })
    ]
    
    return html.Div([
        html.H4(f"📈 {title} 統計資訊", style={'marginBottom': '20px', 'color': '#2c3e50'}),
        html.Div(stats_cards, style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'flexWrap': 'wrap',
            'gap': '15px'
        })
    ])

# 主要地圖回調
@app.callback(
    Output('real-satellite-map', 'figure'),
    [Input('real-map-style', 'value'),
     Input('real-range-filter', 'value'),
     Input('real-mapbox-token', 'value')]
)
def update_real_satellite_map(map_style, range_filter, token):
    # 篩選資料
    if range_filter == 'all':
        filtered_df = df
        title = f"🗺️ 全球地理分布圖"
    else:
        filtered_df = df[df['range'] == range_filter]
        title = f"🎯 範圍 {range_filter} 分布圖"
    
    # 根據地圖樣式調整標題
    map_names = {
        'open-street-map': 'OpenStreetMap',
        'carto-positron': 'CartoDB 簡約',
        'carto-darkmatter': 'CartoDB 深色',
        'basic': 'Plotly 基礎',
        'satellite': 'Mapbox 衛星',
        'satellite-streets': 'Mapbox 衛星街道'
    }
    
    title += f" ({map_names.get(map_style, '地圖')})"
    
    # 建立散點地圖
    fig = go.Figure()
    
    ranges = ['0-25', '26-50', '51-75', '76-100']
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    
    # 首先添加數據點（主要的散點）
    for i, range_val in enumerate(ranges):
        range_data = filtered_df[filtered_df['range'] == range_val]
        
        if len(range_data) > 0:
            fig.add_trace(go.Scattermapbox(
                lat=range_data['latitude'],
                lon=range_data['longitude'],
                mode='markers+text',
                marker=dict(
                    size=range_data['size'],
                    color=colors[i],
                    opacity=0.9,
                    sizemode='diameter'
                ),
                text=range_data['value'],
                textposition="middle center",
                textfont=dict(
                    size=11,
                    color='white',
                    family='Arial Black'
                ),
                name=f'🔘 {range_val}',
                hovertemplate=
                '<b>🏙️ %{customdata[0]}</b><br>' +
                '📊 數值: %{customdata[1]}<br>' +
                '🎯 範圍: %{customdata[2]}<br>' +
                '🌐 緯度: %{lat:.3f}<br>' +
                '🌐 經度: %{lon:.3f}' +
                '<extra></extra>',
                customdata=range_data[['city', 'value', 'range']].values
            ))
    
    # 添加國家級別的標記點（在有數據的國家上方顯示小點）
    if len(filtered_df) > 0:
        # 定義每個國家的中心座標
        country_centers = {
            'Iceland': {'lat': 64.9631, 'lon': -19.0208, 'cities': ['Reykjavik']},
            'Norway': {'lat': 60.4720, 'lon': 8.4689, 'cities': ['Oslo']},
            'Sweden': {'lat': 60.1282, 'lon': 18.6435, 'cities': ['Stockholm']},
            'Finland': {'lat': 61.9241, 'lon': 25.7482, 'cities': ['Helsinki']},
            'Denmark': {'lat': 56.2639, 'lon': 9.5018, 'cities': ['Copenhagen']},
            'United Kingdom': {'lat': 55.3781, 'lon': -3.4360, 'cities': ['London']},
            'France': {'lat': 46.6034, 'lon': 1.8883, 'cities': ['Paris']},
            'Germany': {'lat': 51.1657, 'lon': 10.4515, 'cities': ['Berlin']},
            'Spain': {'lat': 40.4637, 'lon': -3.7492, 'cities': ['Madrid']},
            'Italy': {'lat': 41.8719, 'lon': 12.5674, 'cities': ['Rome']},
            'Russia': {'lat': 61.5240, 'lon': 105.3188, 'cities': ['Moscow']},
            'Ukraine': {'lat': 48.3794, 'lon': 31.1656, 'cities': ['Kiev']},
            'Poland': {'lat': 51.9194, 'lon': 19.1451, 'cities': ['Warsaw']},
            'Czech Republic': {'lat': 49.8175, 'lon': 15.4730, 'cities': ['Prague']},
            'Austria': {'lat': 47.5162, 'lon': 14.5501, 'cities': ['Vienna']},
            'United States': {'lat': 39.8283, 'lon': -98.5795, 'cities': ['New York', 'Los Angeles', 'Chicago']},
            'Canada': {'lat': 56.1304, 'lon': -106.3468, 'cities': ['Toronto', 'Vancouver']},
            'Mexico': {'lat': 23.6345, 'lon': -102.5528, 'cities': ['Mexico City']},
            'Peru': {'lat': -9.1900, 'lon': -75.0152, 'cities': ['Lima']},
            'Argentina': {'lat': -38.4161, 'lon': -63.6167, 'cities': ['Buenos Aires']},
            'Brazil': {'lat': -14.2350, 'lon': -51.9253, 'cities': ['Sao Paulo', 'Brasilia']},
            'Egypt': {'lat': 26.0975, 'lon': 30.0444, 'cities': ['Cairo']},
            'Nigeria': {'lat': 9.0820, 'lon': 8.6753, 'cities': ['Lagos']},
            'South Africa': {'lat': -30.5595, 'lon': 22.9375, 'cities': ['Johannesburg']},
            'Kenya': {'lat': -0.0236, 'lon': 37.9062, 'cities': ['Nairobi']},
            'Morocco': {'lat': 31.7917, 'lon': -7.0926, 'cities': ['Casablanca']},
            'Japan': {'lat': 36.2048, 'lon': 138.2529, 'cities': ['Tokyo']},
            'China': {'lat': 35.8617, 'lon': 104.1954, 'cities': ['Beijing', 'Shanghai']},
            'India': {'lat': 20.5937, 'lon': 78.9629, 'cities': ['Mumbai', 'Delhi']},
            'Thailand': {'lat': 15.8700, 'lon': 100.9925, 'cities': ['Bangkok']},
            'Indonesia': {'lat': -0.7893, 'lon': 113.9213, 'cities': ['Jakarta']},
            'Philippines': {'lat': 12.8797, 'lon': 121.7740, 'cities': ['Manila']},
            'South Korea': {'lat': 35.9078, 'lon': 127.7669, 'cities': ['Seoul']},
            'Australia': {'lat': -25.2744, 'lon': 133.7751, 'cities': ['Sydney']},
            'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'cities': ['Singapore']},
            'Malaysia': {'lat': 4.2105, 'lon': 101.9758, 'cities': ['Kuala Lumpur']},
            'Vietnam': {'lat': 14.0583, 'lon': 108.2772, 'cities': ['Ho Chi Minh', 'Hanoi']},
            'Cambodia': {'lat': 12.5657, 'lon': 104.9910, 'cities': ['Phnom Penh']}
        }
        
        # 找出有數據的國家
        cities_in_data = filtered_df['city'].tolist()
        countries_with_data = []
        
        for country, info in country_centers.items():
            # 檢查這個國家是否有城市在我們的數據中
            if any(city in cities_in_data for city in info['cities']):
                countries_with_data.append({
                    'country': country,
                    'lat': info['lat'],
                    'lon': info['lon'],
                    'city_count': len([city for city in info['cities'] if city in cities_in_data])
                })
        
        if countries_with_data:
            country_lats = [c['lat'] for c in countries_with_data]
            country_lons = [c['lon'] for c in countries_with_data]
            country_names = [c['country'] for c in countries_with_data]
            country_counts = [c['city_count'] for c in countries_with_data]
            
            # 添加國家標記點
            fig.add_trace(go.Scattermapbox(
                lat=country_lats,
                lon=country_lons,
                mode='markers',
                marker=dict(
                    size=12,
                    color='#e67e22',
                    opacity=0.8,
                    symbol='circle'
                ),
                name='📍 有數據的國家',
                hovertemplate=
                '<b>🏛️ %{customdata[0]}</b><br>' +
                '📊 城市數量: %{customdata[1]}<br>' +
                '📍 國家中心座標<br>' +
                '🌐 緯度: %{lat:.3f}<br>' +
                '🌐 經度: %{lon:.3f}' +
                '<extra></extra>',
                customdata=list(zip(country_names, country_counts)),
                showlegend=True
            ))
    
    # 配置 Mapbox 設定
    mapbox_config = {
        'style': map_style,
        'center': dict(lat=25, lon=10),
        'zoom': 1.3
    }
    
    # 如果是 Mapbox 樣式且有 token，則添加 access token
    if map_style in ['satellite', 'satellite-streets'] and token and len(token) > 20:
        mapbox_config['accesstoken'] = token
    elif map_style in ['satellite', 'satellite-streets'] and (not token or len(token) <= 20):
        # 如果沒有 token，改用基礎地圖
        mapbox_config['style'] = 'open-street-map'
        title += " (⚠️ 缺少 Token，顯示標準地圖)"
    
    # 更新佈局
    fig.update_layout(
        mapbox=mapbox_config,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial, sans-serif', 'color': '#2c3e50'}
        },
        font={'family': 'Arial, sans-serif'},
        showlegend=True,
        legend=dict(
            x=1.02,
            y=1,
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(0,0,0,0.3)',
            borderwidth=2,
            font=dict(size=12)
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        height=650
    )
    
    return fig

if __name__ == '__main__':
    import os
    app.run(
        debug=os.getenv('DASH_DEBUG', 'True').lower() == 'true',
        host=os.getenv('DASH_HOST', '0.0.0.0'),
        port=int(os.getenv('DASH_PORT', 8055))
    )
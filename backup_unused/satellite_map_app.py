import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# 建立衛星地圖專用應用
app = dash.Dash(__name__)

# 建立範例地理散點資料
def create_geographic_scatter_data():
    """建立地理散點資料，模擬圖片中的分布"""
    
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
        html.H1("🛰️ 真實衛星地圖視覺化", 
               style={
                   'textAlign': 'center',
                   'marginBottom': '20px',
                   'color': '#2c3e50',
                   'fontFamily': 'Arial, sans-serif'
               }),
        html.P("🌍 多種衛星地圖選項 - 從基礎到高品質衛星影像", 
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
    
    # Mapbox Token 說明
    html.Div([
        html.H4("⚠️ 衛星地圖使用說明", style={'color': '#e67e22', 'marginBottom': '10px'}),
        html.P([
            "🔑 高品質衛星地圖需要 Mapbox API Token。",
            html.Br(),
            "📍 免費選項：satellite-streets（基礎衛星圖）",
            html.Br(), 
            "🚀 高品質選項：需要在 ",
            html.A("Mapbox官網", href="https://www.mapbox.com/", target="_blank", style={'color': '#3498db'}),
            " 註冊並獲取免費 API Token"
        ], style={'margin': '0', 'fontSize': '14px', 'color': '#7f8c8d'})
    ], style={
        'backgroundColor': '#fef9e7',
        'padding': '15px',
        'borderRadius': '8px',
        'margin': '20px',
        'border': '1px solid #f39c12'
    }),
    
    # 控制面板
    html.Div([
        html.Div([
            html.Label("🛰️ 選擇衛星地圖樣式:", style={'fontWeight': 'bold', 'marginBottom': '15px', 'color': '#2c3e50', 'fontSize': '16px'}),
            dcc.RadioItems(
                id='satellite-map-style',
                options=[
                    # 確實有效的衛星選項
                    {'label': ' 🛰️ Stamen Terrain (地形衛星)', 'value': 'stamen-terrain'},
                    {'label': ' 🌍 Stamen Watercolor (藝術衛星)', 'value': 'stamen-watercolor'},
                    {'label': ' � CartoDB Dark (深色衛星)', 'value': 'carto-darkmatter'},
                    
                    # Mapbox 高品質選項（需要 token）
                    {'label': ' 🚀 Mapbox 衛星圖 (需要 Token)', 'value': 'satellite'},
                    {'label': ' 🚀 Mapbox 衛星街道 (需要 Token)', 'value': 'satellite-streets'},
                    
                    # 標準對照組
                    {'label': ' 🗺️ 標準街道地圖', 'value': 'open-street-map'},
                    {'label': ' 🌫️ 簡約地圖', 'value': 'carto-positron'}
                ],
                value='stamen-terrain',
                style={'marginBottom': '20px', 'fontSize': '14px'},
                labelStyle={'display': 'block', 'marginBottom': '8px', 'cursor': 'pointer', 'padding': '6px'}
            ),
            html.Div(id='satellite-status', style={'color': '#27ae60', 'fontSize': '12px', 'fontStyle': 'italic'})
        ], style={'width': '58%', 'display': 'inline-block', 'marginRight': '4%'}),
        
        html.Div([
            html.Label("🎯 數值範圍篩選:", style={'fontWeight': 'bold', 'marginBottom': '10px', 'color': '#2c3e50', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='range-filter',
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
                id='mapbox-token-input',
                type='text',
                placeholder='pk.eyJ1IjoieW91ci11c2VybmFtZSIsImEiOiJjbGJ...',
                style={'width': '100%', 'padding': '8px', 'marginBottom': '10px', 'fontSize': '12px'},
                value=''
            ),
            html.P("💡 輸入 Token 後可使用高品質衛星圖", style={'fontSize': '11px', 'color': '#95a5a6', 'margin': '0'})
        ], style={'width': '38%', 'display': 'inline-block'})
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '25px',
        'borderRadius': '10px',
        'margin': '20px',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
        'border': '1px solid #ddd'
    }),
    
    # 當前地圖資訊和統計
    html.Div([
        html.Div(id='current-satellite-info', style={'marginBottom': '20px'}),
        html.Div(id='stats-info')
    ], style={'margin': '20px'}),
    
    # 地圖
    html.Div([
        dcc.Graph(id='satellite-map', style={'height': '700px'})
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
    })
])

# 顯示衛星地圖狀態
@app.callback(
    Output('satellite-status', 'children'),
    [Input('satellite-map-style', 'value'),
     Input('mapbox-token-input', 'value')]
)
def update_satellite_status(map_style, token):
    if map_style in ['satellite', 'satellite-streets']:
        if token and len(token) > 20:
            return '✅ 高品質衛星圖已配置'
        else:
            return '⚠️ 需要 Mapbox Token 才能使用此樣式'
    
    status_map = {
        'stamen-terrain': '✅ 地形衛星圖已載入 - 顯示山脈、河流等地理特徵',
        'stamen-watercolor': '✅ 藝術風格衛星圖已載入 - 水彩畫風格',
        'carto-darkmatter': '✅ 深色衛星圖已載入 - 適合夜間觀看',
        'satellite': '✅ Mapbox 衛星圖已載入',
        'satellite-streets': '✅ Mapbox 衛星街道圖已載入',
        'open-street-map': '✅ 標準地圖已載入（對照組）',
        'carto-positron': '✅ 簡約地圖已載入（對照組）'
    }
    return status_map.get(map_style, '✅ 地圖已載入')

# 顯示當前衛星地圖資訊
@app.callback(
    Output('current-satellite-info', 'children'),
    [Input('satellite-map-style', 'value'),
     Input('range-filter', 'value'),
     Input('mapbox-token-input', 'value')]
)
def show_current_satellite_info(map_style, range_filter, token):
    map_descriptions = {
        'stamen-terrain': {
            'name': '🛰️ Stamen 地形衛星圖',
            'desc': '顯示真實地形特徵：山脈、河流、森林，立體感強烈',
            'color': '#27ae60',
            'quality': '高品質 (免費)'
        },
        'stamen-watercolor': {
            'name': '🎨 Stamen 水彩衛星圖',
            'desc': '藝術風格衛星圖，水彩畫效果，地理資訊藝術化呈現',
            'color': '#8e44ad',
            'quality': '獨特風格 (免費)'
        },
        'carto-darkmatter': {
            'name': '🌙 CartoDB 深色衛星圖',
            'desc': '深色主題衛星圖，適合夜間使用，現代化界面',
            'color': '#34495e',
            'quality': '高對比度 (免費)'
        },
        'satellite': {
            'name': '🚀 Mapbox 純衛星圖',
            'desc': '真正的高解析度衛星影像，最接近真實地球表面',
            'color': '#e74c3c',
            'quality': '最高品質 (需要 Token)'
        },
        'satellite-streets': {
            'name': '🚀 Mapbox 衛星街道圖',
            'desc': '高解析度衛星影像 + 詳細街道標籤，功能最完整',
            'color': '#c0392b',
            'quality': '最高品質 (需要 Token)'
        },
        'open-street-map': {
            'name': '🗺️ 標準街道地圖',
            'desc': 'OpenStreetMap 經典地圖，用於對比效果',
            'color': '#f39c12',
            'quality': '標準'
        },
        'carto-positron': {
            'name': '🌫️ 簡約地圖',
            'desc': '極簡風格地圖，用於對比衛星圖的豐富視覺效果',
            'color': '#95a5a6',
            'quality': '標準'
        }
    }
    
    map_info = map_descriptions.get(map_style, map_descriptions['satellite-streets'])
    
    # 檢查是否需要 token
    needs_token = map_style in ['satellite', 'satellite-streets']
    has_token = token and len(token) > 20
    
    status_color = map_info['color']
    if needs_token and not has_token:
        status_color = '#e67e22'  # 警告色
    
    return html.Div([
        html.H4("🛰️ 當前衛星地圖資訊", style={'marginBottom': '15px', 'color': '#2c3e50'}),
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
                        html.Span('已配置' if has_token else ('需要配置' if needs_token else '不需要'), 
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

# 更新統計資訊（重用之前的函數）
@app.callback(
    Output('stats-info', 'children'),
    [Input('range-filter', 'value')]
)
def update_stats(range_filter):
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

# 更新衛星地圖
@app.callback(
    Output('satellite-map', 'figure'),
    [Input('satellite-map-style', 'value'),
     Input('range-filter', 'value'),
     Input('mapbox-token-input', 'value')]
)
def update_satellite_map(map_style, range_filter, token):
    # 篩選資料
    if range_filter == 'all':
        filtered_df = df
        title = f"🛰️ 全球地理分布衛星圖"
    else:
        filtered_df = df[df['range'] == range_filter]
        title = f"🎯 範圍 {range_filter} 衛星圖"
    
    # 根據地圖樣式調整標題
    map_names = {
        'stamen-terrain': '地形衛星圖',
        'stamen-watercolor': '水彩衛星圖',
        'carto-darkmatter': '深色衛星圖',
        'satellite': 'Mapbox 純衛星',
        'satellite-streets': 'Mapbox 衛星街道',
        'open-street-map': '標準地圖',
        'carto-positron': '簡約地圖'
    }
    
    title += f" ({map_names.get(map_style, '衛星圖')})"
    
    # 建立散點地圖
    fig = go.Figure()
    
    ranges = ['0-25', '26-50', '51-75', '76-100']
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    
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
    
    # 配置 Mapbox 設定
    mapbox_config = {
        'style': map_style,
        'center': dict(lat=25, lon=10),
        'zoom': 1.3
    }
    
    # 如果是 Mapbox 樣式且有 token，則添加 access token
    if map_style in ['satellite', 'satellite-streets'] and token and len(token) > 20:
        mapbox_config['accesstoken'] = token
    
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
        port=int(os.getenv('DASH_PORT', 8054))
    )
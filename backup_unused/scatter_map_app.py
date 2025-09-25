import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# 建立散點地圖應用
app = dash.Dash(__name__)

# 建立範例地理散點資料 (模擬圖片中的資料)
def create_geographic_scatter_data():
    """建立地理散點資料，模擬圖片中的分布"""
    
    # 模擬圖片中的地點和數值
    locations_data = {
        'city': [
            'Reykjavik', 'Oslo', 'Stockholm', 'Helsinki', 'Copenhagen',  # 北歐
            'London', 'Paris', 'Berlin', 'Madrid', 'Rome',  # 西歐
            'Moscow', 'Kiev', 'Warsaw', 'Prague', 'Vienna',  # 東歐
            'New York', 'Los Angeles', 'Chicago', 'Toronto', 'Vancouver',  # 北美
            'Mexico City', 'Lima', 'Buenos Aires', 'Sao Paulo', 'Brasilia',  # 拉美
            'Cairo', 'Lagos', 'Johannesburg', 'Nairobi', 'Casablanca',  # 非洲
            'Tokyo', 'Beijing', 'Shanghai', 'Mumbai', 'Delhi',  # 亞洲
            'Bangkok', 'Jakarta', 'Manila', 'Seoul', 'Sydney',  # 亞太
            'Singapore', 'Kuala Lumpur', 'Ho Chi Minh', 'Hanoi', 'Phnom Penh'  # 東南亞
        ],
        'latitude': [
            64.1466, 59.9139, 59.3293, 60.1699, 55.6761,  # 北歐
            51.5074, 48.8566, 52.5200, 40.4168, 41.9028,  # 西歐
            55.7558, 50.4501, 52.2297, 50.0755, 48.2082,  # 東歐
            40.7128, 34.0522, 41.8781, 43.6532, 49.2827,  # 北美
            19.4326, -12.0464, -34.6118, -23.5558, -15.8267,  # 拉美
            30.0444, 6.5244, -26.2041, -1.2921, 33.5731,  # 非洲
            35.6762, 39.9042, 31.2304, 19.0760, 28.7041,  # 亞洲
            13.7563, -6.2088, 14.5995, 37.5665, -33.8688,  # 亞太
            1.3521, 3.1390, 10.8231, 21.0285, 11.5449  # 東南亞
        ],
        'longitude': [
            -21.9426, 10.7522, 18.0686, 24.9384, 12.5683,  # 北歐
            -0.1278, 2.3522, 13.4050, -3.7038, 12.4964,  # 西歐
            37.6173, 30.5234, 21.0122, 14.4378, 16.3738,  # 東歐
            -74.0060, -118.2437, -87.6298, -79.3832, -123.1207,  # 北美
            -99.1332, -77.0428, -58.3816, -46.6333, -47.8828,  # 拉美
            31.2357, 3.3792, 28.0473, 36.8219, -7.5898,  # 非洲
            139.6503, 116.4074, 121.4737, 72.8777, 77.1025,  # 亞洲
            100.5018, 106.8456, 120.9842, 126.9780, 151.2093,  # 亞太
            103.8198, 101.6869, 106.6297, 105.8542, 104.9160  # 東南亞
        ]
    }
    
    # 為每個地點隨機生成 0-100 的數值 (模擬圖片中的分布)
    np.random.seed(42)  # 保持結果一致
    values = np.random.randint(0, 101, len(locations_data['city']))
    
    # 根據圖片中的分布，調整一些特定值
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

# 定義顏色映射 (根據圖片中的顏色)
def get_color_and_range(value):
    """根據數值返回顏色和範圍標籤"""
    if 0 <= value <= 25:
        return '#3498db', '0-25'  # 藍色
    elif 26 <= value <= 50:
        return '#2ecc71', '26-50'  # 綠色
    elif 51 <= value <= 75:
        return '#f39c12', '51-75'  # 橙色
    elif 76 <= value <= 100:
        return '#e74c3c', '76-100'  # 紅色
    else:
        return '#95a5a6', 'Unknown'  # 灰色

# 為資料添加顏色和範圍
df['color'] = df['value'].apply(lambda x: get_color_and_range(x)[0])
df['range'] = df['value'].apply(lambda x: get_color_and_range(x)[1])

# 計算圓圈大小 (根據數值)
df['size'] = df['value'].apply(lambda x: max(8, x * 0.3 + 10))

# 應用程式佈局
app.layout = html.Div([
    # 標題
    html.Div([
        html.H1("🌍 地理分布散點地圖", 
               style={
                   'textAlign': 'center',
                   'marginBottom': '20px',
                   'color': '#2c3e50',
                   'fontFamily': 'Arial, sans-serif'
               }),
        html.P("Geographical distribution - 互動式地理散點圖", 
               style={
                   'textAlign': 'center',
                   'fontSize': '16px',
                   'color': '#7f8c8d',
                   'marginBottom': '20px'
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
            html.Label("地圖樣式:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='map-style-dropdown',
                options=[
                    {'label': '🗺️ 開放街圖', 'value': 'open-street-map'},
                    {'label': '🛰️ 衛星圖', 'value': 'satellite-streets'},
                    {'label': '🌎  地形圖', 'value': 'stamen-terrain'},
                    {'label': '🏙️ 基礎地圖', 'value': 'basic'},
                    {'label': '🌫️ 淺色地圖', 'value': 'carto-positron'},
                    {'label': '🌙 深色地圖', 'value': 'carto-darkmatter'},
                    {'label': '� 水彩地圖', 'value': 'stamen-watercolor'}
                ],
                value='open-street-map',
                style={'marginBottom': '20px'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
        
        html.Div([
            html.Label("數值範圍篩選:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='range-filter',
                options=[
                    {'label': '🌍 全部範圍', 'value': 'all'},
                    {'label': '🔵 0-25', 'value': '0-25'},
                    {'label': '🟢 26-50', 'value': '26-50'},
                    {'label': '🟠 51-75', 'value': '51-75'},
                    {'label': '🔴 76-100', 'value': '76-100'}
                ],
                value='all',
                style={'marginBottom': '20px'}
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),
    
    # 統計資訊
    html.Div(id='stats-info', style={'margin': '20px'}),
    
    # 地圖
    html.Div([
        dcc.Graph(id='scatter-map', style={'height': '700px'})
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })
])

# 更新統計資訊
@app.callback(
    Output('stats-info', 'children'),
    [Input('range-filter', 'value')]
)
def update_stats(range_filter):
    # 篩選資料
    if range_filter == 'all':
        filtered_df = df
        title = "全部地點"
    else:
        filtered_df = df[df['range'] == range_filter]
        title = f"範圍 {range_filter} 的地點"
    
    total_locations = len(filtered_df)
    avg_value = filtered_df['value'].mean()
    max_value = filtered_df['value'].max()
    min_value = filtered_df['value'].min()
    
    # 建立統計卡片
    stats_cards = [
        html.Div([
            html.H4("📍 總地點數", style={'margin': '0', 'color': '#2c3e50'}),
            html.H2(f"{total_locations}", style={'margin': '10px 0', 'color': '#3498db'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'border': '2px solid #3498db'
        }),
        
        html.Div([
            html.H4("📊 平均數值", style={'margin': '0', 'color': '#2c3e50'}),
            html.H2(f"{avg_value:.1f}", style={'margin': '10px 0', 'color': '#2ecc71'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'border': '2px solid #2ecc71'
        }),
        
        html.Div([
            html.H4("🔺 最高數值", style={'margin': '0', 'color': '#2c3e50'}),
            html.H2(f"{max_value}", style={'margin': '10px 0', 'color': '#e74c3c'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'border': '2px solid #e74c3c'
        }),
        
        html.Div([
            html.H4("🔻 最低數值", style={'margin': '0', 'color': '#2c3e50'}),
            html.H2(f"{min_value}", style={'margin': '10px 0', 'color': '#f39c12'})
        ], style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'border': '2px solid #f39c12'
        })
    ]
    
    return html.Div([
        html.H3(f"📈 {title} 統計資訊", style={'marginBottom': '20px', 'color': '#2c3e50'}),
        html.Div(stats_cards, style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'flexWrap': 'wrap',
            'gap': '15px'
        })
    ])

# 更新地圖
@app.callback(
    Output('scatter-map', 'figure'),
    [Input('map-style-dropdown', 'value'),
     Input('range-filter', 'value')]
)
def update_map(map_style, range_filter):
    # 篩選資料
    if range_filter == 'all':
        filtered_df = df
        title = "🌍 全球地理分布散點圖"
    else:
        filtered_df = df[df['range'] == range_filter]
        title = f"🎯 範圍 {range_filter} 地理分布"
    
    # 建立散點地圖
    fig = go.Figure()
    
    # 按範圍分組添加散點
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
                    opacity=0.8,
                    sizemode='diameter'
                ),
                text=range_data['value'],
                textposition="middle center",
                textfont=dict(
                    size=10,
                    color='white'
                ),
                name=f'{range_val}',
                hovertemplate=
                '<b>%{customdata[0]}</b><br>' +
                '數值: %{customdata[1]}<br>' +
                '範圍: %{customdata[2]}<br>' +
                '緯度: %{lat}<br>' +
                '經度: %{lon}' +
                '<extra></extra>',
                customdata=range_data[['city', 'value', 'range']].values
            ))
    
    # 更新佈局
    fig.update_layout(
        mapbox=dict(
            style=map_style,
            center=dict(lat=20, lon=0),
            zoom=1.2,
            accesstoken=None  # 確保不需要 token
        ),
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Arial, sans-serif'}
        },
        font={'family': 'Arial, sans-serif'},
        showlegend=True,
        legend=dict(
            x=1.02,
            y=1,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

if __name__ == '__main__':
    import os
    app.run(
        debug=os.getenv('DASH_DEBUG', 'True').lower() == 'true',
        host=os.getenv('DASH_HOST', '0.0.0.0'),
        port=int(os.getenv('DASH_PORT', 8051))  # 使用不同的端口避免衝突
    )
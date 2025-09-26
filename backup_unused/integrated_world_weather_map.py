import dash
from dash import dcc, html, Input, Output, dash_table, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import threading
import time

# 建立整合天氣功能的世界地圖應用
app = dash.Dash(__name__)

# API 配置
API_KEYS = {
    "openweather": "c3021b469b0ad866b2e96b3e5676347f",
    "mapbox": "pk.eyJ1IjoiYmVlLWRuYSIsImEiOiJjbWZ5MTlhOTkwZnF3MmxvbjkwN2RtM2Z4In0.yFiY2MNpWqaDINuLaz1e0w",
}

# 全球主要城市配置
GLOBAL_CITIES = [
    {
        "name": "台北",
        "lat": 25.0330,
        "lng": 121.5654,
        "country": "TW",
        "country_name": "台灣",
        "region": "asia",
    },
    {
        "name": "東京",
        "lat": 35.6762,
        "lng": 139.6503,
        "country": "JP",
        "country_name": "日本",
        "region": "asia",
    },
    {
        "name": "首爾",
        "lat": 37.5665,
        "lng": 126.9780,
        "country": "KR",
        "country_name": "南韓",
        "region": "asia",
    },
    {
        "name": "北京",
        "lat": 39.9042,
        "lng": 116.4074,
        "country": "CN",
        "country_name": "中國",
        "region": "asia",
    },
    {
        "name": "香港",
        "lat": 22.3193,
        "lng": 114.1694,
        "country": "HK",
        "country_name": "香港",
        "region": "asia",
    },
    {
        "name": "新加坡",
        "lat": 1.3521,
        "lng": 103.8198,
        "country": "SG",
        "country_name": "新加坡",
        "region": "asia",
    },
    {
        "name": "孟買",
        "lat": 19.0760,
        "lng": 72.8777,
        "country": "IN",
        "country_name": "印度",
        "region": "asia",
    },
    {
        "name": "倫敦",
        "lat": 51.5074,
        "lng": -0.1278,
        "country": "GB",
        "country_name": "英國",
        "region": "europe",
    },
    {
        "name": "巴黎",
        "lat": 48.8566,
        "lng": 2.3522,
        "country": "FR",
        "country_name": "法國",
        "region": "europe",
    },
    {
        "name": "柏林",
        "lat": 52.5200,
        "lng": 13.4050,
        "country": "DE",
        "country_name": "德國",
        "region": "europe",
    },
    {
        "name": "羅馬",
        "lat": 41.9028,
        "lng": 12.4964,
        "country": "IT",
        "country_name": "意大利",
        "region": "europe",
    },
    {
        "name": "莫斯科",
        "lat": 55.7558,
        "lng": 37.6176,
        "country": "RU",
        "country_name": "俄羅斯",
        "region": "europe",
    },
    {
        "name": "紐約",
        "lat": 40.7128,
        "lng": -74.0060,
        "country": "US",
        "country_name": "美國",
        "region": "americas",
    },
    {
        "name": "洛杉磯",
        "lat": 34.0522,
        "lng": -118.2437,
        "country": "US",
        "country_name": "美國",
        "region": "americas",
    },
    {
        "name": "聖保羅",
        "lat": -23.5505,
        "lng": -46.6333,
        "country": "BR",
        "country_name": "巴西",
        "region": "americas",
    },
    {
        "name": "雪梨",
        "lat": -33.8688,
        "lng": 151.2093,
        "country": "AU",
        "country_name": "澳洲",
        "region": "oceania",
    },
    {
        "name": "開普敦",
        "lat": -33.9249,
        "lng": 18.4241,
        "country": "ZA",
        "country_name": "南非",
        "region": "africa",
    },
    {
        "name": "開羅",
        "lat": 30.0444,
        "lng": 31.2357,
        "country": "EG",
        "country_name": "埃及",
        "region": "africa",
    },
]

# 全域變數
global_weather_data = {}
last_update_time = None


def fetch_weather_data(city):
    """獲取單個城市的天氣資料"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": city["lat"],
            "lon": city["lng"],
            "appid": API_KEYS["openweather"],
            "units": "metric",
            "lang": "zh_tw",
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": city["name"],
                "country": city["country_name"],
                "region": city["region"],
                "lat": city["lat"],
                "lng": city["lng"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"] if "wind" in data else 0,
                "wind_direction": (
                    data["wind"]["deg"]
                    if "wind" in data and "deg" in data["wind"]
                    else 0
                ),
                "weather": (
                    data["weather"][0]["description"] if data["weather"] else "未知"
                ),
                "clouds": data["clouds"]["all"] if "clouds" in data else 0,
                "visibility": data.get("visibility", 10000) / 1000,  # 轉換為公里
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
    except Exception as e:
        print(f"獲取 {city['name']} 天氣資料失敗: {e}")
        # 返回模擬資料
        return {
            "city": city["name"],
            "country": city["country_name"],
            "region": city["region"],
            "lat": city["lat"],
            "lng": city["lng"],
            "temperature": 20 + np.random.random() * 15,
            "feels_like": 20 + np.random.random() * 15,
            "humidity": 40 + np.random.random() * 40,
            "pressure": 1000 + np.random.random() * 50,
            "wind_speed": np.random.random() * 10,
            "wind_direction": np.random.random() * 360,
            "weather": "晴天",
            "clouds": np.random.random() * 100,
            "visibility": 5 + np.random.random() * 15,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def update_global_weather():
    """更新全球天氣資料"""
    global global_weather_data, last_update_time

    print("🌍 開始更新全球天氣資料...")
    weather_list = []

    for city in GLOBAL_CITIES:
        weather = fetch_weather_data(city)
        weather_list.append(weather)
        time.sleep(0.1)  # 避免 API 請求過於頻繁

    global_weather_data = pd.DataFrame(weather_list)
    last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ 全球天氣資料更新完成: {last_update_time}")


# 初始載入天氣資料
update_global_weather()


def create_sample_data():
    """建立世界各國基本資料"""
    countries_data = {
        "country": [
            "China",
            "India",
            "United States",
            "Indonesia",
            "Pakistan",
            "Brazil",
            "Nigeria",
            "Bangladesh",
            "Russia",
            "Mexico",
            "Japan",
            "Germany",
            "Iran",
            "Turkey",
            "Vietnam",
            "Philippines",
            "Ethiopia",
            "Egypt",
            "United Kingdom",
            "France",
        ],
        "population": [
            1439323776,
            1380004385,
            331002651,
            273523615,
            220892340,
            212559417,
            206139589,
            164689383,
            145934462,
            128932753,
            126476461,
            83783942,
            83992949,
            84339067,
            97338579,
            109581078,
            114963588,
            102334404,
            67886011,
            65273511,
        ],
        "gdp": [
            14342.9,
            2875.1,
            21427.7,
            1158.7,
            348.3,
            1839.8,
            432.3,
            416.3,
            1699.9,
            1258.3,
            4937.4,
            3846.4,
            231.3,
            761.4,
            362.6,
            361.5,
            96.1,
            404.1,
            2829.1,
            2715.5,
        ],
        "iso_alpha": [
            "CHN",
            "IND",
            "USA",
            "IDN",
            "PAK",
            "BRA",
            "NGA",
            "BGD",
            "RUS",
            "MEX",
            "JPN",
            "DEU",
            "IRN",
            "TUR",
            "VNM",
            "PHL",
            "ETH",
            "EGY",
            "GBR",
            "FRA",
        ],
    }
    return pd.DataFrame(countries_data)


# 建立基本資料
df_countries = create_sample_data()

# 應用程式佈局
app.layout = html.Div(
    [
        html.H1(
            "🌍 整合世界地圖 & 全球天氣系統",
            style={
                "text-align": "center",
                "margin-bottom": "30px",
                "color": "#2c3e50",
                "font-family": "Arial, sans-serif",
            },
        ),
        # 主控制面板
        html.Div(
            [
                html.Div(
                    [
                        html.H3("🗺️ 地圖模式", style={"margin-bottom": "15px"}),
                        dcc.RadioItems(
                            id="map-mode",
                            options=[
                                {"label": "📊 國家統計資料", "value": "country"},
                                {"label": "🌦️ 全球天氣監測", "value": "weather"},
                            ],
                            value="country",
                            inline=True,
                            style={"margin-bottom": "20px"},
                        ),
                    ],
                    style={"width": "50%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.H3("⏰ 資料更新", style={"margin-bottom": "15px"}),
                        html.P(
                            f"最後更新: {last_update_time}",
                            id="last-update",
                            style={"margin-bottom": "10px"},
                        ),
                        html.Button(
                            "🔄 手動更新天氣",
                            id="refresh-btn",
                            n_clicks=0,
                            style={
                                "background": "#3498db",
                                "color": "white",
                                "border": "none",
                                "padding": "8px 16px",
                                "border-radius": "5px",
                                "cursor": "pointer",
                            },
                        ),
                    ],
                    style={
                        "width": "50%",
                        "display": "inline-block",
                        "text-align": "right",
                    },
                ),
            ],
            style={
                "margin-bottom": "30px",
                "padding": "20px",
                "background": "#f8f9fa",
                "border-radius": "10px",
            },
        ),
        # 國家統計模式控制
        html.Div(
            [
                html.Div(
                    [
                        html.Label("資料類型："),
                        dcc.Dropdown(
                            id="data-dropdown",
                            options=[
                                {"label": "人口數量", "value": "population"},
                                {"label": "GDP (十億美元)", "value": "gdp"},
                            ],
                            value="population",
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.Label("色彩主題："),
                        dcc.Dropdown(
                            id="color-dropdown",
                            options=[
                                {"label": "藍色系", "value": "Blues"},
                                {"label": "紅色系", "value": "Reds"},
                                {"label": "綠色系", "value": "Greens"},
                                {"label": "彩虹色", "value": "Viridis"},
                            ],
                            value="Blues",
                        ),
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
            ],
            id="country-controls",
            style={"margin-bottom": "30px"},
        ),
        # 天氣模式控制
        html.Div(
            [
                html.Div(
                    [
                        html.Label("地區篩選："),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": "🌏 全部地區", "value": "all"},
                                {"label": "🏯 亞洲", "value": "asia"},
                                {"label": "🏰 歐洲", "value": "europe"},
                                {"label": "🗽 美洲", "value": "americas"},
                                {"label": "🦘 大洋洲", "value": "oceania"},
                                {"label": "🦁 非洲", "value": "africa"},
                            ],
                            value="all",
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.Label("天氣顯示："),
                        dcc.Dropdown(
                            id="weather-display",
                            options=[
                                {"label": "🌡️ 溫度", "value": "temperature"},
                                {"label": "💧 濕度", "value": "humidity"},
                                {"label": "💨 風速", "value": "wind_speed"},
                                {"label": "☁️ 雲量", "value": "clouds"},
                            ],
                            value="temperature",
                        ),
                    ],
                    style={"width": "48%", "float": "right", "display": "inline-block"},
                ),
            ],
            id="weather-controls",
            style={"margin-bottom": "30px", "display": "none"},
        ),
        # 主地圖
        dcc.Graph(id="main-map", style={"height": "600px"}),
        html.Hr(style={"margin": "40px 0"}),
        # 統計資訊
        html.Div(
            [
                html.Div(id="stats-cards", style={"margin-bottom": "30px"}),
            ]
        ),
        # 資料表
        html.H2("📊 詳細資料", style={"text-align": "center", "margin-bottom": "20px"}),
        html.Div(id="data-table-container"),
    ],
    style={"padding": "20px", "font-family": "Arial, sans-serif"},
)


# 回調：控制面板顯示
@app.callback(
    [Output("country-controls", "style"), Output("weather-controls", "style")],
    [Input("map-mode", "value")],
)
def toggle_controls(mode):
    if mode == "country":
        return {"margin-bottom": "30px"}, {"margin-bottom": "30px", "display": "none"}
    else:
        return {"margin-bottom": "30px", "display": "none"}, {"margin-bottom": "30px"}


# 回調：更新主地圖
@app.callback(
    Output("main-map", "figure"),
    [
        Input("map-mode", "value"),
        Input("data-dropdown", "value"),
        Input("color-dropdown", "value"),
        Input("region-filter", "value"),
        Input("weather-display", "value"),
        Input("refresh-btn", "n_clicks"),
    ],
)
def update_main_map(
    mode, selected_data, color_scale, region_filter, weather_display, n_clicks
):
    global global_weather_data

    if mode == "country":
        # 國家統計模式
        fig = px.choropleth(
            df_countries,
            locations="iso_alpha",
            color=selected_data,
            hover_name="country",
            hover_data={"population": ":,.0f", "gdp": ":,.1f"},
            color_continuous_scale=color_scale,
            title=f"世界各國 {'人口分布' if selected_data == 'population' else 'GDP分布'}",
        )

        fig.update_layout(
            title_x=0.5,
            geo=dict(
                showframe=False, showcoastlines=True, projection_type="natural earth"
            ),
            height=600,
        )

    else:
        # 天氣模式
        if n_clicks > 0:  # 如果點擊了刷新按鈕
            update_global_weather()

        # 篩選資料
        if region_filter == "all":
            filtered_data = global_weather_data
        else:
            filtered_data = global_weather_data[
                global_weather_data["region"] == region_filter
            ]

        # 創建散點地圖
        fig = go.Figure()

        # 添加背景地圖
        fig.add_trace(
            go.Scattergeo(
                lon=filtered_data["lng"],
                lat=filtered_data["lat"],
                text=[
                    f"{row['city']}<br>{row['country']}<br>"
                    f"🌡️ {row['temperature']:.1f}°C<br>"
                    f"💧 {row['humidity']}%<br>"
                    f"💨 {row['wind_speed']:.1f} m/s<br>"
                    f"☁️ {row['clouds']}%<br>"
                    f"🌤️ {row['weather']}"
                    for _, row in filtered_data.iterrows()
                ],
                mode="markers+text",
                marker=dict(
                    size=[
                        max(8, min(25, abs(temp) / 2))
                        for temp in filtered_data[weather_display]
                    ],
                    color=filtered_data[weather_display],
                    colorscale=(
                        "RdYlBu_r" if weather_display == "temperature" else "Viridis"
                    ),
                    showscale=True,
                    colorbar=dict(title=f"{weather_display}", x=0.02),
                    line=dict(width=2, color="white"),
                ),
                textposition="top center",
                textfont=dict(size=10, color="darkblue"),
                hovertemplate="<b>%{text}</b><extra></extra>",
            )
        )

        fig.update_layout(
            title=f"🌍 全球天氣監測 - {weather_display}",
            title_x=0.5,
            geo=dict(
                projection_type="natural earth",
                showland=True,
                landcolor="lightgray",
                showocean=True,
                oceancolor="lightblue",
                showlakes=True,
                lakecolor="lightblue",
                showcoastlines=True,
                coastlinecolor="darkgray",
                showframe=False,
            ),
            height=600,
        )

    return fig


# 回調：更新統計卡片
@app.callback(
    Output("stats-cards", "children"),
    [
        Input("map-mode", "value"),
        Input("region-filter", "value"),
        Input("refresh-btn", "n_clicks"),
    ],
)
def update_stats_cards(mode, region_filter, n_clicks):
    if mode == "country":
        # 國家統計
        total_countries = len(df_countries)
        total_population = df_countries["population"].sum()
        total_gdp = df_countries["gdp"].sum()
        avg_gdp = df_countries["gdp"].mean()

        return html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            f"{total_countries}",
                            style={"color": "#3498db", "margin": "0"},
                        ),
                        html.P("國家數量", style={"margin": "5px 0"}),
                    ],
                    style={
                        "text-align": "center",
                        "background": "white",
                        "padding": "20px",
                        "border-radius": "10px",
                        "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "width": "23%",
                        "display": "inline-block",
                        "margin": "1%",
                    },
                ),
                html.Div(
                    [
                        html.H3(
                            f"{total_population/1e9:.1f}B",
                            style={"color": "#e74c3c", "margin": "0"},
                        ),
                        html.P("總人口", style={"margin": "5px 0"}),
                    ],
                    style={
                        "text-align": "center",
                        "background": "white",
                        "padding": "20px",
                        "border-radius": "10px",
                        "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "width": "23%",
                        "display": "inline-block",
                        "margin": "1%",
                    },
                ),
                html.Div(
                    [
                        html.H3(
                            f"${total_gdp:.1f}T",
                            style={"color": "#27ae60", "margin": "0"},
                        ),
                        html.P("總GDP", style={"margin": "5px 0"}),
                    ],
                    style={
                        "text-align": "center",
                        "background": "white",
                        "padding": "20px",
                        "border-radius": "10px",
                        "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "width": "23%",
                        "display": "inline-block",
                        "margin": "1%",
                    },
                ),
                html.Div(
                    [
                        html.H3(
                            f"${avg_gdp:.1f}B",
                            style={"color": "#f39c12", "margin": "0"},
                        ),
                        html.P("平均GDP", style={"margin": "5px 0"}),
                    ],
                    style={
                        "text-align": "center",
                        "background": "white",
                        "padding": "20px",
                        "border-radius": "10px",
                        "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "width": "23%",
                        "display": "inline-block",
                        "margin": "1%",
                    },
                ),
            ]
        )

    else:
        # 天氣統計
        if region_filter == "all":
            filtered_data = global_weather_data
        else:
            filtered_data = global_weather_data[
                global_weather_data["region"] == region_filter
            ]

        if len(filtered_data) > 0:
            avg_temp = filtered_data["temperature"].mean()
            max_temp = filtered_data["temperature"].max()
            min_temp = filtered_data["temperature"].min()
            avg_humidity = filtered_data["humidity"].mean()

            return html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                f"{avg_temp:.1f}°C",
                                style={"color": "#e74c3c", "margin": "0"},
                            ),
                            html.P("平均溫度", style={"margin": "5px 0"}),
                        ],
                        style={
                            "text-align": "center",
                            "background": "white",
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                            "width": "23%",
                            "display": "inline-block",
                            "margin": "1%",
                        },
                    ),
                    html.Div(
                        [
                            html.H3(
                                f"{max_temp:.1f}°C",
                                style={"color": "#d35400", "margin": "0"},
                            ),
                            html.P("最高溫度", style={"margin": "5px 0"}),
                        ],
                        style={
                            "text-align": "center",
                            "background": "white",
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                            "width": "23%",
                            "display": "inline-block",
                            "margin": "1%",
                        },
                    ),
                    html.Div(
                        [
                            html.H3(
                                f"{min_temp:.1f}°C",
                                style={"color": "#3498db", "margin": "0"},
                            ),
                            html.P("最低溫度", style={"margin": "5px 0"}),
                        ],
                        style={
                            "text-align": "center",
                            "background": "white",
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                            "width": "23%",
                            "display": "inline-block",
                            "margin": "1%",
                        },
                    ),
                    html.Div(
                        [
                            html.H3(
                                f"{avg_humidity:.0f}%",
                                style={"color": "#2980b9", "margin": "0"},
                            ),
                            html.P("平均濕度", style={"margin": "5px 0"}),
                        ],
                        style={
                            "text-align": "center",
                            "background": "white",
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                            "width": "23%",
                            "display": "inline-block",
                            "margin": "1%",
                        },
                    ),
                ]
            )
        else:
            return html.P("該地區暫無天氣資料", style={"text-align": "center"})


# 回調：更新資料表
@app.callback(
    Output("data-table-container", "children"),
    [
        Input("map-mode", "value"),
        Input("region-filter", "value"),
        Input("refresh-btn", "n_clicks"),
    ],
)
def update_data_table(mode, region_filter, n_clicks):
    if mode == "country":
        return dash_table.DataTable(
            columns=[
                {"name": "國家", "id": "country"},
                {
                    "name": "人口",
                    "id": "population",
                    "type": "numeric",
                    "format": {"specifier": ",.0f"},
                },
                {
                    "name": "GDP (十億美元)",
                    "id": "gdp",
                    "type": "numeric",
                    "format": {"specifier": ",.1f"},
                },
                {"name": "ISO代碼", "id": "iso_alpha"},
            ],
            data=df_countries.to_dict("records"),
            sort_action="native",
            filter_action="native",
            page_size=10,
            style_cell={"textAlign": "center"},
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
            ],
        )
    else:
        # 天氣資料表
        if region_filter == "all":
            filtered_data = global_weather_data
        else:
            filtered_data = global_weather_data[
                global_weather_data["region"] == region_filter
            ]

        return dash_table.DataTable(
            columns=[
                {"name": "城市", "id": "city"},
                {"name": "國家", "id": "country"},
                {
                    "name": "溫度 (°C)",
                    "id": "temperature",
                    "type": "numeric",
                    "format": {"specifier": ".1f"},
                },
                {
                    "name": "體感溫度 (°C)",
                    "id": "feels_like",
                    "type": "numeric",
                    "format": {"specifier": ".1f"},
                },
                {"name": "濕度 (%)", "id": "humidity", "type": "numeric"},
                {
                    "name": "氣壓 (hPa)",
                    "id": "pressure",
                    "type": "numeric",
                    "format": {"specifier": ".0f"},
                },
                {
                    "name": "風速 (m/s)",
                    "id": "wind_speed",
                    "type": "numeric",
                    "format": {"specifier": ".1f"},
                },
                {"name": "雲量 (%)", "id": "clouds", "type": "numeric"},
                {"name": "天氣", "id": "weather"},
                {"name": "更新時間", "id": "timestamp"},
            ],
            data=filtered_data.to_dict("records") if len(filtered_data) > 0 else [],
            sort_action="native",
            filter_action="native",
            page_size=15,
            style_cell={"textAlign": "center", "fontSize": "12px"},
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
            ],
        )


# 回調：更新時間顯示
@app.callback(Output("last-update", "children"), [Input("refresh-btn", "n_clicks")])
def update_last_update_time(n_clicks):
    global last_update_time
    return f"最後更新: {last_update_time}"


# 背景天氣更新任務
def background_weather_update():
    """背景執行天氣更新"""
    while True:
        time.sleep(7200)  # 2小時更新一次
        update_global_weather()


# 啟動背景更新線程
import atexit

weather_thread = threading.Thread(target=background_weather_update, daemon=True)
weather_thread.start()

if __name__ == "__main__":
    import os

    # 從環境變數獲取配置
    debug_mode = os.getenv("DASH_DEBUG", "True").lower() == "true"
    port = int(os.getenv("PORT", 8050))
    host = os.getenv("HOST", "0.0.0.0")

    print("🚀 啟動整合世界地圖應用...")
    print(
        f"📍 請在瀏覽器中開啟: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/"
    )
    print(f"🔧 Debug 模式: {'開啟' if debug_mode else '關閉'}")
    print(f"🌍 功能: 世界國家統計 + 全球天氣監測")

    app.run(debug=debug_mode, host=host, port=port)

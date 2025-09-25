import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from datetime import datetime

# 建立實時統計增強版 Dash 應用
app = dash.Dash(__name__)


# 建立地理資料
def create_geographic_data():
    """建立地理資料"""
    locations_data = {
        "city": [
            "台北",
            "台中",
            "高雄",
            "台南",
            "新竹",
            "基隆",
            "桃園",
            "嘉義",
            "宜蘭",
            "花蓮",
            "台東",
            "屏東",
            "雲林",
            "彰化",
            "南投",
            "苗栗",
        ],
        "latitude": [
            25.0330,
            24.1477,
            22.6273,
            22.9917,
            24.8138,
            25.1276,
            24.9936,
            23.4801,
            24.7021,
            23.9927,
            22.7972,
            22.5519,
            23.7092,
            24.0518,
            23.9609,
            24.5602,
        ],
        "longitude": [
            121.5654,
            120.6736,
            120.3014,
            120.2513,
            120.9647,
            121.7081,
            121.2168,
            120.4473,
            121.7195,
            121.6015,
            121.1444,
            120.5487,
            120.4313,
            120.5161,
            120.9719,
            120.8214,
        ],
        "value": np.random.randint(10, 100, 16).tolist(),
        "population": (np.random.exponential(2, 16) * 100000).astype(int).tolist(),
    }
    return pd.DataFrame(locations_data)


# 建立資料
df = create_geographic_data()


def create_stat_item(label, value, item_id):
    """建立統計項目"""
    return html.Div(
        [
            html.Div(
                [
                    html.Span(label, style={"fontWeight": "bold", "color": "#2c3e50"}),
                    html.Span(
                        value,
                        id=item_id,
                        style={
                            "float": "right",
                            "fontWeight": "bold",
                            "color": "#27ae60",
                            "backgroundColor": "rgba(39, 174, 96, 0.1)",
                            "padding": "2px 8px",
                            "borderRadius": "4px",
                            "fontFamily": "monospace",
                        },
                    ),
                ]
            )
        ],
        style={
            "padding": "10px",
            "borderBottom": "1px solid #eee",
            "transition": "background-color 0.3s ease",
        },
    )


# 應用佈局
app.layout = html.Div(
    [
        # 標題區域
        html.Div(
            [
                html.H1(
                    "🌍 實時統計增強版地圖系統",
                    style={
                        "textAlign": "center",
                        "color": "#2c3e50",
                        "marginBottom": "10px",
                        "fontFamily": "Arial, sans-serif",
                    },
                ),
                html.P(
                    "即時更新地圖統計資訊與互動式視覺化",
                    style={
                        "textAlign": "center",
                        "color": "#7f8c8d",
                        "marginBottom": "20px",
                        "fontSize": "16px",
                    },
                ),
            ],
            style={
                "backgroundColor": "#ecf0f1",
                "padding": "20px",
                "borderRadius": "10px",
                "margin": "20px",
            },
        ),
        # 主要內容區域
        html.Div(
            [
                # 左側統計面板
                html.Div(
                    [
                        html.H3(
                            "📈 實時地圖統計",
                            style={
                                "color": "#27ae60",
                                "marginBottom": "20px",
                                "textAlign": "center",
                            },
                        ),
                        # 狀態指示器
                        html.Div(
                            [
                                html.Div(
                                    "🟢",
                                    style={
                                        "fontSize": "20px",
                                        "display": "inline-block",
                                    },
                                ),
                                html.Span(
                                    "實時更新中",
                                    style={
                                        "marginLeft": "10px",
                                        "fontWeight": "bold",
                                        "color": "#27ae60",
                                    },
                                ),
                            ],
                            style={"marginBottom": "15px"},
                        ),
                        # 統計項目
                        html.Div(
                            id="stats-container",
                            children=[
                                create_stat_item(
                                    "地圖中心點", "載入中...", "map-center"
                                ),
                                create_stat_item("縮放等級", "載入中...", "zoom-level"),
                                create_stat_item("資料點數量", "0", "data-count"),
                                create_stat_item("地圖樣式", "載入中...", "map-style"),
                                create_stat_item(
                                    "最後更新", "載入中...", "last-update"
                                ),
                                create_stat_item("更新次數", "0", "update-count"),
                            ],
                        ),
                        # 控制面板
                        html.Div(
                            [
                                html.H4(
                                    "🎛️ 控制設定",
                                    style={"color": "#2c3e50", "marginBottom": "15px"},
                                ),
                                html.Label(
                                    "地圖樣式:",
                                    style={"fontWeight": "bold", "marginBottom": "5px"},
                                ),
                                dcc.Dropdown(
                                    id="map-style-dropdown",
                                    options=[
                                        {
                                            "label": "🗺️ 開放街圖",
                                            "value": "open-street-map",
                                        },
                                        {"label": "🛰️ 衛星圖", "value": "satellite"},
                                        {
                                            "label": "🌍 地形圖",
                                            "value": "stamen-terrain",
                                        },
                                        {
                                            "label": "🌫️ 淺色地圖",
                                            "value": "carto-positron",
                                        },
                                        {
                                            "label": "🌙 深色地圖",
                                            "value": "carto-darkmatter",
                                        },
                                    ],
                                    value="open-street-map",
                                    style={"marginBottom": "15px"},
                                ),
                                html.Label(
                                    "更新頻率:",
                                    style={"fontWeight": "bold", "marginBottom": "5px"},
                                ),
                                dcc.Dropdown(
                                    id="update-frequency-dropdown",
                                    options=[
                                        {"label": "⚡ 超高頻 (0.5秒)", "value": 500},
                                        {"label": "🚀 高頻 (1秒)", "value": 1000},
                                        {"label": "⭐ 標準 (2秒)", "value": 2000},
                                        {"label": "🐌 低頻 (5秒)", "value": 5000},
                                    ],
                                    value=1000,
                                    style={"marginBottom": "15px"},
                                ),
                                html.Button(
                                    "🎲 重新生成資料",
                                    id="regenerate-btn",
                                    n_clicks=0,
                                    style={
                                        "width": "100%",
                                        "padding": "10px",
                                        "backgroundColor": "#3498db",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "5px",
                                        "cursor": "pointer",
                                        "fontWeight": "bold",
                                        "marginBottom": "10px",
                                    },
                                ),
                                html.Button(
                                    "🇹🇼 回到台灣",
                                    id="reset-view-btn",
                                    n_clicks=0,
                                    style={
                                        "width": "100%",
                                        "padding": "10px",
                                        "backgroundColor": "#e74c3c",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "5px",
                                        "cursor": "pointer",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            style={
                                "backgroundColor": "#f8f9fa",
                                "padding": "15px",
                                "borderRadius": "8px",
                                "marginTop": "20px",
                            },
                        ),
                    ],
                    style={
                        "width": "30%",
                        "padding": "20px",
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                        "marginRight": "20px",
                        "height": "fit-content",
                    },
                ),
                # 右側地圖區域
                html.Div(
                    [
                        dcc.Graph(
                            id="realtime-map",
                            style={"height": "700px"},
                            config={
                                "displayModeBar": True,
                                "displaylogo": False,
                                "modeBarButtonsToAdd": ["pan2d", "select2d", "lasso2d"],
                            },
                        )
                    ],
                    style={
                        "width": "70%",
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
                        "padding": "10px",
                    },
                ),
            ],
            style={"display": "flex", "margin": "20px"},
        ),
        # 隱藏的狀態儲存
        dcc.Store(id="map-state-store"),
        dcc.Store(id="update-counter-store", data=0),
        # 定時器
        dcc.Interval(id="stats-interval", interval=1000, n_intervals=0),  # 1秒更新
    ]
)


# 回調：更新地圖
@app.callback(
    [Output("realtime-map", "figure"), Output("map-state-store", "data")],
    [
        Input("map-style-dropdown", "value"),
        Input("regenerate-btn", "n_clicks"),
        Input("reset-view-btn", "n_clicks"),
    ],
    [State("map-state-store", "data")],
)
def update_map(style, regen_clicks, reset_clicks, current_state):
    global df

    # 檢查是否需要重新生成資料
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"]
        if "regenerate-btn" in prop_id:
            df = create_geographic_data()

    # 建立地圖
    fig = go.Figure()

    # 添加散點圖
    fig.add_trace(
        go.Scattermapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            mode="markers",
            marker=dict(
                size=[max(8, val / 3) for val in df["value"]],
                color=df["value"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="數值"),
                sizemode="diameter",
                opacity=0.8,
            ),
            text=[
                f"城市: {city}<br>數值: {val}<br>人口: {pop:,}"
                for city, val, pop in zip(df["city"], df["value"], df["population"])
            ],
            hovertemplate="<b>%{text}</b><br>座標: (%{lat:.4f}, %{lon:.4f})<extra></extra>",
            name="城市資料",
        )
    )

    # 地圖樣式映射
    mapbox_styles = {
        "open-street-map": "open-street-map",
        "satellite": "satellite",
        "stamen-terrain": "stamen-terrain",
        "carto-positron": "carto-positron",
        "carto-darkmatter": "carto-darkmatter",
    }

    # 設定地圖佈局
    center_lat = 23.8
    center_lon = 121.0
    zoom_level = 6.5

    # 檢查是否需要重設視角
    if ctx.triggered and "reset-view-btn" in ctx.triggered[0]["prop_id"]:
        center_lat = 23.8
        center_lon = 121.0
        zoom_level = 6.5
    elif current_state:
        center_lat = current_state.get("center_lat", 23.8)
        center_lon = current_state.get("center_lon", 121.0)
        zoom_level = current_state.get("zoom", 6.5)

    fig.update_layout(
        mapbox=dict(
            style=mapbox_styles.get(style, "open-street-map"),
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom_level,
        ),
        showlegend=True,
        margin=dict(r=0, t=0, l=0, b=0),
        height=700,
    )

    # 儲存地圖狀態
    map_state = {
        "center_lat": center_lat,
        "center_lon": center_lon,
        "zoom": zoom_level,
        "style": style,
        "data_count": len(df),
    }

    return fig, map_state


# 回調：更新統計資訊
@app.callback(
    [
        Output("map-center", "children"),
        Output("zoom-level", "children"),
        Output("data-count", "children"),
        Output("map-style", "children"),
        Output("last-update", "children"),
        Output("update-count", "children"),
        Output("update-counter-store", "data"),
    ],
    [Input("stats-interval", "n_intervals"), Input("realtime-map", "relayoutData")],
    [
        State("map-state-store", "data"),
        State("map-style-dropdown", "value"),
        State("update-counter-store", "data"),
    ],
)
def update_stats(n_intervals, relayout_data, map_state, current_style, update_count):
    # 更新計數器
    update_count = (update_count or 0) + 1

    # 取得當前時間
    current_time = datetime.now().strftime("%H:%M:%S")

    # 從 relayout_data 取得地圖狀態
    if relayout_data and map_state:
        center_lat = relayout_data.get(
            "mapbox.center.lat", map_state.get("center_lat", 23.8)
        )
        center_lon = relayout_data.get(
            "mapbox.center.lon", map_state.get("center_lon", 121.0)
        )
        zoom = relayout_data.get("mapbox.zoom", map_state.get("zoom", 6.5))
        data_count = map_state.get("data_count", len(df))
    elif map_state:
        center_lat = map_state.get("center_lat", 23.8)
        center_lon = map_state.get("center_lon", 121.0)
        zoom = map_state.get("zoom", 6.5)
        data_count = map_state.get("data_count", len(df))
    else:
        center_lat = 23.8
        center_lon = 121.0
        zoom = 6.5
        data_count = len(df)

    # 樣式名稱映射
    style_names = {
        "open-street-map": "🗺️ 開放街圖",
        "satellite": "🛰️ 衛星圖",
        "stamen-terrain": "🌍 地形圖",
        "carto-positron": "🌫️ 淺色地圖",
        "carto-darkmatter": "🌙 深色地圖",
    }

    return (
        f"{center_lat:.4f}, {center_lon:.4f}",
        f"{zoom:.2f}°",
        str(data_count),
        style_names.get(current_style, "未知"),
        current_time,
        str(update_count),
    )


# 回調：更新定時器頻率
@app.callback(
    Output("stats-interval", "interval"), [Input("update-frequency-dropdown", "value")]
)
def update_interval_frequency(frequency):
    return frequency


if __name__ == "__main__":
    print("🚀 正在啟動實時統計增強版地圖系統...")
    print("📍 請在瀏覽器中開啟: http://127.0.0.1:8050/")
    app.run_server(debug=True, port=8050)

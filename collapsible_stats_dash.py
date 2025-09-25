import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# 建立可收納統計面板 Dash 應用
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

# CSS 樣式
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @keyframes slideDown {
                from {
                    max-height: 0;
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    max-height: 500px;
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideUp {
                from {
                    max-height: 500px;
                    opacity: 1;
                    transform: translateY(0);
                }
                to {
                    max-height: 0;
                    opacity: 0;
                    transform: translateY(-20px);
                }
            }
            
            @keyframes pulse {
                0%, 100% { 
                    transform: scale(1);
                    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4);
                }
                50% { 
                    transform: scale(1.05);
                    box-shadow: 0 0 0 10px rgba(40, 167, 69, 0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .collapsible-panel {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-left: 4px solid #28a745;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            }
            
            .collapsible-panel:hover {
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
                transform: translateY(-2px);
            }
            
            .panel-header {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 1rem 1.5rem;
                cursor: pointer;
                transition: all 0.3s ease;
                user-select: none;
                position: relative;
                overflow: hidden;
            }
            
            .panel-header:hover {
                background: linear-gradient(135deg, #218838 0%, #1e8a7a 100%);
            }
            
            .panel-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .panel-header:hover::before {
                left: 100%;
            }
            
            .panel-title {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 0;
                font-size: 1.2rem;
                font-weight: 600;
                position: relative;
                z-index: 1;
            }
            
            .toggle-icon {
                font-size: 1.5rem;
                transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            }
            
            .collapsed .toggle-icon {
                transform: rotate(-90deg);
            }
            
            .panel-content {
                transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
                overflow: hidden;
            }
            
            .collapsed .panel-content {
                animation: slideUp 0.5s ease-out forwards;
                max-height: 0 !important;
            }
            
            .expanded .panel-content {
                animation: slideDown 0.5s ease-out forwards;
            }
            
            .stat-item-dash {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.8rem 1.5rem;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                animation: fadeInUp 0.6s ease forwards;
                opacity: 0;
            }
            
            .stat-item-dash:nth-child(1) { animation-delay: 0.1s; }
            .stat-item-dash:nth-child(2) { animation-delay: 0.2s; }
            .stat-item-dash:nth-child(3) { animation-delay: 0.3s; }
            .stat-item-dash:nth-child(4) { animation-delay: 0.4s; }
            .stat-item-dash:nth-child(5) { animation-delay: 0.5s; }
            .stat-item-dash:nth-child(6) { animation-delay: 0.6s; }
            
            .stat-item-dash:hover {
                background-color: rgba(40, 167, 69, 0.05);
                transform: translateX(5px);
                border-radius: 8px;
            }
            
            .stat-item-dash:last-child {
                border-bottom: none;
            }
            
            .stat-label-dash {
                font-weight: 600;
                color: #495057;
                font-size: 0.95rem;
            }
            
            .stat-value-dash {
                font-weight: 700;
                color: #28a745;
                background: rgba(40, 167, 69, 0.1);
                padding: 0.4rem 0.8rem;
                border-radius: 20px;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                border: 2px solid transparent;
                transition: all 0.3s ease;
            }
            
            .stat-value-updating {
                animation: pulse 0.8s ease-in-out;
                background: rgba(40, 167, 69, 0.2);
                border-color: #28a745;
            }
            
            .auto-collapse-timer {
                position: absolute;
                top: 10px;
                right: 60px;
                background: rgba(255, 255, 255, 0.9);
                color: #28a745;
                padding: 4px 12px;
                border-radius: 15px;
                font-size: 0.75rem;
                font-weight: bold;
                animation: pulse 2s infinite;
            }
            
            .update-indicator {
                position: absolute;
                bottom: 10px;
                right: 15px;
                background: rgba(40, 167, 69, 0.1);
                color: #28a745;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.7rem;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# 應用佈局
app.layout = html.Div(
    [
        # 標題區域
        html.Div(
            [
                html.H1(
                    "🌍 可收納統計面板地圖系統 (Dash版)",
                    style={
                        "textAlign": "center",
                        "color": "#2c3e50",
                        "marginBottom": "10px",
                        "fontFamily": "Arial, sans-serif",
                    },
                ),
                html.P(
                    "智能收納統計面板，展開時自動更新數據，具備流暢動畫效果",
                    style={
                        "textAlign": "center",
                        "color": "#7f8c8d",
                        "marginBottom": "20px",
                        "fontSize": "16px",
                    },
                ),
            ],
            style={
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
                "padding": "30px",
                "borderRadius": "15px",
                "margin": "20px",
            },
        ),
        # 主要內容區域
        html.Div(
            [
                # 左側統計面板
                html.Div(
                    [
                        # 可收納統計面板
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            "📊 實時地圖統計", className="panel-title"
                                        ),
                                        html.Span("▼", className="toggle-icon"),
                                    ],
                                    className="panel-header",
                                    id="stats-panel-header",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    "🔍 當前縮放級別",
                                                    className="stat-label-dash",
                                                ),
                                                html.Div(
                                                    "載入中...",
                                                    id="zoom-stat",
                                                    className="stat-value-dash",
                                                ),
                                            ],
                                            className="stat-item-dash",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "📍 中心座標",
                                                    className="stat-label-dash",
                                                ),
                                                html.Div(
                                                    "載入中...",
                                                    id="coords-stat",
                                                    className="stat-value-dash",
                                                ),
                                            ],
                                            className="stat-item-dash",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "📊 資料點數量",
                                                    className="stat-label-dash",
                                                ),
                                                html.Div(
                                                    "0",
                                                    id="points-stat",
                                                    className="stat-value-dash",
                                                ),
                                            ],
                                            className="stat-item-dash",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "🎨 地圖樣式",
                                                    className="stat-label-dash",
                                                ),
                                                html.Div(
                                                    "載入中...",
                                                    id="style-stat",
                                                    className="stat-value-dash",
                                                ),
                                            ],
                                            className="stat-item-dash",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "⏰ 最後更新",
                                                    className="stat-label-dash",
                                                ),
                                                html.Div(
                                                    "載入中...",
                                                    id="time-stat",
                                                    className="stat-value-dash",
                                                ),
                                            ],
                                            className="stat-item-dash",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "🔄 更新次數",
                                                    className="stat-label-dash",
                                                ),
                                                html.Div(
                                                    "0",
                                                    id="counter-stat",
                                                    className="stat-value-dash",
                                                ),
                                            ],
                                            className="stat-item-dash",
                                        ),
                                        html.Div(
                                            "更新中...",
                                            className="update-indicator",
                                            id="update-indicator",
                                            style={"display": "none"},
                                        ),
                                    ],
                                    className="panel-content expanded",
                                    id="stats-panel-content",
                                    style={"maxHeight": "500px", "padding": "1rem 0"},
                                ),
                                html.Div(
                                    id="auto-collapse-timer",
                                    className="auto-collapse-timer",
                                    style={"display": "none"},
                                ),
                            ],
                            className="collapsible-panel",
                            id="collapsible-panel",
                            style={"marginBottom": "20px"},
                        ),
                        # 控制面板
                        html.Div(
                            [
                                html.H4(
                                    "🎛️ 控制設定",
                                    style={
                                        "color": "#2c3e50",
                                        "marginBottom": "15px",
                                        "textAlign": "center",
                                    },
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
                                    "自動收納時間:",
                                    style={"fontWeight": "bold", "marginBottom": "5px"},
                                ),
                                dcc.Dropdown(
                                    id="auto-collapse-dropdown",
                                    options=[
                                        {"label": "3秒後收納", "value": 3},
                                        {"label": "5秒後收納", "value": 5},
                                        {"label": "8秒後收納", "value": 8},
                                        {"label": "10秒後收納", "value": 10},
                                        {"label": "關閉自動收納", "value": 0},
                                    ],
                                    value=5,
                                    style={"marginBottom": "15px"},
                                ),
                                html.Button(
                                    "🎲 重新生成資料",
                                    id="regenerate-btn",
                                    n_clicks=0,
                                    style={
                                        "width": "100%",
                                        "padding": "12px",
                                        "background": "linear-gradient(135deg, #3498db 0%, #2980b9 100%)",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "8px",
                                        "cursor": "pointer",
                                        "fontWeight": "bold",
                                        "marginBottom": "10px",
                                        "transition": "all 0.3s ease",
                                    },
                                ),
                                html.Button(
                                    "🇹🇼 回到台灣",
                                    id="reset-view-btn",
                                    n_clicks=0,
                                    style={
                                        "width": "100%",
                                        "padding": "12px",
                                        "background": "linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "8px",
                                        "cursor": "pointer",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            style={
                                "background": "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)",
                                "padding": "20px",
                                "borderRadius": "12px",
                                "boxShadow": "0 4px 15px rgba(0,0,0,0.1)",
                            },
                        ),
                    ],
                    style={"width": "35%", "marginRight": "20px"},
                ),
                # 右側地圖區域
                html.Div(
                    [
                        dcc.Graph(
                            id="collapsible-map",
                            style={"height": "700px"},
                            config={
                                "displayModeBar": True,
                                "displaylogo": False,
                                "modeBarButtonsToAdd": ["pan2d", "select2d", "lasso2d"],
                            },
                        )
                    ],
                    style={
                        "width": "65%",
                        "background": "white",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 15px rgba(0,0,0,0.1)",
                        "padding": "10px",
                    },
                ),
            ],
            style={"display": "flex", "margin": "20px", "alignItems": "flex-start"},
        ),
        # 隱藏的狀態儲存
        dcc.Store(id="map-state-store"),
        dcc.Store(id="update-counter-store", data=0),
        dcc.Store(id="panel-collapsed-store", data=False),
        dcc.Store(id="auto-collapse-active-store", data=False),
        # 定時器
        dcc.Interval(id="stats-interval", interval=1000, n_intervals=0),
        dcc.Interval(
            id="auto-collapse-interval", interval=1000, n_intervals=0, disabled=True
        ),
    ]
)


# 回調：切換統計面板
@app.callback(
    [
        Output("collapsible-panel", "className"),
        Output("stats-panel-content", "className"),
        Output("stats-panel-header", "children"),
        Output("panel-collapsed-store", "data"),
        Output("auto-collapse-interval", "disabled"),
        Output("auto-collapse-timer", "style"),
        Output("update-indicator", "style"),
    ],
    [
        Input("stats-panel-header", "n_clicks"),
        Input("auto-collapse-interval", "n_intervals"),
    ],
    [
        State("panel-collapsed-store", "data"),
        State("auto-collapse-dropdown", "value"),
        State("auto-collapse-active-store", "data"),
    ],
)
def toggle_stats_panel(
    header_clicks, auto_intervals, is_collapsed, auto_time, auto_active
):
    ctx = callback_context

    if not ctx.triggered:
        return (
            "collapsible-panel",
            "panel-content expanded",
            [
                html.H3("📊 實時地圖統計", className="panel-title"),
                html.Span("▼", className="toggle-icon"),
            ],
            False,
            True,
            {"display": "none"},
            {"display": "none"},
        )

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # 手動切換
    if trigger_id == "stats-panel-header":
        new_collapsed = not is_collapsed

        if new_collapsed:
            # 收納狀態
            return (
                "collapsible-panel collapsed",
                "panel-content collapsed",
                [
                    html.H3("📊 實時地圖統計", className="panel-title"),
                    html.Span("▶", className="toggle-icon"),
                ],
                True,
                True,
                {"display": "none"},
                {"display": "none"},
            )
        else:
            # 展開狀態，啟動自動收納
            timer_style = {"display": "block"} if auto_time > 0 else {"display": "none"}

            return (
                "collapsible-panel expanded",
                "panel-content expanded",
                [
                    html.H3("📊 實時地圖統計", className="panel-title"),
                    html.Span("▼", className="toggle-icon"),
                ],
                False,
                auto_time == 0,  # 如果auto_time為0則禁用定時器
                timer_style,
                {"display": "block"},
            )

    # 自動收納倒計時結束
    elif (
        trigger_id == "auto-collapse-interval"
        and auto_intervals >= auto_time
        and auto_time > 0
    ):
        return (
            "collapsible-panel collapsed",
            "panel-content collapsed",
            [
                html.H3("📊 實時地圖統計", className="panel-title"),
                html.Span("▶", className="toggle-icon"),
            ],
            True,
            True,
            {"display": "none"},
            {"display": "none"},
        )

    # 預設返回當前狀態
    if is_collapsed:
        return (
            "collapsible-panel collapsed",
            "panel-content collapsed",
            [
                html.H3("📊 實時地圖統計", className="panel-title"),
                html.Span("▶", className="toggle-icon"),
            ],
            True,
            True,
            {"display": "none"},
            {"display": "none"},
        )
    else:
        timer_style = {"display": "block"} if auto_time > 0 else {"display": "none"}
        return (
            "collapsible-panel expanded",
            "panel-content expanded",
            [
                html.H3("📊 實時地圖統計", className="panel-title"),
                html.Span("▼", className="toggle-icon"),
            ],
            False,
            auto_time == 0,
            timer_style,
            {"display": "block"},
        )


# 回調：更新自動收納倒計時顯示
@app.callback(
    Output("auto-collapse-timer", "children"),
    [Input("auto-collapse-interval", "n_intervals")],
    [State("auto-collapse-dropdown", "value"), State("panel-collapsed-store", "data")],
)
def update_countdown_display(n_intervals, auto_time, is_collapsed):
    if is_collapsed or auto_time == 0:
        return ""

    remaining = max(0, auto_time - (n_intervals or 0))
    return f"⏰ {remaining}秒後自動收納"


# 回調：更新地圖
@app.callback(
    [Output("collapsible-map", "figure"), Output("map-state-store", "data")],
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
    ctx = callback_context
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
                size=[max(12, val / 4) for val in df["value"]],
                color=df["value"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="數值"),
                sizemode="diameter",
                opacity=0.8,
                line=dict(width=2, color="white"),
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
        showlegend=False,
        margin=dict(r=0, t=0, l=0, b=0),
        height=700,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
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


# 回調：更新統計資訊（展開時觸發動畫）
@app.callback(
    [
        Output("zoom-stat", "children"),
        Output("zoom-stat", "className"),
        Output("coords-stat", "children"),
        Output("coords-stat", "className"),
        Output("points-stat", "children"),
        Output("points-stat", "className"),
        Output("style-stat", "children"),
        Output("style-stat", "className"),
        Output("time-stat", "children"),
        Output("time-stat", "className"),
        Output("counter-stat", "children"),
        Output("counter-stat", "className"),
        Output("update-counter-store", "data"),
    ],
    [
        Input("stats-interval", "n_intervals"),
        Input("collapsible-map", "relayoutData"),
        Input("stats-panel-header", "n_clicks"),
    ],
    [
        State("map-state-store", "data"),
        State("map-style-dropdown", "value"),
        State("update-counter-store", "data"),
        State("panel-collapsed-store", "data"),
    ],
)
def update_stats(
    n_intervals,
    relayout_data,
    header_clicks,
    map_state,
    current_style,
    update_count,
    is_collapsed,
):
    ctx = callback_context
    is_panel_toggle = any(
        "stats-panel-header" in trigger["prop_id"] for trigger in ctx.triggered
    )

    # 如果面板收納了，不更新統計
    if is_collapsed:
        return (
            "載入中...",
            "stat-value-dash",
            "載入中...",
            "stat-value-dash",
            "0",
            "stat-value-dash",
            "載入中...",
            "stat-value-dash",
            "載入中...",
            "stat-value-dash",
            str(update_count or 0),
            "stat-value-dash",
            update_count or 0,
        )

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

    # 如果是面板切換觸發，使用更新動畫
    animate_class = (
        "stat-value-dash stat-value-updating" if is_panel_toggle else "stat-value-dash"
    )

    return (
        f"{zoom:.2f}°",
        animate_class,
        f"{center_lat:.4f}, {center_lon:.4f}",
        animate_class,
        str(data_count),
        animate_class,
        style_names.get(current_style, "未知"),
        animate_class,
        current_time,
        animate_class,
        str(update_count),
        animate_class,
        update_count,
    )


if __name__ == "__main__":
    print("🚀 正在啟動可收納統計面板地圖系統...")
    print("📍 請在瀏覽器中開啟: http://127.0.0.1:8050/")
    app.run_server(debug=True, port=8050)

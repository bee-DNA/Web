import dash
from dash import dcc, html, Input, Output, dash_table, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# 進階世界地圖應用
app = dash.Dash(__name__)


# 更豐富的範例資料
def create_extended_data():
    """建立更詳細的世界資料"""
    data = {
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
            376.8,
            95.9,
            404.1,
            2829.1,
            2715.5,
        ],
        "life_expectancy": [
            76.9,
            69.4,
            78.9,
            71.7,
            67.3,
            75.9,
            54.7,
            72.6,
            72.6,
            75.1,
            84.6,
            81.3,
            76.7,
            77.7,
            75.4,
            71.2,
            66.6,
            72.0,
            81.3,
            82.7,
        ],
        "continent": [
            "Asia",
            "Asia",
            "North America",
            "Asia",
            "Asia",
            "South America",
            "Africa",
            "Asia",
            "Europe",
            "North America",
            "Asia",
            "Europe",
            "Asia",
            "Asia",
            "Asia",
            "Asia",
            "Africa",
            "Africa",
            "Europe",
            "Europe",
        ],
    }
    return pd.DataFrame(data)


df = create_extended_data()

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "🌍 進階世界資料視覺化平台",
                    style={
                        "text-align": "center",
                        "color": "#2c3e50",
                        "margin-bottom": "20px",
                    },
                )
            ],
            style={
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "padding": "20px",
                "margin-bottom": "30px",
            },
        ),
        # 控制面板
        html.Div(
            [
                html.Div(
                    [
                        html.Label("📊 選擇資料指標：", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="metric-dropdown",
                            options=[
                                {"label": "👥 人口數量", "value": "population"},
                                {"label": "💰 GDP (十億美元)", "value": "gdp"},
                                {"label": "💗 平均壽命", "value": "life_expectancy"},
                            ],
                            value="population",
                            style={"margin-top": "10px"},
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "margin-right": "5%",
                    },
                ),
                html.Div(
                    [
                        html.Label("🎨 色彩主題：", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="color-dropdown",
                            options=[
                                {"label": "🔵 藍色系", "value": "Blues"},
                                {"label": "🔴 紅色系", "value": "Reds"},
                                {"label": "🟢 綠色系", "value": "Greens"},
                                {"label": "🌈 彩虹色", "value": "Viridis"},
                                {"label": "🟡 等離子", "value": "Plasma"},
                            ],
                            value="Viridis",
                            style={"margin-top": "10px"},
                        ),
                    ],
                    style={
                        "width": "30%",
                        "display": "inline-block",
                        "margin-right": "5%",
                    },
                ),
                html.Div(
                    [
                        html.Label("🌍 選擇洲別：", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="continent-dropdown",
                            options=[
                                {"label": "🌏 全世界", "value": "All"},
                                {"label": "🏛️ 亞洲", "value": "Asia"},
                                {"label": "🏰 歐洲", "value": "Europe"},
                                {"label": "🗽 北美洲", "value": "North America"},
                                {"label": "🌴 南美洲", "value": "South America"},
                                {"label": "🦁 非洲", "value": "Africa"},
                            ],
                            value="All",
                            style={"margin-top": "10px"},
                        ),
                    ],
                    style={"width": "30%", "display": "inline-block"},
                ),
            ],
            style={
                "margin-bottom": "30px",
                "padding": "20px",
                "background-color": "#f8f9fa",
                "border-radius": "10px",
            },
        ),
        # 世界地圖
        dcc.Graph(id="world-choropleth", style={"margin-bottom": "30px"}),
        # 統計資訊
        html.Div(id="stats-cards", style={"margin-bottom": "30px"}),
        # 資料表
        html.Div(
            [
                html.H2(
                    "📋 詳細資料表",
                    style={"text-align": "center", "margin-bottom": "20px"},
                ),
                dash_table.DataTable(
                    id="data-table",
                    columns=[
                        {"name": "🌍 國家", "id": "country"},
                        {"name": "📍 洲別", "id": "continent"},
                        {
                            "name": "👥 人口",
                            "id": "population",
                            "type": "numeric",
                            "format": {"specifier": ",.0f"},
                        },
                        {
                            "name": "💰 GDP",
                            "id": "gdp",
                            "type": "numeric",
                            "format": {"specifier": ",.1f"},
                        },
                        {
                            "name": "💗 平均壽命",
                            "id": "life_expectancy",
                            "type": "numeric",
                            "format": {"specifier": ".1f"},
                        },
                        {"name": "🏷️ ISO", "id": "iso_alpha"},
                    ],
                    sort_action="native",
                    filter_action="native",
                    page_size=15,
                    style_cell={
                        "textAlign": "center",
                        "padding": "12px",
                        "fontFamily": "Arial",
                    },
                    style_header={
                        "backgroundColor": "#3498db",
                        "color": "white",
                        "fontWeight": "bold",
                        "fontSize": "14px",
                    },
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#f8f9fa"},
                        {"if": {"row_index": "even"}, "backgroundColor": "white"},
                    ],
                ),
            ]
        ),
    ]
)


# 更新地圖的回調函數
@app.callback(
    [
        Output("world-choropleth", "figure"),
        Output("data-table", "data"),
        Output("stats-cards", "children"),
    ],
    [
        Input("metric-dropdown", "value"),
        Input("color-dropdown", "value"),
        Input("continent-dropdown", "value"),
    ],
)
def update_visualization(selected_metric, color_scale, selected_continent):
    # 過濾資料
    filtered_df = df.copy()
    if selected_continent != "All":
        filtered_df = df[df["continent"] == selected_continent]

    # 建立地圖標題
    metric_names = {
        "population": "人口分布",
        "gdp": "GDP分布",
        "life_expectancy": "平均壽命分布",
    }

    # 建立世界地圖
    fig = px.choropleth(
        filtered_df,
        locations="iso_alpha",
        color=selected_metric,
        hover_name="country",
        hover_data={
            "continent": True,
            "population": ":,.0f",
            "gdp": ":,.1f",
            "life_expectancy": ":.1f",
        },
        color_continuous_scale=color_scale,
        title=f"🌍 世界各國{metric_names[selected_metric]}",
    )

    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
        ),
        height=600,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    # 建立統計卡片
    stats_cards = create_stats_cards(filtered_df, selected_metric)

    return fig, filtered_df.to_dict("records"), stats_cards


def create_stats_cards(df, metric):
    """建立統計資訊卡片"""
    total_countries = len(df)

    if metric == "population":
        total_value = df["population"].sum()
        avg_value = df["population"].mean()
        max_country = df.loc[df["population"].idxmax(), "country"]
        unit = "人"
        format_str = "{:,.0f}"
    elif metric == "gdp":
        total_value = df["gdp"].sum()
        avg_value = df["gdp"].mean()
        max_country = df.loc[df["gdp"].idxmax(), "country"]
        unit = "十億美元"
        format_str = "{:,.1f}"
    else:  # life_expectancy
        total_value = df["life_expectancy"].mean()
        avg_value = df["life_expectancy"].mean()
        max_country = df.loc[df["life_expectancy"].idxmax(), "country"]
        unit = "歲"
        format_str = "{:.1f}"

    return html.Div(
        [
            html.Div(
                [
                    html.H3("📊 國家數量"),
                    html.H2(f"{total_countries}", style={"color": "#3498db"}),
                ],
                className="stat-card",
                style={
                    "background": "white",
                    "padding": "20px",
                    "border-radius": "10px",
                    "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
                    "text-align": "center",
                    "width": "22%",
                    "display": "inline-block",
                    "margin": "1.5%",
                },
            ),
            html.Div(
                [
                    html.H3("🏆 最高值國家"),
                    html.H2(
                        max_country, style={"color": "#e74c3c", "font-size": "16px"}
                    ),
                ],
                className="stat-card",
                style={
                    "background": "white",
                    "padding": "20px",
                    "border-radius": "10px",
                    "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
                    "text-align": "center",
                    "width": "22%",
                    "display": "inline-block",
                    "margin": "1.5%",
                },
            ),
            html.Div(
                [
                    html.H3("📈 平均值"),
                    html.H2(
                        format_str.format(avg_value) + " " + unit,
                        style={"color": "#f39c12", "font-size": "16px"},
                    ),
                ],
                className="stat-card",
                style={
                    "background": "white",
                    "padding": "20px",
                    "border-radius": "10px",
                    "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
                    "text-align": "center",
                    "width": "22%",
                    "display": "inline-block",
                    "margin": "1.5%",
                },
            ),
            html.Div(
                [
                    html.H3(
                        "💯 總計/全球平均"
                        if metric != "life_expectancy"
                        else "🌍 全球平均"
                    ),
                    html.H2(
                        format_str.format(total_value) + " " + unit,
                        style={"color": "#27ae60", "font-size": "16px"},
                    ),
                ],
                className="stat-card",
                style={
                    "background": "white",
                    "padding": "20px",
                    "border-radius": "10px",
                    "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
                    "text-align": "center",
                    "width": "22%",
                    "display": "inline-block",
                    "margin": "1.5%",
                },
            ),
        ]
    )


if __name__ == "__main__":
    print("🚀 啟動進階世界地圖應用...")
    print("📍 請在瀏覽器中開啟: http://127.0.0.1:8051/")
    print("✨ 功能包含：")
    print("   - 🌍 互動式世界地圖")
    print("   - 📊 多種資料指標")
    print("   - 🎨 可客製化色彩")
    print("   - 📋 可排序和篩選的資料表")
    print("   - 📈 即時統計資訊")
    app.run(debug=True, port=8051)

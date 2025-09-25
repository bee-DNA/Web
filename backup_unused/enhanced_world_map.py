import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 建立增強版世界地圖應用
app = dash.Dash(__name__)


# 建立更豐富的範例資料
def create_enhanced_data():
    """建立增強版世界資料"""
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
            "Italy",
            "South Africa",
            "Tanzania",
            "Myanmar",
            "Kenya",
            "South Korea",
            "Colombia",
            "Spain",
            "Ukraine",
            "Argentina",
            "Algeria",
            "Sudan",
            "Uganda",
            "Iraq",
            "Poland",
            "Canada",
            "Afghanistan",
            "Morocco",
            "Saudi Arabia",
            "Uzbekistan",
            "Peru",
            "Angola",
            "Malaysia",
            "Mozambique",
            "Ghana",
            "Yemen",
            "Nepal",
            "Venezuela",
            "Madagascar",
            "Cameroon",
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
            60461826,
            59308690,
            59734218,
            54409800,
            53771296,
            51269185,
            50882891,
            46754778,
            43733762,
            45195774,
            43851044,
            43849260,
            45741007,
            40222493,
            37846611,
            37742154,
            38928346,
            36910560,
            34813871,
            33469203,
            32971854,
            32866272,
            32365999,
            31255435,
            31072940,
            29825964,
            29136808,
            28435940,
            27691018,
            26545863,
        ],
        "gdp_per_capita": [
            10261.7,
            2104.1,
            65297.5,
            4256.2,
            1543.9,
            8717.2,
            2229.9,
            2503.4,
            11654.8,
            9946.0,
            39285.2,
            46259.0,
            2760.8,
            9042.3,
            3694.6,
            3485.3,
            936.3,
            3832.0,
            42354.4,
            40492.7,
            31952.9,
            6374.0,
            1122.1,
            1408.2,
            1838.2,
            31846.2,
            6131.2,
            27057.2,
            3659.0,
            9912.7,
            4115.0,
            977.3,
            817.7,
            4157.0,
            15694.7,
            46194.7,
            507.1,
            3190.8,
            23139.8,
            1724.9,
            6941.2,
            2108.7,
            11414.8,
            506.1,
            2202.3,
            824.1,
            1155.1,
            3242.8,
            528.5,
            1534.3,
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
            "Europe",
            "Africa",
            "Africa",
            "Asia",
            "Africa",
            "Asia",
            "South America",
            "Europe",
            "Europe",
            "South America",
            "Africa",
            "Africa",
            "Africa",
            "Asia",
            "Europe",
            "North America",
            "Asia",
            "Africa",
            "Asia",
            "Asia",
            "South America",
            "Africa",
            "Asia",
            "Africa",
            "Africa",
            "Asia",
            "Asia",
            "South America",
            "Africa",
            "Africa",
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
            "ITA",
            "ZAF",
            "TZA",
            "MMR",
            "KEN",
            "KOR",
            "COL",
            "ESP",
            "UKR",
            "ARG",
            "DZA",
            "SDN",
            "UGA",
            "IRQ",
            "POL",
            "CAN",
            "AFG",
            "MAR",
            "SAU",
            "UZB",
            "PER",
            "AGO",
            "MYS",
            "MOZ",
            "GHA",
            "YEM",
            "NPL",
            "VEN",
            "MDG",
            "CMR",
        ],
    }
    return pd.DataFrame(countries_data)


# 建立資料
df = create_enhanced_data()

# 自定義配色方案
color_schemes = {
    "海洋藍": px.colors.sequential.Blues,
    "森林綠": px.colors.sequential.Greens,
    "火焰橙": px.colors.sequential.Oranges,
    "紫羅蘭": px.colors.sequential.Purples,
    "日落紅": px.colors.sequential.Reds,
    "彩虹色": px.colors.qualitative.Plotly,
    "專業色": px.colors.qualitative.Set3,
}

# 地圖投影選項
map_projections = {
    "自然地球": "natural earth",
    "正射投影": "orthographic",
    "立體投影": "stereographic",
    "等距圓錐": "equirectangular",
    "墨卡托": "mercator",
    "羅賓森": "robinson",
}

# 應用程式佈局
app.layout = html.Div(
    [
        # 標題區域
        html.Div(
            [
                html.H1(
                    "🌍 增強版世界資料地圖",
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "color": "#2c3e50",
                        "fontFamily": "Arial, sans-serif",
                        "textShadow": "2px 2px 4px rgba(0,0,0,0.1)",
                    },
                ),
                html.P(
                    "探索全球人口與經濟資料的互動視覺化",
                    style={
                        "textAlign": "center",
                        "fontSize": "18px",
                        "color": "#7f8c8d",
                        "marginBottom": "30px",
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
        # 控制面板
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "選擇資料指標:",
                            style={"fontWeight": "bold", "marginBottom": "10px"},
                        ),
                        dcc.Dropdown(
                            id="metric-dropdown",
                            options=[
                                {"label": "👥 人口數量", "value": "population"},
                                {"label": "💰 人均GDP", "value": "gdp_per_capita"},
                            ],
                            value="population",
                            style={"marginBottom": "20px"},
                        ),
                    ],
                    style={
                        "width": "23%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "marginRight": "2%",
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "選擇大洲:",
                            style={"fontWeight": "bold", "marginBottom": "10px"},
                        ),
                        dcc.Dropdown(
                            id="continent-dropdown",
                            options=[{"label": "🌍 全部大洲", "value": "all"}]
                            + [
                                {"label": continent, "value": continent}
                                for continent in df["continent"].unique()
                            ],
                            value="all",
                            style={"marginBottom": "20px"},
                        ),
                    ],
                    style={
                        "width": "23%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "marginRight": "2%",
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "配色方案:",
                            style={"fontWeight": "bold", "marginBottom": "10px"},
                        ),
                        dcc.Dropdown(
                            id="color-scheme-dropdown",
                            options=[
                                {"label": name, "value": name}
                                for name in color_schemes.keys()
                            ],
                            value="海洋藍",
                            style={"marginBottom": "20px"},
                        ),
                    ],
                    style={
                        "width": "23%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                        "marginRight": "2%",
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "地圖投影:",
                            style={"fontWeight": "bold", "marginBottom": "10px"},
                        ),
                        dcc.Dropdown(
                            id="projection-dropdown",
                            options=[
                                {"label": name, "value": proj}
                                for name, proj in map_projections.items()
                            ],
                            value="natural earth",
                            style={"marginBottom": "20px"},
                        ),
                    ],
                    style={
                        "width": "23%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                    },
                ),
            ],
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "margin": "20px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            },
        ),
        # 統計卡片
        html.Div(id="stats-cards", style={"margin": "20px"}),
        # 地圖區域
        html.Div(
            [dcc.Graph(id="world-map", style={"height": "600px"})],
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "margin": "20px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            },
        ),
        # 資料表格
        html.Div(
            [
                html.H3(
                    "📊 詳細資料", style={"marginBottom": "20px", "color": "#2c3e50"}
                ),
                dash_table.DataTable(
                    id="data-table",
                    columns=[
                        {"name": "國家", "id": "country"},
                        {"name": "大洲", "id": "continent"},
                        {
                            "name": "人口",
                            "id": "population",
                            "type": "numeric",
                            "format": {"specifier": ",.0f"},
                        },
                        {
                            "name": "人均GDP (USD)",
                            "id": "gdp_per_capita",
                            "type": "numeric",
                            "format": {"specifier": ",.1f"},
                        },
                    ],
                    sort_action="native",
                    page_size=15,
                    style_cell={"textAlign": "left", "padding": "10px"},
                    style_header={
                        "backgroundColor": "#3498db",
                        "color": "white",
                        "fontWeight": "bold",
                    },
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#f8f9fa"}
                    ],
                ),
            ],
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "margin": "20px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
            },
        ),
    ]
)


# 更新統計卡片
@app.callback(
    Output("stats-cards", "children"),
    [Input("metric-dropdown", "value"), Input("continent-dropdown", "value")],
)
def update_stats_cards(metric, continent):
    # 篩選資料
    if continent == "all":
        filtered_df = df
    else:
        filtered_df = df[df["continent"] == continent]

    if metric == "population":
        total_value = filtered_df["population"].sum()
        avg_value = filtered_df["population"].mean()
        max_country = filtered_df.loc[filtered_df["population"].idxmax(), "country"]
        max_value = filtered_df["population"].max()
        unit = "人"
        title = "人口統計"
        icon = "👥"
    else:
        total_value = None
        avg_value = filtered_df["gdp_per_capita"].mean()
        max_country = filtered_df.loc[filtered_df["gdp_per_capita"].idxmax(), "country"]
        max_value = filtered_df["gdp_per_capita"].max()
        unit = "USD"
        title = "GDP統計"
        icon = "💰"

    cards = []

    # 總計卡片（僅人口）
    if total_value:
        cards.append(
            html.Div(
                [
                    html.H4(
                        f"{icon} 總{title}", style={"margin": "0", "color": "#2c3e50"}
                    ),
                    html.H2(
                        f"{total_value:,.0f} {unit}",
                        style={"margin": "10px 0", "color": "#e74c3c"},
                    ),
                ],
                style={
                    "backgroundColor": "#ffffff",
                    "padding": "20px",
                    "borderRadius": "10px",
                    "textAlign": "center",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "border": "1px solid #bdc3c7",
                },
            )
        )

    # 平均值卡片
    cards.append(
        html.Div(
            [
                html.H4(f"📊 平均{title}", style={"margin": "0", "color": "#2c3e50"}),
                html.H2(
                    f"{avg_value:,.1f} {unit}",
                    style={"margin": "10px 0", "color": "#f39c12"},
                ),
            ],
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "textAlign": "center",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "border": "1px solid #bdc3c7",
            },
        )
    )

    # 最高值卡片
    cards.append(
        html.Div(
            [
                html.H4(f"🏆 最高{title}", style={"margin": "0", "color": "#2c3e50"}),
                html.H2(
                    f"{max_value:,.1f} {unit}",
                    style={"margin": "10px 0", "color": "#27ae60"},
                ),
                html.P(f"({max_country})", style={"margin": "0", "color": "#7f8c8d"}),
            ],
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "borderRadius": "10px",
                "textAlign": "center",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "border": "1px solid #bdc3c7",
            },
        )
    )

    return html.Div(
        cards,
        style={
            "display": "flex",
            "justifyContent": "space-around",
            "flexWrap": "wrap",
            "gap": "20px",
        },
    )


# 更新地圖
@app.callback(
    Output("world-map", "figure"),
    [
        Input("metric-dropdown", "value"),
        Input("continent-dropdown", "value"),
        Input("color-scheme-dropdown", "value"),
        Input("projection-dropdown", "value"),
    ],
)
def update_map(metric, continent, color_scheme, projection):
    # 篩選資料
    if continent == "all":
        filtered_df = df
        title_suffix = "全球"
    else:
        filtered_df = df[df["continent"] == continent]
        title_suffix = continent

    # 設定標題和單位
    if metric == "population":
        title = f"👥 {title_suffix}人口分布"
        hover_name = "人口"
        color_label = "人口數量"
    else:
        title = f"💰 {title_suffix}人均GDP分布"
        hover_name = "人均GDP"
        color_label = "人均GDP (USD)"

    # 選擇配色
    if color_scheme in ["彩虹色", "專業色"]:
        color_continuous_scale = color_schemes[color_scheme]
        color_discrete_map = None
    else:
        color_continuous_scale = color_schemes[color_scheme]
        color_discrete_map = None

    # 建立地圖
    fig = px.choropleth(
        filtered_df,
        locations="iso_alpha",
        color=metric,
        hover_name="country",
        hover_data={
            "population": ":,.0f",
            "gdp_per_capita": ":,.1f",
            "continent": True,
        },
        color_continuous_scale=color_continuous_scale,
        labels={
            "population": "人口",
            "gdp_per_capita": "人均GDP (USD)",
            "continent": "大洲",
        },
        title=title,
    )

    # 更新佈局
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type=projection,
            bgcolor="rgba(0,0,0,0)",
        ),
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "family": "Arial, sans-serif"},
        },
        coloraxis_colorbar=dict(title=dict(text=color_label, font=dict(size=14))),
        font={"family": "Arial, sans-serif"},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


# 更新資料表格
@app.callback(Output("data-table", "data"), [Input("continent-dropdown", "value")])
def update_table(continent):
    if continent == "all":
        filtered_df = df
    else:
        filtered_df = df[df["continent"] == continent]

    return filtered_df.to_dict("records")


if __name__ == "__main__":
    import os

    app.run(
        debug=os.getenv("DASH_DEBUG", "True").lower() == "true",
        host=os.getenv("DASH_HOST", "0.0.0.0"),
        port=int(os.getenv("DASH_PORT", 8050)),
    )

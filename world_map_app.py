import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests

# 建立 Dash 應用
app = dash.Dash(__name__)


# 範例資料：世界各國人口資料
def create_sample_data():
    """建立範例世界資料"""
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
        ],
    }
    return pd.DataFrame(countries_data)


# 建立範例資料
df = create_sample_data()

# 應用程式佈局
app.layout = html.Div(
    [
        html.H1(
            "🌍 世界資料互動地圖",
            style={"text-align": "center", "margin-bottom": "30px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("選擇資料類型："),
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
            style={"margin-bottom": "30px"},
        ),
        # 世界地圖
        dcc.Graph(id="world-map"),
        html.Hr(),
        # 資料表
        html.H2("📊 資料表", style={"text-align": "center"}),
        dash_table.DataTable(
            id="data-table",
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
            data=df.to_dict("records"),
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
        ),
    ]
)


# 回調函數：更新世界地圖
@app.callback(
    Output("world-map", "figure"),
    [Input("data-dropdown", "value"), Input("color-dropdown", "value")],
)
def update_world_map(selected_data, color_scale):
    # 建立地圖
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color=selected_data,
        hover_name="country",
        hover_data={"population": ":,.0f", "gdp": ":,.1f"},
        color_continuous_scale=color_scale,
        title=f"世界各國 {'人口分布' if selected_data == 'population' else 'GDP分布'}",
    )

    fig.update_layout(
        title_x=0.5,
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        height=600,
    )

    return fig


if __name__ == "__main__":
    print("🚀 啟動 Dash 應用...")
    print("📍 請在瀏覽器中開啟: http://127.0.0.1:8050/")
    app.run(debug=True, port=8050)

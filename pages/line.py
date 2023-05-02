from dash import html, dcc, Input, Output, callback
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from init_data import dfs
from comps import common_component
from datetime import datetime


dash.register_page(__name__, name="Line")

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        common_component(),
                    ],
                    width=4,
                    class_name="ms-5 text-center",
                ),
                dbc.Col(dcc.Graph("line-graph")),
            ],
        ),
    ]
)


# @callback(
#     Output("line-graph", "figure"),
#     Input("level", "value"),
#     Input("select-region", "value"),
#     Input("select-state", "value"),
#     Input("select-city", "value"),
#     Input("select-region", "options"),
#     Input("select-state", "options"),
#     Input("select-city", "options"),
#     Input("all-region", "value"),
#     Input("all-state", "value"),
#     Input("all-city", "value"),
#     Input("date", "start_date"),
#     Input("date", "end_date"),
#     Input("case", "value"),
# )
# def update_line(
#     level: str,
#     region_value: list[str],
#     state_value: list[str],
#     city_value: list[str],
#     region_option: list[str],
#     state_option: list[str],
#     city_option: list[str],
#     all_region: bool,
#     all_state: bool,
#     all_city: bool,
#     start: str,
#     end: str,
#     case: list[str],
# ):
#     valid_region = bool(region_value) or all_region
#     valid_state = bool(state_value) or all_state
#     valid_city = bool(city_value) or all_city

#     if level == "City" and valid_region and valid_state and valid_city:
#         regions = set()
#         states = set()
#         cities = set()
#         for val in city_option if all_city else city_value:
#             arr = val.split(" / ")
#             regions.add(arr[0])
#             states.add(arr[1])
#             cities.add(arr[2])
#         df = df_orig[
#             (df_orig["Region"].isin(regions))
#             & (df_orig["State"].isin(states))
#             & (df_orig["City"].isin(cities))
#             & (df_orig["Date"] >= datetime.strptime(start[:10], "%Y-%m-%d"))
#             & (df_orig["Date"] <= datetime.strptime(end[:10], "%Y-%m-%d"))
#         ]
#         return px.line(df, x="Date", y=case[0], color=["Region", "State", "City"])

#     return px.line()

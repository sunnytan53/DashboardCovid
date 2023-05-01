from dash import html, dcc, Input, Output, callback
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from global_data import df_final, common_component, levels
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


@callback(
    Output("line-graph", "figure"),
    Input("level", "value"),
    Input("select-region", "value"),
    Input("select-state", "value"),
    Input("select-city", "value"),
    Input("select-region", "options"),
    Input("select-state", "options"),
    Input("select-city", "options"),
    Input("all-region", "value"),
    Input("all-state", "value"),
    Input("all-city", "value"),
    Input("date", "start_date"),
    Input("date", "end_date"),
)
def update_line(
    level: str,
    region_value: list[str],
    state_value: list[str],
    city_value: list[str],
    region_option: list[str],
    state_option: list[str],
    city_option: list[str],
    all_region: bool,
    all_state: bool,
    all_city: bool,
    start: str,
    end: str,
):
    valid_region = bool(region_value) or all_region
    valid_state = bool(state_value) or all_state
    valid_city = bool(city_value) or all_city

    if level == "City" and valid_region and valid_state and valid_city:
        for val in city_option if all_city else city_value:
            region, state, city = val.split(" / ")
    # if locations is None:
    #     return px.line()
    # df = df_final[
    #     (df_final[level].isin(locations))
    #     & (df_final["Date"] >= datetime.strptime(start[:10], "%Y-%m-%d"))
    #     & (df_final["Date"] <= datetime.strptime(end[:10], "%Y-%m-%d"))
    # ]
    return px.line()

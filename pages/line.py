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
    Input("case", "value"),
)
def update_line(
    level: str,
    region_values: list[str],
    state_values: list[str],
    city_values: list[str],
    region_option: list[str],
    state_option: list[str],
    city_option: list[str],
    all_region: bool,
    all_state: bool,
    all_city: bool,
    start: str,
    end: str,
    case: list[str],
):
    valid_region = bool(region_values) or all_region
    valid_state = bool(state_values) or all_state
    valid_city = bool(city_values) or all_city

    if level == "City" and valid_region and valid_state and valid_city:
        print(city_values)
        df = dfs[level]
        mask = (df["Date"] >= datetime.strptime(start[:10], "%Y-%m-%d")) & (
            df["Date"] <= datetime.strptime(end[:10], "%Y-%m-%d")
        )
        if not all_city:
            mask &= df[level].isin(city_values)
        return px.line(df[mask], x="Date", y=case, color=level)

    return px.line()

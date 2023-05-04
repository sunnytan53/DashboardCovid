from dash import html, dcc, Input, Output, callback
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from init_data import dfs
from comps import common_component
from datetime import datetime
import pandas as pd


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
                dbc.Col(
                    dbc.Spinner(dcc.Graph("line-graph"), size="md", delay_show=300)
                ),
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
    Input("cumu", "value"),
)
def update_line(
    level: str,
    region_values: list[str],
    state_values: list[str],
    city_values: list[str],
    region_options: list[str],
    state_options: list[str],
    city_options: list[str],
    all_region: bool,
    all_state: bool,
    all_city: bool,
    start: str,
    end: str,
    case_cat: str,
    to_cumu: bool,
):
    valid_region = bool(region_values) or all_region
    valid_state = bool(state_values) or all_state
    valid_city = bool(city_values) or all_city

    df = dfs[level]
    mask = None
    if level == "City":
        if valid_region and valid_state and valid_city:
            mask = df[level].isin(city_options if all_city else city_values)

    elif level == "State":
        if valid_region and valid_state:
            mask = df[level].isin(state_options if all_state else state_values)

    elif level == "Region":
        if valid_region:
            mask = df[level].isin(region_options if all_region else region_values)

    if mask is None:
        return px.line()

    case_cat += " Cases"
    mask &= (df["Date"] >= datetime.strptime(start[:10], "%Y-%m-%d")) & (
        df["Date"] <= datetime.strptime(end[:10], "%Y-%m-%d")
    )

    df = df[mask]
    if to_cumu:
        df = df.drop(
            "Death Cases" if case_cat == "Confirmed Cases" else "Confirmed Cases",
            axis=1,
        )
        df_list = []
        for _, x in df.groupby(level):
            x[case_cat] = x[case_cat].cumsum()
            df_list.append(x)
        df = pd.concat(df_list)

    return px.line(df, x="Date", y=case_cat, color=level)

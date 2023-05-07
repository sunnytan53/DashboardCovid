from dash import Input, Output, callback
import plotly.express as px
from init_data import get_df
from datetime import datetime
import pandas as pd


@callback(
    Output("graph", "figure"),
    Output("full-graph", "figure"),
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
    Input("period", "value"),
    Input("active-page", "pathname"),
)
def update_graph(  # can't use _name here sine import will ignore this function
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
    to_cumu: str,
    period: str,
    active_page: str,
):
    valid_region = bool(region_values) or all_region
    valid_state = bool(state_values) or all_state
    valid_city = bool(city_values) or all_city

    df = get_df(level, period[0])
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


    active_page = active_page[1:]
    if mask is None:
        if active_page == "bar":
            fig = px.bar()
        else:
            fig = px.line()
        return fig, fig

    case_cat += " Cases"
    mask &= (df["Date"] >= datetime.strptime(start[:10], "%Y-%m-%d")) & (
        df["Date"] <= datetime.strptime(end[:10], "%Y-%m-%d")
    )
    df = df[mask]

    if to_cumu == "Cumulative":
        df_list = []
        for _, x in df.groupby(level):
            x[case_cat] = x[case_cat].cumsum()
            df_list.append(x)
        df = pd.concat(df_list)

    if active_page == "bar":
        fig = px.bar(df, x="Date", y=case_cat, color=level)
    else:
        fig = px.line(df, x="Date", y=case_cat, color=level)
    return fig, fig

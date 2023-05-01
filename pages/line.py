from dash import html, dcc, Input, Output, callback
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from global_data import (
    df_final,
    level_component,
    date_component,
)
from datetime import datetime


dash.register_page(__name__, name="Line")

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        # this will be instantly replaced by the real Dropdown
                        level_component(),
                        date_component(),
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
#     Input("line-level", "value"),
#     Input("line-select", "value"),
#     Input("line-date", "start_date"),
#     Input("line-date", "end_date"),
# )
# def update_line(level: str, locations: list, start: str, end: str):
#     if locations is None:
#         return px.line()
#     df = df_final[
#         (df_final[level].isin(locations))
#         & (df_final["Date"] >= datetime.strptime(start[:10], "%Y-%m-%d"))
#         & (df_final["Date"] <= datetime.strptime(end[:10], "%Y-%m-%d"))
#     ]
#     return px.line(
#         df,
#         "Date",
#         "Death Cases",
#         color=level,
#     )

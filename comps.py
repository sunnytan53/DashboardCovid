from dash import dcc, html
import dash_bootstrap_components as dbc
from init_data import levels, empty_figure

border = " my-2 py-2 border border-secondary fs-5 "


def _level():
    return dbc.Row(
        [
            dbc.Row(
                [
                    dbc.Col("Level:", width=1),
                    dbc.Col(
                        dcc.RadioItems(
                            levels,
                            value="Region",
                            inline=True,
                            id="level",
                            labelClassName="px-3 mx-1 bg-warning",
                        ),
                    ),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            multi=True,
                            id="select-region",
                            placeholder="Click to search, or select all",
                        )
                    ),
                    dbc.Col(
                        dbc.Checkbox(
                            id="all-region",
                            label="All regions",
                            className="text-danger",
                        ),
                        width=4,
                    ),
                ],
                className="pt-3",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(multi=True, id="select-state")),
                    dbc.Col(
                        dbc.Checkbox(
                            id="all-state", label="All states", className="text-danger"
                        ),
                        width=4,
                    ),
                ],
                className="pt-3",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(multi=True, id="select-city")),
                    dbc.Col(
                        dbc.Checkbox(
                            id="all-city", label="All cities", className="text-danger"
                        ),
                        width=4,
                    ),
                ],
                className="pt-3",
            ),
        ],
        class_name=border,
    )


def _category(page: str):
    has_agg = page in ["pie", "map"]
    return dbc.Row(
        [
            dbc.Row(
                [
                    dbc.Col("Case:", width=1),
                    dbc.Col(
                        dcc.RadioItems(
                            ["Confirmed", "Death"],
                            id="case",
                            value="Confirmed",
                            inline=True,
                            labelClassName="px-3 mx-1 bg-warning",
                        ),
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col("Type:", width=2),
                    dbc.Col(
                        dcc.RadioItems(
                            ["Cumulative (auto/force)"]
                            if has_agg
                            else ["Cumulative", "Individual"],
                            id="cumu",
                            value="Cumulative (auto/force)" if has_agg else "Cumulative",
                            inline=True,
                            labelClassName="px-3 mx-1 bg-warning",
                        )
                    ),
                ],
                className="pt-3",
            ),
        ],
        className=border,
    )


def _date(page: str):
    has_agg = page in ["pie", "map"]
    return dbc.Row(
        [
            dbc.Row(
                [
                    dbc.Col("Period:", width=2),
                    dbc.Col(
                        dcc.RadioItems(
                            ["Month (auto/force)"]
                            if has_agg
                            else ["Day", "Week", "Month", "Quarter", "Year"],
                            id="period",
                            inline=True,
                            value="Month (auto/force)" if has_agg else "Month",
                            labelClassName="px-3 mx-1 mt-1 bg-warning",
                        ),
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col("Range:", width=2),
                    dbc.Col(
                        dcc.DatePickerRange(
                            id="date",
                            clearable=True,
                            show_outside_days=True,
                        )
                    ),
                ],
                className="pt-3",
            ),
        ],
        className="pt-3" + border,
    )


def _option(page: str):
    row = None
    if page == "bar":
        row = [
            html.B("Bar Options", className="text-info"),
            dbc.Row(
                [
                    dbc.Col("Column:", width=1),
                    dbc.Col(
                        dcc.RadioItems(
                            ["Stack", "Group"],
                            value="Stack",
                            inline=True,
                            id="bar-column",
                            labelClassName="px-3 mx-1 bg-warning",
                        ),
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col("Orientation:", width=1),
                    dbc.Col(
                        dcc.RadioItems(
                            ["Vertical", "Horizontal"],
                            value="Vertical",
                            inline=True,
                            id="bar-orient",
                            labelClassName="px-3 mx-1 bg-warning",
                        )
                    ),
                ],
                className="pt-2",
            ),
            dbc.RadioItems(id="line-marker"),
            dbc.RadioItems(id="pie-hole"),
        ]
    elif page == "pie":
        row = [
            html.B("Pie Options", className="text-info"),
            dbc.Row(
                [
                    dbc.Col("Hole:", width=1),
                    dbc.Col(dcc.Slider(0, 0.5, step=0.1, id="pie-hole", value=0)),
                ]
            ),
            dbc.RadioItems(id="line-marker"),
            dbc.RadioItems(id="bar-column"),
            dbc.RadioItems(id="bar-orient"),
        ]
    elif page == "map":
        row = [
            html.B("No Map Options", className="text-info"),
            dbc.RadioItems(id="pie-hole"),
            dbc.RadioItems(id="line-marker"),
            dbc.RadioItems(id="bar-column"),
            dbc.RadioItems(id="bar-orient"),
        ]
    else:
        row = [
            html.B("Line Options", className="text-info"),
            dbc.Row(
                [
                    dbc.Col("Marker:", width=1),
                    dbc.Col(
                        dcc.RadioItems(
                            ["None", "Simple", "Complex"],
                            value="None",
                            inline=True,
                            id="line-marker",
                            labelClassName="px-3 mx-1 bg-warning",
                        ),
                    ),
                ]
            ),
            dbc.RadioItems(id="bar-column"),
            dbc.RadioItems(id="bar-orient"),
            dbc.RadioItems(id="pie-hole"),
        ]

    return dbc.Row(row, className=border)


def get_page_layout(page: str):
    return dbc.Tabs(
        [
            dbc.Tab(
                dbc.Row(
                    [
                        dbc.Col(
                            children=[
                                _level(),
                                _category(page),
                                _date(page),
                                _option(page),
                            ],
                            class_name="ms-5 text-center",
                        ),
                        dbc.Col(
                            dbc.Spinner(
                                dcc.Graph("graph", figure=empty_figure),
                                size="md",
                                delay_show=300,
                            ),
                            width=8,
                        ),
                    ],
                ),
                label="Default",
                tab_id="default",
            ),
            dbc.Tab(
                dbc.Spinner(
                    dcc.Graph("full-graph", figure=empty_figure),
                    size="md",
                    delay_show=300,
                ),
                label="Fullscreen Graph",
            ),
            dcc.Location("active-page"),
        ],
        className="px-5 bg-info",
        active_tab="default",
    )


def get_home_layout():
    return None

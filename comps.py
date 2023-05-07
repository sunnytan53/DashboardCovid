from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
from init_data import *


def _level(border: str):
    return dbc.Row(
        [
            dbc.Row(
                [
                    dbc.Col("Level: ", width=1),
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
                className="fs-5",
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


def _category(border: str):
    return dbc.Row(
        [
            dbc.Row(
                [
                    dbc.Col("Case: ", width=1),
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
                    dbc.Col("Type: ", width=2),
                    dbc.Col(
                        dcc.RadioItems(
                            ["Individual", "Cumulative"],
                            id="cumu",
                            value="Individual",
                            inline=True,
                            labelClassName="px-3 mx-1 bg-warning",
                        )
                    ),
                ],
                className="pt-3",
            ),
        ],
        className="fs-5" + border,
    )


def _date(border: str):
    return dbc.Row(
        [
            dbc.Row(
                dbc.Col(
                    [
                        dcc.DatePickerRange(id="date"),
                        dbc.Button("reset", id="reset-time", className="ms-3"),
                    ]
                ),
            ),
            dbc.Row(
                [
                    dbc.Col("Period: ", width=2, className="pt-3"),
                    dbc.Col(
                        dcc.RadioItems(
                            ["Day", "Week", "Month", "Quarter", "Year"],
                            id="period",
                            inline=True,
                            value="Month",
                            labelClassName="px-3 mx-1 mt-1 bg-warning",
                        ),
                    ),
                ]
            ),
        ],
        className="pt-3 fs-5" + border,
    )


def get_page_layout(page: str):
    border = " my-2 py-2 border border-secondary "
    return dbc.Tabs(
        [
            dbc.Tab(
                dbc.Row(
                    [
                        dbc.Col(
                            children=[_level(border), _category(border), _date(border)],
                            class_name="ms-5 text-center",
                        ),
                        dbc.Col(
                            dbc.Spinner(dcc.Graph("graph"), size="md", delay_show=300),
                            width=8,
                        ),
                    ],
                ),
                label="Default",
                tab_id="default",
            ),
            dbc.Tab(
                dbc.Spinner(dcc.Graph("full-graph"), size="md", delay_show=300),
                label="Fullscreen Graph",
            ),
            dcc.Location("active-page"),
        ],
        className="px-5 bg-info",
        active_tab="default",
    )


###
### Callbacks
###
@callback(
    Output("select-region", "options"),
    Input("level", "value"),
)
def _switch_select_region(level: str):
    if level == "State":
        return region_has_states
    elif level == "City":
        return region_has_cities
    return region_no_limit


@callback(
    Output("select-state", "placeholder"),
    Output("select-state", "options"),
    Output("select-state", "value"),
    Output("select-state", "disabled"),
    Input("level", "value"),
    Input("select-region", "value"),
    Input("select-region", "options"),
    Input("all-region", "value"),
    Input("all-state", "value"),
)
def _switch_select_state(
    level: str,
    values: list[str],
    region_options: list[str],
    all_region: bool,
    all_state: bool,
):
    ret = ["Select a region above, or check all", [], [], True]
    if level == "Region":
        ret[0] = "Not state or city level"
    else:
        if all_region:
            values = region_options
        if values:
            region_to_state = (
                region_to_state_city if level == "City" else region_to_state_state
            )
            for region in values:
                for state in region_to_state[region]:
                    state_str = f"{region} / {state}"
                    ret[1].append(state_str)
            # show states
            ret[1].sort()
            if all_state:
                ret[0] = "All states selected"
            else:
                ret[3] = False
                ret[0] = "Click to search/select states"
    # empty selection
    return ret


@callback(
    Output("select-city", "placeholder"),
    Output("select-city", "options"),
    Output("select-city", "value"),
    Output("select-city", "disabled"),
    Input("level", "value"),
    Input("select-state", "value"),
    Input("select-state", "options"),
    Input("all-state", "value"),
    Input("all-city", "value"),
)
def _switch_select_city(
    level: str,
    values: str,
    state_options: list[str],
    all_state: bool,
    all_city: bool,
):
    ret = ["Select a state above, or check all", [], [], True]
    if level != "City":
        ret[0] = "Not city level"
    else:
        if all_state:
            values = state_options
        if values:
            for x in values:
                region, state = x.split(" / ")
                for city in state_to_city[state]:
                    ret[1].append(f"{x} / {city}")
            # show cities
            ret[1].sort()
            if all_city:
                ret[3] = True
                ret[0] = "All cities selected"
            else:
                ret[3] = False
                ret[0] = "Click to search/select cities"
    # empty selection
    return ret


@callback(
    Output("all-region", "disabled"),
    Output("all-state", "disabled"),
    Output("all-city", "disabled"),
    Output("all-region", "value"),
    Output("all-state", "value"),
    Output("all-city", "value"),
    Input("level", "value"),
)
def _swtich_all(level: str):
    arr = [False] * 3 + [False] * 3
    if level == "Region":
        arr[1] = True
        arr[2] = True
    elif level == "State":
        arr[2] = True
    return arr


@callback(
    Output("select-region", "placeholder"),
    Output("select-region", "value"),
    Output("select-region", "disabled"),
    Input("all-region", "value"),
)
def _select_all_region(all_region: bool):
    if all_region:
        return "All regions selected", [], True
    return "Click to search/select regions", [], False


@callback(
    Output("date", "start_date"),
    Output("date", "end_date"),
    Output("date", "min_date_allowed"),
    Output("date", "max_date_allowed"),
    Input("level", "value"),
    Input("period", "value"),
)
def _switch_date_by_level(level: str, period: str):
    df = get_df(level, period[0])
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    return min_date, max_date, min_date, max_date


last_click = -1


@callback(
    Output("date", "start_date", True),
    Output("date", "end_date", True),
    Input("reset-time", "n_clicks"),
    Input("date", "disabled"),
    Input("date", "start_date"),
    Input("date", "end_date"),
    Input("date", "min_date_allowed"),
    Input("date", "max_date_allowed"),
    prevent_initial_call=True,
)
def _reset_time(
    click: int,
    disabled: bool,
    cur_start: str,
    cur_end: str,
    orig_start: str,
    orig_end: str,
):
    global last_click
    if not disabled and last_click != click:
        last_click = click
        if orig_start and orig_end:
            return orig_start, orig_end
    return cur_start, cur_end

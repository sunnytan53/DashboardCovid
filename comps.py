from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
from init_data import *


def _level():
    return dcc.RadioItems(
        levels,
        "Region",
        inline=True,
        id="level",
        className="pt-3 fs-5",
        labelClassName="px-3",
    )


def _select():
    return dbc.Row(
        [
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
                        width=3,
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
                        width=3,
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
                        width=3,
                    ),
                ],
                className="pt-3",
            ),
        ]
    )


def _date_case():
    return dbc.Row(
        [
            dbc.Col(dcc.DatePickerRange(id="date", disabled=True)),
            dbc.Col(
                dbc.RadioItems(
                    ["Confirmed Cases", "Death Cases"],
                    id="case",
                    value="Confirmed Cases",
                ),
                width=3,
            ),
        ],
        className="pt-3",
    )


def common_component():
    return html.Div(
        [
            _level(),
            _select(),
            _date_case(),
        ]
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
    Output("date", "disabled"),
    Output("date", "start_date"),
    Output("date", "end_date"),
    Output("date", "min_date_allowed"),
    Output("date", "max_date_allowed"),
    Input("level", "value"),
    Input("select-region", "value"),
    Input("select-state", "value"),
    Input("select-city", "value"),
    Input("all-region", "value"),
    Input("all-state", "value"),
    Input("all-city", "value"),
)
def _switch_date_by_level(
    level: str,
    region_values: list[str],
    state_values: list[str],
    city_values: list[str],
    all_region: bool,
    all_state: bool,
    all_city: bool,
):
    df: pd.DataFrame = None
    if level == "Region":
        if region_values:
            df = dfs[level]
            df = df[df[level].isin(region_values)]
        elif all_region:
            df = dfs[level]
    elif level == "State" and (region_values or all_region):
        if state_values:
            df = dfs[level]
            df = df[df[level].isin(state_values)]
        elif all_state:
            df = dfs[level]
    elif (
        level == "City"
        and (region_values or all_region)
        and (state_values or all_state)
    ):
        if city_values:
            df = dfs[level]
            df = df[df[level].isin(city_values)]
        elif all_city:
            df = dfs[level]

    if df is not None:
        min_date = df["Date"].min()
        max_date = df["Date"].max()
        return False, min_date, max_date, min_date, max_date

    return [True] + [None] * 4

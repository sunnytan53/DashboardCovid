import pandas as pd
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc


df_final = pd.read_csv(
    "data.zip",
    dtype={  # shrik memory usage by converting known types
        "City": "category",
        "State": "category",
        "Region": "category",
        "Confirmed Cases": "uint32",
        "Death Cases": "uint32",
    },
    parse_dates=["Date"],
    nrows=400000,
)

# df.info()
min_date = df_final["Date"].min()
max_date = df_final["Date"].max()

levels = ["Region", "State", "City"]
locations = {}
for _, row in df_final[levels].drop_duplicates(levels, ignore_index=True).iterrows():
    row = [x if type(x) == str else "Unassigned" for x in list(row)]

    locations.setdefault(row[0], {})
    locations[row[0]].setdefault(row[1], set())
    locations[row[0]][row[1]].add(row[2])

for region in locations.values():
    for state, city in region.items():
        state = sorted(city)


def date_component():
    return html.Div(
        [
            html.B("Date Range", className="pe-3 fs-5"),
            dcc.DatePickerRange(
                id="date",
                start_date=min_date,
                end_date=max_date,
                min_date_allowed=min_date,
                max_date_allowed=max_date,
            ),
        ]
    )


### Shared Components & Callbacks
def level_component():
    return html.Div(
        [
            dcc.RadioItems(
                levels,
                "Region",
                inline=True,
                id="level",
                className="pt-3 fs-5",
                labelClassName="px-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            list(locations.keys()),
                            multi=True,
                            id="select-region",
                            placeholder="Click to search, or select all",
                        )
                    ),
                    dbc.Col(dbc.Checkbox(id="all-region", label="All regions"), width=3),
                ],
                className="pt-3",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(multi=True, id="select-state")),
                    dbc.Col(dbc.Checkbox(id="all-state", label="All states"), width=3),
                ],
                className="pt-3",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(multi=True, id="select-city")),
                    dbc.Col(dbc.Checkbox(id="all-city", label="All cities"), width=3),
                ],
                className="pt-3",
            ),
        ]
    )


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
def switch_select_state(
    level: str,
    values: list,
    region_options: list,
    all_region: bool,
    all_state: bool,
):
    ret = ["Select a region first", [], [], True]
    if level == "Region":
        ret[0] = "Not state or city level"
    else:
        if all_region:
            values = region_options
        if values:
            for region in values:
                for state in locations[region].keys():
                    ret[1].append(f"{region} / {state}")
            # show states
            ret[1] = sorted(ret[1])
            if all_state:
                ret[3] = True
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
def switch_select_city(
    level: str,
    values: str,
    state_options: list,
    all_state: bool,
    all_city: bool,
):
    ret = ["Select a state first", [], [], True]
    if level != "City":
        ret[0] = "Not city level"
    else:
        if all_state:
            values = state_options
        if values:
            for x in values:
                region, state = x.split(" / ")
                for city in locations[region][state]:
                    ret[1].append(f"{x} / {city}")
            # show cities
            ret[1] = sorted(ret[1])
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
    Input("level", "value"),
)
def swtich_all(level: str):
    arr = [False] * 3
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
def select_all_region(all_region: list):
    if all_region:
        return "All regions selected", [], True
    return "Click to search/select regions", [], False

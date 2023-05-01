import pandas as pd
from dash import dcc, html, callback, Input, Output


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
                className="pt-3 s-5",
                labelClassName="px-3",
            ),
            dcc.Dropdown(
                list(locations.keys()),
                placeholder="Click to search/select regions",
                multi=True,
                id="select-region",
                className="pt-3",
            ),
            dcc.Dropdown(multi=True, id="select-state", className="pt-3"),
            dcc.Dropdown(multi=True, id="select-city", className="pt-3"),
        ],
        className="justify-content-evenly",
    )


@callback(
    Output("select-state", "placeholder"),
    Output("select-state", "disabled"),
    Output("select-state", "options"),
    Output("select-state", "value"),
    Input("level", "value"),
    Input("select-region", "value"),
)
def switch_select_state(level: str, values: list):
    if level == "Region":
        return "Not state or city level", True, [], []

    if values:
        arr = []
        for region in values:
            for state in locations[region].keys():
                arr.append(f"{region} - {state}")
        return "Click to search/select state", False, sorted(arr), []
    # empty selection
    return "Select a region first", True, [], []


@callback(
    Output("select-city", "placeholder"),
    Output("select-city", "disabled"),
    Output("select-city", "options"),
    Output("select-city", "value"),
    Input("level", "value"),
    Input("select-state", "value"),
)
def switch_select_city(level: str, values: str):
    if level == "City":
        if values:
            arr = []
            for x in values:
                region, state = x.split(" - ")
                for city in locations[region][state]:
                    arr.append(f"{region} - {state} - {city}")
            # show cities
            return "Click to search/select cities", False, sorted(arr), []
        # empty selection
        return "Select a state first", True, [], []

    return "Not city level", True, [], []

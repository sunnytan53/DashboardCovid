import pandas as pd
import plotly.express as px

levels = ["Region", "State", "City"]
empty_figure = px.pie()

_dfs: dict[str, pd.DataFrame] = {x: {} for x in levels}
_dfs_loc: dict[str, pd.DataFrame] = {}


def get_df(level: str, freq: str):
    if freq not in _dfs[level]:
        _dfs[level][freq] = pd.read_csv(
            f"data/{level}/{freq}.zip",
            dtype={  # shrink memory usage by converting known types
                level: "string",
                "Confirmed Cases": "int",
                "Death Cases": "int",
            },
            parse_dates=["Date"],
        )

    return _dfs[level][freq]


def get_df_loc(level: str):
    if level not in _dfs_loc:
        _dfs[level] = pd.read_csv(
            f"data/{level}/loc.zip",
            dtype={  # shrink memory usage by converting known types
                level: "string",
                "Latitude Cases": "float",
                "Longitude": "float",
            },
        )

    return _dfs_loc[level]


# calling method to get global data
# the reason is because Python keeps all variables in one scope
def _get_values():
    region_no_limit = set()
    region_has_states = set()
    region_has_cities = set()
    state_has_cities = set()
    region_to_state_state = {}
    region_to_state_city = {}
    state_to_city = {}

    for _, row in (
        get_df(levels[0], "M").drop_duplicates(levels[0], ignore_index=True).iterrows()
    ):
        region_no_limit.add(row[levels[0]])
    for _, row in (
        get_df(levels[1], "M").drop_duplicates(levels[1], ignore_index=True).iterrows()
    ):
        r, s = row[levels[1]].split(" / ")
        region_has_states.add(r)
        region_to_state_state.setdefault(r, set())
        region_to_state_state[r].add(s)
    for _, row in (
        get_df(levels[2], "M").drop_duplicates(levels[2], ignore_index=True).iterrows()
    ):
        r, s, c = row[levels[2]].split(" / ")
        region_has_cities.add(r)
        state_has_cities.add(s)
        region_to_state_city.setdefault(r, set())
        region_to_state_city[r].add(s)
        state_to_city.setdefault(s, set())
        state_to_city[s].add(c)

    for d in [region_to_state_state, region_to_state_city, state_to_city]:
        for k, v in d.items():
            d[k] = sorted(v)

    return (
        sorted(region_no_limit),
        sorted(region_has_states),
        sorted(region_has_cities),
        sorted(state_has_cities),
        region_to_state_state,
        region_to_state_city,
        state_to_city,
    )


(
    region_no_limit,
    region_has_states,
    region_has_cities,
    state_has_cities,
    region_to_state_state,
    region_to_state_city,
    state_to_city,
) = _get_values()

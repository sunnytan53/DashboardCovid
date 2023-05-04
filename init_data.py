import pandas as pd

levels = ["Region", "State", "City"]

dfs: dict[str, pd.DataFrame] = {}
for x in levels:
    dfs[x] = pd.read_csv(
        f"data_{x.lower()}.zip",
        dtype={  # shrink memory usage by converting known types
            x: "string",
            "Confirmed Cases": "int",
            "Death Cases": "int",
        },
        parse_dates=["Date"],
        nrows=400000,
    )


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
        dfs[levels[0]].drop_duplicates(levels[0], ignore_index=True).iterrows()
    ):
        region_no_limit.add(row[levels[0]])
    for _, row in (
        dfs[levels[1]].drop_duplicates(levels[1], ignore_index=True).iterrows()
    ):
        r, s = row[levels[1]].split(" / ")
        region_has_states.add(r)
        region_to_state_state.setdefault(r, set())
        region_to_state_state[r].add(s)
    for _, row in (
        dfs[levels[2]].drop_duplicates(levels[2], ignore_index=True).iterrows()
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

import pandas as pd
from dash import dcc, html


pages = ["line", "bar", "pie"]

df = pd.read_csv(
    "data.zip",
    dtype={  # shrik memory usage by converting known types
        "City": "category",
        "State": "category",
        "Region": "category",
        "Confirmed Cases": "int32",
        "Death Cases": "int32",
    },
    parse_dates=["Date"],
    # nrows=400000,
)

# df.info()
min_date = df["Date"].min()
max_date = df["Date"].max()


def get_level_component(id: str):
    return dcc.RadioItems(["City", "State", "Region"], "Region", id=id)


def get_date_component(id: str):
    return dcc.DatePickerRange(
        id=id,
        start_date=min_date,
        end_date=max_date,
        min_date_allowed=min_date,
        max_date_allowed=max_date,
    )

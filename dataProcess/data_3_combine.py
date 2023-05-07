# This file combine columns based on locations
# this will generate 3 dataframes in daily format

import pandas as pd
import os

df_in = pd.read_csv(
    "data_after_convert.zip",
    dtype={  # shrink memory usage by converting known types
        "City": "category",
        "State": "category",
        "Region": "category",
        "Confirmed Cases": "int",
        "Death Cases": "int",
    },
    parse_dates=["Date"],
)

for x in ["Region", "State", "City"]:
    p = f"data/{x}"
    if not os.path.exists(p):
        os.makedirs(p)


print("*** exporting data_region.zip")
df_in.drop(["State", "City"], axis=1).groupby(
    ["Region", "Date"], as_index=False
).sum().sort_values(["Region", "Date"]).to_csv(
    "data/Region/D.zip", compression="zip", index=False
)

print("*** exporting data_state.zip")
df_out = df_in.drop(["City"], axis=1).dropna(subset=["State"])
df_out["State"] = (
    df_out["Region"].astype(str) + " / " + df_out["State"].astype(str)
).astype("category")
df_out.drop(["Region"], axis=1).groupby(
    ["State", "Date"], as_index=False
).sum().sort_values(["State", "Date"]).to_csv(
    "data/State/D.zip", compression="zip", index=False
)
del df_out

print("*** exporting data_city.zip")
df_out = df_in.dropna(subset=["State", "City"])
df_out["City"] = (
    df_out["Region"]
    .str.cat([df_out["State"], df_out["City"]], " / ")
    .astype("category")
)
df_out.drop(["Region", "State"], axis=1).sort_values(["City", "Date"]).to_csv(
    "data/City/D.zip", compression="zip", index=False
)
# This file combine columns based on locations
# this will generate the final files, which are 3 dataframes
# they are corresponding to the 3 levels of locations

import pandas as pd

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

print("*** exporting data_region.zip")
df_in.drop(["State", "City"], axis=1).groupby(
    ["Region", "Date"], as_index=False
).sum().to_csv("data_region.zip", compression="zip", index=False)

print("*** exporting data_state.zip")
df_out = df_in.drop(["City"], axis=1).dropna(subset=["State"])
df_out["State"] = (
    df_out["Region"].astype(str) + " / " + df_out["State"].astype(str)
).astype("category")
df_out.drop(["Region"], axis=1).groupby(["State", "Date"], as_index=False).sum().to_csv(
    "data_state.zip", compression="zip", index=False
)
del df_out

print("*** exporting data_city.zip")
df_out = df_in.dropna(subset=["State", "City"])
df_out["City"] = df_out["Region"].str.cat([df_out["State"], df_out["City"]], " / ").astype("category")
df_out.drop(["Region", "State"], axis=1).to_csv(
    "data_city.zip", compression="zip", index=False
)

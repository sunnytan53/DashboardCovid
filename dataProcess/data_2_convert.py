# This file convert cumulative data into daily data

import pandas as pd

df_in = pd.read_csv(
    "data_after_extract.zip",
    dtype={  # shrink memory usage by converting known types
        "City": "category",
        "State": "category",
        "Region": "category",
        "Confirmed Cases": "int",
        "Death Cases": "int",
    },
    parse_dates=["Date"],
)


print("*** convert cumulative data into daily data")
print("*** this will take a minute, look at progress")
df_list = []
df_loc = df_in.drop_duplicates(["City", "State", "Region"], ignore_index=True)
for i, row in df_loc.iterrows():
    print(f"* progress: {i}/{df_loc.shape[0]}", end="\r")

    df = df_in[
        (
            (df_in["City"] == row["City"])
            if (type(row["City"]) == str)
            else (df_in["City"].isna())
        )
        & (
            (df_in["State"] == row["State"])
            if (type(row["State"]) == str)
            else (df_in["State"].isna())
        )
        & (df_in["Region"] == row["Region"])
    ].sort_values(["Date"])

    df["Confirmed Cases"] = df["Confirmed Cases"].diff()
    df["Death Cases"] = df["Death Cases"].diff()
    df = df[1:]  # MUST delete the first row because it becomes NaN
    df["Confirmed Cases"] = df["Confirmed Cases"].astype(int)
    df["Death Cases"] = df["Death Cases"].astype(int)

    df_list.append(df)


print("*** exporting data_after_convert.zip")
df_out = pd.concat(df_list, ignore_index=True)
df_out.info()
df_out.to_csv("data_after_convert.zip", compression="zip", index=False)

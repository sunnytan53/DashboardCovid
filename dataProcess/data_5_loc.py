# This file simply extract location
# NOT combined with step 1 for ease of use

import pandas as pd
import os

df_list = []
path = "csse_covid_19_daily_reports/"  # include "/" at the end
skipped = 0

print("*** get location from daily report")
for filename in os.listdir(path):
    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(
                path + filename,
                usecols=[
                    "Admin2",
                    "Province_State",
                    "Country_Region",
                    "Lat",
                    "Long_",
                ],
            )
            df_list.append(df)
        except:  # skip files in early dates that are not in standard format
            skipped += 1
print("total skipped:", skipped)

df_out = pd.concat(df_list, ignore_index=True).rename(
    columns={
        "Admin2": "City",
        "Province_State": "State",
        "Country_Region": "Region",
        "Lat": "Latitude",
        "Long_": "Longitude",
    }
).dropna(subset=["Latitude", "Longitude"]).drop_duplicates(ignore_index=True)
df_out.info()


print("*** exporting data_region.zip")
df_out.drop(["State", "City"], axis=1).groupby(
    ["Region"], as_index=False
).sum().sort_values(["Region"]).to_csv(
    "data/Region/loc.zip", compression="zip", index=False
)

print("*** exporting data_state.zip")
df_2 = df_out.drop(["City"], axis=1).dropna(subset=["State"])
df_2["State"] = (
    df_2["Region"].astype(str) + " / " + df_2["State"].astype(str)
).astype("category")
df_2.drop(["Region"], axis=1).groupby(
    ["State"], as_index=False
).sum().sort_values(["State"]).to_csv(
    "data/State/loc.zip", compression="zip", index=False
)
del df_2

print("*** exporting data_city.zip")
df_out = df_out.dropna(subset=["State", "City"])
df_out["City"] = (
    df_out["Region"]
    .str.cat([df_out["State"], df_out["City"]], " / ")
    .astype("category")
)
df_out.drop(["Region", "State"], axis=1).sort_values(["City"]).to_csv(
    "data/City/loc.zip", compression="zip", index=False
)
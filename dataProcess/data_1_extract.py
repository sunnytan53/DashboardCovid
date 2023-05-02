# This file simply extract useful data and rename needed data

import pandas as pd
import os


def get_date(d: str):
    return pd.to_datetime(d, format="%m-%d-%Y").date()


df_list = []
last_skip = get_date("01-01-2000")
path = "csse_covid_19_daily_reports/"  # include "/" at the end

print("*** get all data from daily report")
for filename in os.listdir(path):
    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(
                path + filename,
                usecols=[
                    "Admin2",
                    "Province_State",
                    "Country_Region",
                    "Confirmed",
                    "Deaths",
                ],
            )
            df["Date"] = get_date(filename[:-4])
            df["Confirmed"] = df["Confirmed"].fillna(0).astype(int)
            df["Deaths"] = df["Deaths"].fillna(0).astype(int)
            df_list.append(df)
        except:  # skip files in early dates that are not in standard format
            last_skip = max(get_date(filename[:-4]), last_skip)
print("last skipped date:", last_skip)

df_out = pd.concat(df_list, ignore_index=True).rename(
    columns={
        "Admin2": "City",
        "Province_State": "State",
        "Country_Region": "Region",
        "Confirmed": "Confirmed Cases",
        "Deaths": "Death Cases",
        "Date": "Date",
    }
)
df_out.info()
print("*** exporting data_after_extract.zip")
df_out.to_csv("data_after_extract.zip", compression="zip", index=False)

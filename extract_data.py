import pandas as pd
import os


def get_date(d: str):
    return pd.to_datetime(d, format="%m-%d-%Y").date()


df_list = []
last_skip = get_date("01-01-2018")
path = "csse_covid_19_daily_reports/"

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


df_final = (
    pd.concat(df_list, ignore_index=True)
    .rename(
        columns={
            "Admin2": "city",
            "Province_State": "state",
            "Country_Region": "region",
            "Confirmed": "confirmed",
            "Deaths": "deaths",
            "Date": "date",
        }
    )
    .sort_values(["date", "region", "state", "city"])
)
df_final.info()


df_final.to_csv("data.zip", compression="zip", index=False)

import pandas as pd
import os


def get_date(d: str):
    return pd.to_datetime(d, format="%m-%d-%Y").date()


df_list = []
last_skip = get_date("01-01-2000")
path = "csse_covid_19_daily_reports/"

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


print("*** convert cumulative data into daily data")
df_2 = pd.concat(df_list, ignore_index=True).rename(
    columns={
        "Admin2": "City",
        "Province_State": "State",
        "Country_Region": "Region",
        "Confirmed": "Confirmed Cases",
        "Deaths": "Death Cases",
        "Date": "Date",
    }
)

df_list = []
df_3 = df_2.drop_duplicates(["City", "State", "Region"], ignore_index=True)
for i, row in df_3.iterrows():
    print(f"* progress: {i}/{df_3.shape[0]}", end="\r")

    df = df_2[
        (
            (df_2["City"] == row["City"])
            if (type(row["City"]) == str)
            else (df_2["City"].isna())
        )
        & (
            (df_2["State"] == row["State"])
            if (type(row["State"]) == str)
            else (df_2["State"].isna())
        )
        & (df_2["Region"] == row["Region"])
    ].sort_values(["Date"])

    df["Confirmed Cases"] = df["Confirmed Cases"].diff()
    df["Death Cases"] = df["Death Cases"].diff()
    df = df[1:]  # MUST delete the first row because it becomes NaN
    df["Confirmed Cases"] = df["Confirmed Cases"].astype(int).clip(lower=0)
    df["Death Cases"] = df["Death Cases"].astype(int).clip(lower=0)

    df_list.append(df)


print("*** finalize and export into data.zip")
df_final = pd.concat(df_list, ignore_index=True).sort_values(
    ["Date", "Region", "State", "City"]
)
df_final.info()
df_final.to_csv("data.zip", compression="zip", index=False)

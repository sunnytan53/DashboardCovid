# This file prepares different periods of data
# since they are small, storing them is easy

import pandas as pd

for level in ["Region", "State", "City"]:
    df = pd.read_csv(
        f"data/{level}/D.zip",
        dtype={  # shrink memory usage by converting known types
            level: "category",
            "Confirmed Cases": "int",
            "Death Cases": "int",
        },
        parse_dates=["Date"],
    )

    print(f"*** exporting all periods of {level}")
    for freq in ["W", "M", "Y", "Q"]:
        df_list = []
        for _, x in df.groupby(level):
            x_new = (
                x.groupby(x["Date"].dt.to_period(freq))[
                    ["Confirmed Cases", "Death Cases"]
                ]
                .sum()
                .reset_index()
            )
            x_new[level] = x.iloc[0][level]
            x_new["Date"] = x_new["Date"].astype("datetime64[ns]")
            df_list.append(x_new)
        pd.concat(df_list).to_csv(
            f"data/{level}/{freq}.zip", compression="zip", index=False
        )

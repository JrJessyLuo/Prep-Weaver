import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Cyclists with no purchases recorded (i.e., did not purchase any racing bike)
no_purchase_ids = t1.loc[~t1["id"].isin(t2["cyclist_id"].dropna().unique()), "id"]

# Split nation_result into nation and result
nr = t1["nation_result"].astype("string").str.split("|", n=1, expand=True)
t1["nation"] = nr[0]
t1["result"] = nr[1]

out = (
    t1.loc[t1["id"].isin(no_purchase_ids), ["name", "nation", "result"]]
      .reset_index(drop=True)
)

result = {"cyclists_no_racing_bike_purchase": out}

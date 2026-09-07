import pandas as pd

bikes = tables["table_1"].copy()
cyclists = tables["table_2"].copy()
purchases = tables["table_3"].copy()

# Parse cyclist time from heat_result (e.g., "4-4:16.571" -> "4:16.571")
time_str = cyclists["heat_result"].astype(str).str.split("-", n=1).str[-1]

# Convert "m:ss.xxx" to total seconds
mm_ss = time_str.str.split(":", n=1, expand=True)
cyclists["time_seconds"] = pd.to_numeric(mm_ss[0], errors="coerce") * 60 + pd.to_numeric(mm_ss[1], errors="coerce")

# Threshold time "4:21.558"
thr_min, thr_sec = "4:21.558".split(":")
thr_seconds = float(thr_min) * 60 + float(thr_sec)

# Cyclists with better (faster) results
better_cyclists = cyclists.loc[cyclists["time_seconds"] < thr_seconds, ["id"]]

# Join to purchases and bikes
bikes["bike_name"] = bikes["product_material"].astype(str).str.split("###", n=1).str[0]

out = (
    purchases.merge(better_cyclists, left_on="cid", right_on="id", how="inner")
             .merge(bikes[["id", "bike_name"]], left_on="bike_id", right_on="id", how="inner")
)

result_df = out[["bike_name"]].drop_duplicates().reset_index(drop=True)

result = {"racing_bike_names": result_df}

import pandas as pd

pa = tables["table_1"].copy()
kv = tables["table_2"].copy()

# Pivot key-value player table to wide (one row per player)
kv["variable"] = pd.to_numeric(kv["variable"], errors="coerce")
wide = (
    kv.dropna(subset=["variable"])
      .pivot_table(index="variable", columns="id", values="value", aggfunc="first")
      .reset_index()
      .rename(columns={"variable": "player_api_id"})
)

# Find player_api_id(s) for "Aaron Doran"
name_cols = [c for c in wide.columns if any(k in str(c).lower() for k in ["name", "player_name", "fullname", "full_name"])]
if name_cols:
    mask = False
    for c in name_cols:
        mask = mask | wide[c].astype(str).str.strip().str.lower().eq("aaron doran")
    player_ids = wide.loc[mask, "player_api_id"].dropna().astype("int64").unique()
else:
    # Fallback: look for the name anywhere in the values
    mask = wide.astype(str).apply(lambda s: s.str.lower().eq("aaron doran")).any(axis=1)
    player_ids = wide.loc[mask, "player_api_id"].dropna().astype("int64").unique()

avg_rating = pa.loc[pa["player_api_id"].isin(player_ids), "overall_rating"].mean()

result = {
    "average_overall_rating": pd.DataFrame({"average_overall_rating": [avg_rating]})
}

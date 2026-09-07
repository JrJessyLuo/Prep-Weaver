import pandas as pd

pa = tables["table_1"].copy()
meta = tables["table_2"].copy()

# Player with the highest overall rating (break ties by most recent date, then smallest player_api_id)
pa["date"] = pd.to_datetime(pa["date"], errors="coerce")
top_player_api_id = (
    pa.dropna(subset=["overall_rating", "player_api_id"])
      .sort_values(["overall_rating", "date", "player_api_id"], ascending=[False, False, True])
      .iloc[0]["player_api_id"]
)

# Build mapping: player_api_id -> birthday from the transposed meta table (table_2)
meta_idx = meta.set_index("mc")
cols = [c for c in meta_idx.columns if c in meta_idx.columns]

mapping = pd.DataFrame({
    "player_api_id": pd.to_numeric(meta_idx.loc["player_api_id", cols], errors="coerce"),
    "birthday": meta_idx.loc["birthday", cols]
}).dropna(subset=["player_api_id"])

mapping["player_api_id"] = mapping["player_api_id"].astype("int64")
mapping["birthday"] = pd.to_datetime(mapping["birthday"], errors="coerce")

birthday = mapping.loc[mapping["player_api_id"].eq(int(top_player_api_id)), "birthday"].iloc[0]

result = {
    "highest_overall_player_birthday": pd.DataFrame({"birthday": [birthday]})
}

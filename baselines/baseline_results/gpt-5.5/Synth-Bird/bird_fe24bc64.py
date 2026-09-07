import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Normalize join key types + weight
t1["player_api_id"] = pd.to_numeric(t1["player_api_id"], errors="coerce")
t2["player_api_id"] = pd.to_numeric(t2["player_api_id"], errors="coerce")
t2["weight"] = pd.to_numeric(t2["weight"], errors="coerce")

# One preferred_foot value per player (take first non-null)
foot = (
    t1.loc[t1["preferred_foot"].notna(), ["player_api_id", "preferred_foot"]]
      .dropna(subset=["player_api_id"])
      .sort_values(["player_api_id"])
      .drop_duplicates(subset=["player_api_id"], keep="first")
)
foot["preferred_foot"] = foot["preferred_foot"].astype(str).str.strip().str.lower()

merged = t2.merge(foot, on="player_api_id", how="inner")

count_left = merged.loc[
    (merged["weight"] < 130) & (merged["preferred_foot"] == "left"),
    "player_api_id"
].nunique()

result = {
    "players_under_130_left_preferred_foot_count": pd.DataFrame(
        {"num_players": [count_left]}
    )
}

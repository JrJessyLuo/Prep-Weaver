import pandas as pd

pa = tables["table_2"].copy()
attr = tables["table_1"].copy()

# Birth year filter (1987-1992 inclusive)
pa["birthday"] = pd.to_datetime(pa["birthday"], errors="coerce")
pa["birth_year"] = pa["birthday"].dt.year
cohort = pa.loc[pa["birth_year"].between(1987, 1992, inclusive="both"), ["player_api_id"]].dropna()

# One preferred_foot value per player (use most recent non-null if multiple)
attr["date"] = pd.to_datetime(attr["date"], errors="coerce")
attr = attr.sort_values(["player_api_id", "date"])
pref = (
    attr.dropna(subset=["preferred_foot"])
        .groupby("player_api_id", as_index=False)["preferred_foot"]
        .last()
)

# Join and compute percentage
df = cohort.merge(pref, on="player_api_id", how="inner")
total_players = df["player_api_id"].nunique()
left_players = df.loc[df["preferred_foot"].str.lower().eq("left"), "player_api_id"].nunique()
percentage_left = (left_players / total_players * 100) if total_players else 0.0

result = {
    "left_foot_percentage_1987_1992": pd.DataFrame(
        [{"percentage_left_foot": percentage_left}]
    )
}

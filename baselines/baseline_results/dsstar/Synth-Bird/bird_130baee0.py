import pandas as pd
import numpy as np

# Input tables (already loaded)
players = tables["table_1"].copy()
matches = tables["table_2"].copy()

# ----------------------------
# Parse datetimes
# ----------------------------
players["birthday_dt"] = pd.to_datetime(players["birthday"], errors="coerce")
matches["match_date_dt"] = pd.to_datetime(matches["date"], errors="coerce")

# ----------------------------
# Unpivot home players to long table
# ----------------------------
home_player_cols = [f"home_player_{i}" for i in range(1, 12)]
home_player_cols = [c for c in home_player_cols if c in matches.columns]

base_match_cols = ["id", "match_date_dt", "home_team_goal"]
base_match_cols = [c for c in base_match_cols if c in matches.columns]

home_long = (
    matches[base_match_cols + home_player_cols]
    .melt(
        id_vars=base_match_cols,
        value_vars=home_player_cols,
        var_name="home_player_slot",
        value_name="player_api_id",
    )
)

home_long["player_api_id"] = pd.to_numeric(home_long["player_api_id"], errors="coerce")
home_long = home_long.dropna(subset=["player_api_id", "match_date_dt"])
home_long["player_api_id"] = home_long["player_api_id"].astype("int64")

# ----------------------------
# Join to players and compute age at match date
# ----------------------------
home_long = home_long.merge(
    players[["player_api_id", "birthday_dt"]],
    on="player_api_id",
    how="left",
)

home_long["age_years"] = (home_long["match_date_dt"] - home_long["birthday_dt"]).dt.days / 365.25

# ----------------------------
# Filter to age <= 30, deduplicate by match_id, then SUM(home_team_goal)
# ----------------------------
home_long_u30 = home_long.loc[home_long["age_years"].notna() & (home_long["age_years"] <= 30)].copy()
matches_with_u30 = home_long_u30[["id", "home_team_goal"]].drop_duplicates(subset=["id"])

home_team_goal_sum_u30_matches = matches_with_u30["home_team_goal"].sum()

answer_df = pd.DataFrame({"home_team_goal_sum": [home_team_goal_sum_u30_matches]})

# Final result in required format
result = {"home_team_goal_sum_u30": answer_df}
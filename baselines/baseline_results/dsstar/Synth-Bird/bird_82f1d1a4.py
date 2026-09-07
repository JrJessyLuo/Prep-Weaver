import pandas as pd

# Tables are already loaded in the environment as `tables`
match_df = tables["table_2"]
league_map = tables["table_1"]

# ----------------------------
# 1) Validate required columns in Match
# ----------------------------
required_cols = ["league_id", "season", "home_team_goal", "away_team_goal"]
missing = [c for c in required_cols if c not in match_df.columns]
if missing:
    raise KeyError(
        f"Match table missing expected columns: {missing}\n"
        f"Match columns (sample): {list(match_df.columns)[:80]}"
    )

# ----------------------------
# 2) Filter matches for 2015/2016 (or season string containing '2016')
# ----------------------------
match_df = match_df.copy()
match_df["_season_str"] = match_df["season"].astype(str)

if (match_df["_season_str"] == "2015/2016").any():
    match_2016 = match_df.loc[match_df["_season_str"] == "2015/2016"].copy()
else:
    match_2016 = match_df.loc[match_df["_season_str"].str.contains("2016", na=False)].copy()

if match_2016.empty:
    raise ValueError(
        "No matches found for season '2015/2016' or where season contains '2016'. "
        f"Available seasons sample: {sorted(match_df['_season_str'].unique())[:50]}"
    )

# Draw indicator
match_2016["is_draw"] = match_2016["home_team_goal"] == match_2016["away_team_goal"]

# ----------------------------
# 3) Compute draw counts per league_id
# ----------------------------
draw_counts = (
    match_2016.groupby("league_id", dropna=False)["is_draw"]
    .sum()
    .astype(int)
    .reset_index(name="draw_count")
)

# ----------------------------
# 4) Join with league/country mapping to get league name
# ----------------------------
expected_map_cols = {"id", "country_id_name"}
if not expected_map_cols.issubset(league_map.columns):
    raise KeyError(
        f"League mapping file missing expected columns {expected_map_cols}. "
        f"Found columns: {list(league_map.columns)}"
    )

merged = draw_counts.merge(
    league_map.rename(columns={"id": "league_id"}),
    on="league_id",
    how="left",
)

# ----------------------------
# 5) Select the league with the max draw_count
# ----------------------------
result_sorted = merged.sort_values(["draw_count", "league_id"], ascending=[False, True]).reset_index(drop=True)
answer_df = result_sorted.head(1)

# Final answer per guidelines
result = {"league_with_most_draws_2016": answer_df}
import pandas as pd

# --- Tables ---
league_df = tables["table_1"].copy()
match_kv = tables["table_2"].copy()

# --- Reconstruct match table from key-value / transposed format ---
# table_2: rows are attributes (in 'id'), columns are match ids -> transpose to get one row per match
matches = match_kv.set_index("id").T.reset_index().rename(columns={"index": "match_id"})

# normalize column names for robust access
colmap = {c: str(c).strip().lower() for c in matches.columns}
matches = matches.rename(columns=colmap)

# required fields (goals might be named slightly differently)
season_col = "season"
league_id_col = "league_id"
home_goal_col = "home_team_goal" if "home_team_goal" in matches.columns else "home_goal"
away_goal_col = "away_team_goal" if "away_team_goal" in matches.columns else "away_goal"

# type cleanup
matches[league_id_col] = pd.to_numeric(matches[league_id_col], errors="coerce")
matches[home_goal_col] = pd.to_numeric(matches[home_goal_col], errors="coerce")
matches[away_goal_col] = pd.to_numeric(matches[away_goal_col], errors="coerce")

# --- Filter to 2016 season (typically encoded as '2015/2016') and draws ---
m2016 = matches[matches[season_col].astype(str).eq("2015/2016")].copy()
draws = m2016[m2016[home_goal_col].eq(m2016[away_goal_col])].copy()

# --- League with most draws ---
draw_counts = (
    draws.groupby(league_id_col, dropna=True)
    .size()
    .reset_index(name="draw_matches")
    .sort_values(["draw_matches", league_id_col], ascending=[False, True])
)

top_league_id = draw_counts.iloc[0][league_id_col] if not draw_counts.empty else None

# --- Map league_id to league name from table_1 ---
league_df["league_id"] = pd.to_numeric(league_df["id"], errors="coerce")
league_df["league_name"] = league_df["country_id_name"].astype(str).str.split("-", n=1).str[-1].str.strip()

out = league_df.loc[league_df["league_id"].eq(top_league_id), ["league_name"]].head(1).reset_index(drop=True)

result = {"league_with_most_draws_2016": out}

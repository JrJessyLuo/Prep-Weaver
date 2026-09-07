import pandas as pd

# --- players of interest -> player_api_id ---
players = ["Daan Smith", "Filipe Ferreira"]
p = tables["table_1"].loc[tables["table_1"]["xm"].isin(players), ["xm", "player_api_id"]].drop_duplicates()

# --- reshape match table (table_2 is transposed: rows are field names, columns are match ids) ---
m = tables["table_2"].set_index("id").T.reset_index().rename(columns={"index": "match_id"})
m.columns = m.columns.astype(str)

# identify relevant columns
away_goal_col = "away_team_goal"
away_player_cols = [c for c in m.columns if c.startswith("away_player_")]

# coerce numeric where needed
if away_goal_col in m.columns:
    m[away_goal_col] = pd.to_numeric(m[away_goal_col], errors="coerce").fillna(0)

for c in away_player_cols:
    m[c] = pd.to_numeric(m[c], errors="coerce")

# --- sum away team goals in matches where each player appears in away lineup, then add both sums ---
total = 0.0
if away_goal_col in m.columns and away_player_cols:
    for pid in p["player_api_id"].unique():
        total += m.loc[m[away_player_cols].eq(pid).any(axis=1), away_goal_col].sum()

result = {
    "away_goals_sum": pd.DataFrame({"sum_away_team_goals": [total]})
}

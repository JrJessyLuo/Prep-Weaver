import pandas as pd

# Tables are preloaded in the `tables` dict per instructions:
# table_1 -> teams, table_2 -> matches
teams = tables["table_1"]
matches = tables["table_2"]

# Compute total away goals per away team and find the max (same logic as reference)
away_goals_by_team = (
    matches.groupby("away_team_api_id", as_index=False)["away_team_goal"]
    .sum()
    .rename(columns={"away_team_goal": "total_away_goals"})
)

top_team_row = away_goals_by_team.loc[away_goals_by_team["total_away_goals"].idxmax()]
top_team_api_id = int(top_team_row["away_team_api_id"])

# Look up the full team name (team_long_name)
answer_df = teams.loc[teams["team_api_id"] == top_team_api_id, ["team_long_name"]].rename(
    columns={"team_long_name": "away_team_full_name"}
)

result = {"away_team_with_most_away_goals_full_name": answer_df}
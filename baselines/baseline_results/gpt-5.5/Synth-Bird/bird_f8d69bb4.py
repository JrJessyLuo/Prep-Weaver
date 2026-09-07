import pandas as pd

teams = tables["table_1"]
matches = tables["table_2"]

away_goals = (
    matches.groupby("away_team_api_id", as_index=False)["away_team_goal"]
    .sum()
    .rename(columns={"away_team_api_id": "team_api_id", "away_team_goal": "total_away_goals"})
)

max_goals = away_goals["total_away_goals"].max()

top_away_teams = away_goals.loc[away_goals["total_away_goals"].eq(max_goals), ["team_api_id"]]

out = (
    top_away_teams.merge(teams[["team_api_id", "team_long_name"]], on="team_api_id", how="left")
    .rename(columns={"team_long_name": "away_team_full_name"})
    [["away_team_full_name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"away_team_most_goals": out}

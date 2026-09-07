import pandas as pd

# Tables are preloaded in `tables`
match = tables["table_2"]          # european_football_2_Match.pkl (per reference code)
team = tables["table_1"]           # european_football_2_Team.pkl (from bird input)

# Ensure types match expected logic
match = match.copy()
match["season"] = match["season"].astype(str)
match["home_team_goal"] = pd.to_numeric(match["home_team_goal"], errors="coerce")
match["away_team_goal"] = pd.to_numeric(match["away_team_goal"], errors="coerce")

# Filter to 2016 season (dataset uses season strings like "2015/2016")
m2016 = match[match["season"].str.contains("2016", na=False)].copy()

# Home loss = away goals > home goals
home_losses = (
    m2016.assign(is_home_loss=m2016["away_team_goal"] > m2016["home_team_goal"])
        .groupby("home_team_api_id", as_index=False)["is_home_loss"]
        .sum()
        .rename(columns={"is_home_loss": "home_losses"})
)

# Pick team(s) with fewest home losses
min_losses = home_losses["home_losses"].min()
fewest = home_losses[home_losses["home_losses"] == min_losses].copy()

# Attach team name
fewest = fewest.merge(
    team[["team_api_id", "team_long_name"]],
    left_on="home_team_api_id",
    right_on="team_api_id",
    how="left",
)

answer = (
    fewest[["team_long_name", "home_team_api_id", "home_losses"]]
    .sort_values(["home_losses", "team_long_name", "home_team_api_id"], ascending=[True, True, True])
    .reset_index(drop=True)
)

result = {"fewest_home_losses_2016": answer}
import pandas as pd

country = tables["table_1"]
matches = tables["table_2"]

poland_row = country.loc[country["name"].eq("Poland")].head(1)
poland_country_id = int(poland_row["prefix"].iloc[0] + poland_row["suffix"].iloc[0])

m = matches.loc[
    matches["season"].eq("2010/2011") & matches["country_id"].eq(poland_country_id),
    ["game_score"],
].copy()

# Parse home goals from "H-A"
m["home_goals"] = (
    m["game_score"]
    .astype(str)
    .str.extract(r"^\s*(\d+)\s*-\s*(\d+)\s*$")[0]
    .astype(float)
)

avg_home_goals = m["home_goals"].mean()

result = {
    "average_home_team_goal_poland_2010_2011": pd.DataFrame(
        {"average_home_team_goal": [avg_home_goals]}
    )
}

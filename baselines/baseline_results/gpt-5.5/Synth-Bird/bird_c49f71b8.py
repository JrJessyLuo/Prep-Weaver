import pandas as pd

team = tables["table_1"]
team_attr = tables["table_2"]

team_id = team.loc[team["team_long_name"].eq("Heart of Midlothian"), "team_api_id"].iloc[0]

avg_speed = team_attr.loc[team_attr["team_api_id"].eq(team_id), "buildUpPlaySpeed"].mean()

result = {
    "average_build_up_play_speed": pd.DataFrame(
        {"team_long_name": ["Heart of Midlothian"], "average_build_up_play_speed": [avg_speed]}
    )
}

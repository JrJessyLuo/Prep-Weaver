import pandas as pd

# Team table: get Heart of Midlothian team_api_id(s)
team_df = tables["table_1"]
heart_team_api_ids = (
    team_df.loc[team_df["team_long_name"].eq("Heart of Midlothian"), "team_api_id"]
    .unique()
    .tolist()
)

# Team_Attributes: compute mean buildUpPlaySpeed for that team (NaNs ignored by default)
team_attr_df = tables["table_2"]
heart_buildup_speed_mean = (
    team_attr_df.loc[team_attr_df["team_api_id"].isin(heart_team_api_ids), "buildUpPlaySpeed"]
    .mean(skipna=True)
)

# Final answer as a DataFrame and stored in result dict
answer_df = pd.DataFrame(
    {"average_buildUpPlaySpeed": [heart_buildup_speed_mean]}
)

result = {"heart_of_midlothian_avg_buildup_play_speed": answer_df}
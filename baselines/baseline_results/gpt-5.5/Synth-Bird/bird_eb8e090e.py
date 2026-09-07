import pandas as pd

df_teams = tables["table_1"]
df_attrs = tables["table_2"]

attrs = df_attrs.set_index("id")

# Extract team_api_id ("taid") and speed class ("bpsc") per team column, then reshape to long
team_speed = (
    attrs.loc[["taid", "bpsc"]]
    .T
    .reset_index(drop=True)
    .rename(columns={"taid": "team_api_id", "bpsc": "speed_class"})
)

team_speed["team_api_id"] = pd.to_numeric(team_speed["team_api_id"], errors="coerce")
team_speed["speed_class"] = team_speed["speed_class"].astype(str)

fast_team_ids = team_speed.loc[
    team_speed["speed_class"].str.strip().str.lower().eq("fast"),
    "team_api_id",
].dropna().astype("int64")

out = (
    df_teams[df_teams["team_api_id"].isin(fast_team_ids)][["team_long_name"]]
    .drop_duplicates()
    .sort_values("team_long_name")
    .reset_index(drop=True)
)

result = {"fast_speed_class_teams": out}

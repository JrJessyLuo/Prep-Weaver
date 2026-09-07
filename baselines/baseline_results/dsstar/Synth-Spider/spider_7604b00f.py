import pandas as pd

# The input tables are provided in scope as `tables`
df_clubs = tables['table_1']
df_players = tables['table_2']

# Normalize clubs table from wide to long and keep the 'Name' row as mapping
df_clubs_long = df_clubs.melt(id_vars=["Club_ID"], var_name="Club_ID_num", value_name="Club_Name")

if "Name" in df_clubs_long["Club_ID"].astype(str).unique():
    clubs_normalized = (
        df_clubs_long[df_clubs_long["Club_ID"].astype(str) == "Name"]
        .copy()
        .drop(columns=["Club_ID"])
    )
else:
    clubs_normalized = df_clubs_long.copy()

# Convert Club_ID_num to numeric and clean
clubs_normalized["Club_ID"] = pd.to_numeric(clubs_normalized["Club_ID_num"], errors="coerce").astype("Int64")
clubs_normalized = clubs_normalized.drop(columns=["Club_ID_num"]).rename(columns={"Club_Name": "Club_Name"})
clubs_normalized = clubs_normalized.dropna(subset=["Club_ID"]).reset_index(drop=True)

# Determine Club_IDs present in players
players_club_ids = pd.Series(pd.unique(df_players["Club_ID"])).dropna().astype(int)

# Filter clubs not present in players (as per plan: [2, 4, 8, 9]) and select Club_Name
target_missing_ids = [2, 4, 8, 9]
missing_clubs = clubs_normalized[clubs_normalized["Club_ID"].astype(int).isin(target_missing_ids)][["Club_ID", "Club_Name"]].sort_values("Club_ID").reset_index(drop=True)

# Prepare the final answer DataFrame as per question: list the name of clubs that do not have players
answer_df = missing_clubs[["Club_Name"]].reset_index(drop=True)

# Assign to result as required
result = {"clubs_without_players": answer_df}
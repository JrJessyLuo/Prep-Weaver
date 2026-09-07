import pandas as pd

# Load tables from the provided in-scope dict `tables`
player_attr = tables["table_1"].copy()
player_info = tables["table_2"].copy()

# Ensure join keys are aligned in type
player_attr["player_api_id"] = pd.to_numeric(player_attr["player_api_id"], errors="coerce")
player_info["player_api_id"] = pd.to_numeric(player_info["player_api_id"], errors="coerce")

# Convert weight to numeric
player_info["weight"] = pd.to_numeric(player_info["weight"], errors="coerce")

# Join on player_api_id
df = player_attr.merge(
    player_info[["player_api_id", "weight"]],
    on="player_api_id",
    how="inner",
)

# Filter to weight < 130
df_lt130 = df[df["weight"] < 130].copy()

# Ensure distinct player_api_id (in case multiple attribute rows per player)
df_unique_players = df_lt130.drop_duplicates(subset=["player_api_id"])

# Compute n_left among distinct players
n_left = (
    df_unique_players["preferred_foot"]
    .astype("string")
    .str.strip()
    .str.lower()
    .eq("left")
    .sum()
)

# Final answer DataFrame
answer_df = pd.DataFrame({"n_left": [int(n_left)]})

# Assign result per guidelines
result = {"players_under_130_left_preferred_foot_count": answer_df}
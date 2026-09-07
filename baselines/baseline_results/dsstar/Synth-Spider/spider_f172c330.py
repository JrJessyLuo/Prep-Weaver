import pandas as pd
import numpy as np

# Access pre-loaded tables
player_info = tables['table_1']
player_active = tables['table_2']

# Left merge on Player_ID
merged_players = player_info.merge(player_active, on="Player_ID", how="left")

# Create boolean indicator for “plays any game”
flag_cols = ["If_active_1", "If_active_2", "If_active_3", "If_active_4"]

plays_any = False
for c in flag_cols:
    plays_any = plays_any | (merged_players[c].astype(str) == 'T')

# Identify rows where all flags are NaN
all_nan_flags = merged_players[flag_cols].isna().all(axis=1)

# Filter rows where plays_any is False OR all flags are NaN
filter_mask = (~plays_any) | all_nan_flags

# Select full names
result_full_names = (merged_players.loc[filter_mask, 'First_part'].fillna('') + ' ' +
                     merged_players.loc[filter_mask, 'Last_part'].fillna('')).str.strip()

# Build final answer DataFrame
answer_df = pd.DataFrame({'Player_Name': result_full_names.tolist()})

# Assign to result dict as required
result = {"players_no_games": answer_df}
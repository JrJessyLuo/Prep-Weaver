import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'player_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_fifa_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'overall_rating', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['player_api_id', 'player_fifa_api_id', 'date', 'overall_rating']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['player_api_id'] = pd.to_numeric(tmp_0['player_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['player_fifa_api_id'] = pd.to_numeric(tmp_1['player_fifa_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date'] = pd.to_datetime(tmp_2['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['overall_rating'] = pd.to_numeric(tmp_3['overall_rating'], errors='coerce').astype(float)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['player_api_id', 'player_fifa_api_id', 'date', 'overall_rating']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()
# Find the maximum overall rating across all snapshots
max_rating = df['overall_rating'].max()
# Filter to rows with the max rating; if multiple dates/players tie, keep all
top = df[df['overall_rating'] == max_rating]
# As only this table is available and it does not contain birthdays, we cannot extract birthday directly.
# Return the identifiers and date of the snapshot with highest rating as the closest available evidence.
# If multiple, return them all sorted by date descending.
target = top.sort_values(by=['date'], ascending=False)[['player_api_id', 'player_fifa_api_id', 'date', 'overall_rating']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

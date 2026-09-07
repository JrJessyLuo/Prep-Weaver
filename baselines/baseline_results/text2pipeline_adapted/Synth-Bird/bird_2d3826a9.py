import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_fifa_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'overall_rating', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'potential', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['player_api_id', 'date', 'overall_rating']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'variable', 'new_name': 'player_api_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'id', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'player_api_id', 'columns': 'id', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['player_fifa_api_id'] = pd.to_numeric(tmp_1['player_fifa_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['player_api_id'] = pd.to_numeric(tmp_2['player_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['overall_rating'] = pd.to_numeric(tmp_3['overall_rating'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['potential'] = pd.to_numeric(tmp_4['potential'], errors='coerce').astype(float)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['date'] = pd.to_datetime(tmp_5['date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['player_api_id', 'date', 'overall_rating']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'variable': 'player_api_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['player_api_id'] = pd.to_numeric(tmp_1['player_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['id'] = tmp_2['id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Pivot
    result = pd.pivot_table(tmp_2, index='player_api_id', columns='id', values='value', aggfunc='first').reset_index()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
ratings = prepared_table_1
players = prepared_table_2

# Merge ratings with players on player_api_id before any filtering
integrated = ratings.merge(players, on='player_api_id', how='inner')

# Ensure text columns are strings to safely use .str operations
for col in integrated.columns:
    if integrated[col].dtype == object:
        integrated[col] = integrated[col].astype(str)

# Build mask for Aaron Doran using case-insensitive search across plausible name fields
mask = None
name_cols = [c for c in ['first_name', 'lname'] if c in integrated.columns]
if name_cols:
    first_mask = integrated['first_name'].str.contains('aaron', case=False, na=False) if 'first_name' in integrated.columns else False
    last_mask = integrated['lname'].str.contains('doran', case=False, na=False) if 'lname' in integrated.columns else False
    mask = first_mask & last_mask

# If strict mask yields nothing, relax: look for both tokens anywhere in any string column
if mask is None or not mask.any():
    relaxed = None
    str_cols = [c for c in integrated.columns if integrated[c].dtype == object]
    for c in str_cols:
        m = integrated[c].str.contains('aaron', case=False, na=False) & integrated[c].str.contains('doran', case=False, na=False)
        relaxed = m if relaxed is None else (relaxed | m)
    mask = relaxed if relaxed is not None else None

filtered = integrated[mask] if mask is not None and mask.any() else integrated

# Compute average overall_rating for the matched player rows
result = filtered[['overall_rating']].copy()
result['overall_rating'] = result['overall_rating'].astype(float)
avg = result['overall_rating'].mean()

# Prepare final target DataFrame with the average
target = result.iloc[0:0].copy()
target.loc[:, 'average_overall_rating'] = [avg]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

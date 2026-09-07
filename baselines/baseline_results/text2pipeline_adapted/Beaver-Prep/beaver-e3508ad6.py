import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_BUILT', 'date_format': '%m/%d/%Y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_OCCUPIED', 'date_format': '%m/%d/%Y'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'DATE_BUILT', 'target_columns': ['DATE_BUILT_YEAR', '___drop_db_tmp'], 'func': "def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s, errors='coerce')\n    except Exception:\n        dt = pd.NaT\n    yr = int(dt.year) if pd.notna(dt) else None\n    return [yr, None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['___drop_db_tmp']}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'DATE_OCCUPIED', 'target_columns': ['DATE_OCCUPIED_YEAR', '___drop_do_tmp'], 'func': "def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s, errors='coerce')\n    except Exception:\n        dt = pd.NaT\n    yr = int(dt.year) if pd.notna(dt) else None\n    return [yr, None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['___drop_do_tmp']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNERSHIP_TYPE', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_TYPE', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else None'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DATE_BUILT_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DATE_OCCUPIED_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_NUMBER', 'OWNERSHIP_TYPE', 'BUILDING_TYPE', 'DATE_BUILT_YEAR', 'DATE_OCCUPIED_YEAR']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['DATE_BUILT'] = pd.to_datetime(tmp_0['DATE_BUILT'], errors='coerce').dt.strftime('%m/%d/%Y')
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['DATE_OCCUPIED'] = pd.to_datetime(tmp_1['DATE_OCCUPIED'], errors='coerce').dt.strftime('%m/%d/%Y')
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s, errors='coerce')\n    except Exception:\n        dt = pd.NaT\n    yr = int(dt.year) if pd.notna(dt) else None\n    return [yr, None]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['DATE_BUILT'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['DATE_BUILT_YEAR'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['___drop_db_tmp'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['___drop_db_tmp'], errors='ignore').copy()
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s, errors='coerce')\n    except Exception:\n        dt = pd.NaT\n    yr = int(dt.year) if pd.notna(dt) else None\n    return [yr, None]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_4['DATE_OCCUPIED'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['DATE_OCCUPIED_YEAR'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['___drop_do_tmp'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: DropColumn
    tmp_5 = tmp_4.drop(columns=['___drop_do_tmp'], errors='ignore').copy()
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else None', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['OWNERSHIP_TYPE'] = tmp_6['OWNERSHIP_TYPE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else None', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_7['BUILDING_TYPE'] = tmp_7['BUILDING_TYPE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['DATE_BUILT_YEAR'] = pd.to_numeric(tmp_8['DATE_BUILT_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['DATE_OCCUPIED_YEAR'] = pd.to_numeric(tmp_9['DATE_OCCUPIED_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['BUILDING_NUMBER', 'OWNERSHIP_TYPE', 'BUILDING_TYPE', 'DATE_BUILT_YEAR', 'DATE_OCCUPIED_YEAR']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()
# Filter for owned buildings that are not subdivisions (case-insensitive handled by prior standardization)
mask_owned = df['OWNERSHIP_TYPE'] == 'OWNED'
mask_not_subdiv = df['BUILDING_TYPE'] != 'SUBDIVISION'
res = df[mask_owned & mask_not_subdiv].copy()
# Sort by construction start year then building number for the display logic
res = res.sort_values(by=['DATE_BUILT_YEAR', 'BUILDING_NUMBER'], kind='mergesort')
# Prepare display columns with UNKNOWN for missing years
def year_or_unknown(x):
    return 'UNKNOWN' if pd.isna(x) else str(int(x))
res['Construction Start Year'] = res['DATE_BUILT_YEAR'].apply(year_or_unknown)
res['Building Number'] = res['BUILDING_NUMBER']
res['Year of Initial Occupancy'] = res['DATE_OCCUPIED_YEAR'].apply(year_or_unknown)
# Suppress repeated construction start year if same as previous row
# We only compare rows within the sorted result
prev = res['Construction Start Year'].shift(1)
same_as_prev = (res['Construction Start Year'] == prev)
# But do not blank UNKNOWN if previous is UNKNOWN; rule says display only if differs from previous row
res.loc[same_as_prev, 'Construction Start Year'] = ''
# Final projection
final_cols = ['Construction Start Year', 'Building Number', 'Year of Initial Occupancy']
answer = res[final_cols].copy()
# Append totals row: (null, #building Buildings, null) where null rendered as None
count_buildings = len(res)
total_label = f"{count_buildings} Buildings"
summary = pd.DataFrame([[None, total_label, None]], columns=final_cols)
target = pd.concat([answer, summary], ignore_index=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

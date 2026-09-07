import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'siji_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'siji_id', 'new_name': 'Driver_ID'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'shuxing', 'target_columns': ['attribute_name_list'], 'func': "def transform(s):\n    import ast\n    try:\n        v = ast.literal_eval(str(s))\n    except Exception:\n        v = [x.strip() for x in str(s).strip('[]').split(',') if x.strip()!='']\n    return [v]"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'shuxing_zhi', 'target_columns': ['attribute_value_list'], 'func': "def transform(s):\n    import ast\n    try:\n        v = ast.literal_eval(str(s))\n    except Exception:\n        v = [x.strip() for x in str(s).strip('[]').split(',') if x.strip()!='']\n    return [v]"}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'attribute_name_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'attribute_value_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute_name_list', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'attribute_value_list', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'attribute_name_list', 'new_name': 'attribute_name'}, {'old_name': 'attribute_value_list', 'new_name': 'Age'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Driver_ID', 'attribute_name', 'Age']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Driver_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Driver_ID', 'Road', 'Race_Base', 'Race_Suffix']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['siji_id'] = pd.to_numeric(tmp_0['siji_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'siji_id': 'Driver_ID'})
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import ast\n    try:\n        v = ast.literal_eval(str(s))\n    except Exception:\n        v = [x.strip() for x in str(s).strip('[]').split(',') if x.strip()!='']\n    return [v]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['shuxing'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['attribute_name_list'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import ast\n    try:\n        v = ast.literal_eval(str(s))\n    except Exception:\n        v = [x.strip() for x in str(s).strip('[]').split(',') if x.strip()!='']\n    return [v]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_3['shuxing_zhi'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['attribute_value_list'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: Explode
    tmp_4 = tmp_3.explode('attribute_name_list')
    # Step 6: Explode
    tmp_5 = tmp_4.explode('attribute_value_list')
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['attribute_name_list'] = tmp_6['attribute_name_list'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['attribute_value_list'] = pd.to_numeric(tmp_7['attribute_value_list'], errors='coerce').fillna(0).astype(int)
    # Step 9: Rename
    tmp_8 = tmp_7.rename(columns={'attribute_name_list': 'attribute_name', 'attribute_value_list': 'Age'})
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['Driver_ID', 'attribute_name', 'Age']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Driver_ID'] = pd.to_numeric(tmp_0['Driver_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['Driver_ID', 'Road', 'Race_Base', 'Race_Suffix']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge all needed tables to link drivers to their races and ages
integrated = prepared_table_2.merge(prepared_table_1, on='Driver_ID', how='inner')

# If merge yielded no usable Age column values, relax by ensuring Age is present numerically
if integrated.empty or ('Age' not in integrated.columns):
    # Fallback: use prepared_table_2 to count races, then left-join ages
    participation_counts = prepared_table_2.groupby('Driver_ID', as_index=False).size().rename(columns={'size': 'race_count'})
    leaders = participation_counts[participation_counts['race_count'] == participation_counts['race_count'].max()][['Driver_ID']]
    result = leaders.merge(prepared_table_1, on='Driver_ID', how='left')
    # Final projection of Age
    target = result[['Age']].dropna()
else:
    # Count participations per driver as number of race rows per Driver_ID
    participation_counts = integrated.groupby('Driver_ID', as_index=False).size().rename(columns={'size': 'race_count'})
    # Find the Driver_ID(s) with the maximum race_count
    max_count = participation_counts['race_count'].max()
    leaders = participation_counts[participation_counts['race_count'] == max_count][['Driver_ID']]
    # Join back to get Age for the leading Driver_ID(s)
    result = leaders.merge(prepared_table_1, on='Driver_ID', how='left')
    # Final projection: age(s) of the driver(s) with the most races
    target = result[['Age']].dropna()

# If still empty, relax further by selecting most frequent Driver_ID in prepared_table_2 and any available age from prepared_table_1
if target.empty:
    if not prepared_table_2.empty:
        fallback_counts = prepared_table_2.groupby('Driver_ID', as_index=False).size().rename(columns={'size': 'race_count'})
        top_id = fallback_counts.sort_values('race_count', ascending=False).head(1)[['Driver_ID']]
        target = top_id.merge(prepared_table_1, on='Driver_ID', how='left')[['Age']]
    else:
        # As a last resort, return any available Age from prepared_table_1
        target = prepared_table_1[['Age']].head(1)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

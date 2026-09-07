import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Stack', 'params': {'id_vars': ['district_id'], 'value_vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], 'var_name': 'col_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'col_id', 'columns': 'district_id', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'A2', 'new_name': 'district_name'}, {'old_name': 'A3', 'new_name': 'region_name'}, {'old_name': 'A4', 'new_name': 'crimes_1995'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'crimes_1995', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'col_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'col_id', 'new_name': 'district_key'}, {'old_name': 'district_name', 'new_name': 'district'}, {'old_name': 'region_name', 'new_name': 'region'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['district_key', 'district', 'region', 'crimes_1995']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'fdm', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'fdm', 'target_columns': ['open_year'], 'func': "def transform(s):\n    import pandas as pd\n    if isinstance(s, pd.Timestamp):\n        return [s.year]\n    try:\n        dt = pd.to_datetime(s, errors='coerce')\n        return [int(dt.year) if pd.notnull(dt) else None]\n    except Exception:\n        return [None]"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'open_year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['district_id', 'account_id', 'fdm', 'open_year']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['district_id'], value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], var_name='col_id', value_name='value')
    # Step 2: Pivot
    tmp_1 = pd.pivot_table(tmp_0, index='col_id', columns='district_id', values='value', aggfunc='first').reset_index()
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'A2': 'district_name', 'A3': 'region_name', 'A4': 'crimes_1995'})
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['crimes_1995'] = pd.to_numeric(tmp_3['crimes_1995'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['col_id'] = pd.to_numeric(tmp_4['col_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'col_id': 'district_key', 'district_name': 'district', 'region_name': 'region'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['district_key', 'district', 'region', 'crimes_1995']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['district_id'] = pd.to_numeric(tmp_0['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['fdm'] = pd.to_datetime(tmp_1['fdm'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import pandas as pd\n    if isinstance(s, pd.Timestamp):\n        return [s.year]\n    try:\n        dt = pd.to_datetime(s, errors='coerce')\n        return [int(dt.year) if pd.notnull(dt) else None]\n    except Exception:\n        return [None]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['fdm'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['open_year'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['open_year'] = pd.to_numeric(tmp_3['open_year'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['district_id', 'account_id', 'fdm', 'open_year']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, left_on='district_id', right_on='district_key', how='inner')
# Keep regions (districts) that have at least one account opened starting from 1997
mask_accounts_1997_plus = integrated['open_year'] >= 1997
regions_with_1997_accounts = integrated.loc[mask_accounts_1997_plus, ['district_key']].drop_duplicates()
# Filter integrated to districts meeting the accounts condition
integrated_filtered = integrated.merge(regions_with_1997_accounts, on='district_key', how='inner', suffixes=('', '_dup'))
# Now filter for crimes in 1995 exceeding 4000
integrated_filtered = integrated_filtered[integrated_filtered['crimes_1995'] > 4000]
# Compute average crimes_1995 across qualifying districts (unique by district_key)
by_district = integrated_filtered[['district_key', 'crimes_1995']].drop_duplicates()
avg_value = by_district['crimes_1995'].mean()
target = by_district.assign(avg_crimes_1995=avg_value)[['avg_crimes_1995']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

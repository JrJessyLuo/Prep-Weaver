import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'conference_staff', 'target_columns': ['conference_id_raw', 'staff_id_raw'], 'func': "def transform(s):\n    parts = str(s).split('-') if s is not None else []\n    if len(parts) < 2:\n        return [None, None]\n    return [parts[0].strip(), parts[1].strip()]"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'conference_id_raw', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'staff_id_raw', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'conference_id_raw', 'new_name': 'conference_id'}, {'old_name': 'staff_id_raw', 'new_name': 'staff_id'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'role', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['conference_id', 'staff_id', 'role']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['staff_ID'], 'value_vars': [1, 2, 3, 4, 5, 6, 7], 'var_name': 'staff_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'staff_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'staff_id', 'columns': 'staff_ID', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Age', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'Nationality', 'target_columns': ['Nationality', 'Nationality_norm'], 'func': 'def transform(s):\n    val = "" if s is None else str(s)\n    return [val, val.strip().lower()]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['staff_id', 'name', 'Age', 'Nationality', 'Nationality_norm']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['Institution_ID', 'Institution_Name', 'Location', 'Founded']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('-') if s is not None else []\n    if len(parts) < 2:\n        return [None, None]\n    return [parts[0].strip(), parts[1].strip()]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['conference_staff'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['conference_id_raw'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['staff_id_raw'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['conference_id_raw'] = pd.to_numeric(tmp_1['conference_id_raw'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['staff_id_raw'] = pd.to_numeric(tmp_2['staff_id_raw'], errors='coerce').fillna(0).astype(int)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'conference_id_raw': 'conference_id', 'staff_id_raw': 'staff_id'})
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['role'] = tmp_4['role'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['conference_id', 'staff_id', 'role']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['staff_ID'], value_vars=[1, 2, 3, 4, 5, 6, 7], var_name='staff_id', value_name='value')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['staff_id'] = pd.to_numeric(tmp_1['staff_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: Pivot
    tmp_2 = pd.pivot_table(tmp_1, index='staff_id', columns='staff_ID', values='value', aggfunc='first').reset_index()
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Age'] = pd.to_numeric(tmp_3['Age'], errors='coerce').fillna(0).astype(int)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    val = "" if s is None else str(s)\n    return [val, val.strip().lower()]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_4['Nationality'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['Nationality'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['Nationality_norm'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['staff_id', 'name', 'Age', 'Nationality', 'Nationality_norm']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['Institution_ID', 'Institution_Name', 'Location', 'Founded']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='staff_id')
# Filter for Canadian staff using normalized nationality
mask_canada = integrated['Nationality_norm'].str.contains('canada', case=False, na=False)
canada_attendance = integrated[mask_canada]
# Derive conference names: no separate names available, so use conference_id as the conference identifier
result = canada_attendance[['conference_id']].drop_duplicates().sort_values('conference_id')
# Present as names: cast to string for naming consistency
result['conference_name'] = 'Conference ' + result['conference_id'].astype(str)
target = result[['conference_name']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

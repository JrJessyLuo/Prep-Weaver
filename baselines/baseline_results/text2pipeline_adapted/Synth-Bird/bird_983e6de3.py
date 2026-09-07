import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'WBC', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'WBC']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ID', 'new_name': 'ID'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"4526214"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"1747469"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"5174645"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"5358902"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"5437753"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"4922344"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"5184284"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': '"720029"', 'func': 'def transform(s):\n    return str(s).strip().strip(\'"\')'}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['ID'], 'value_vars': ['"4526214"', '"1747469"', '"5174645"', '"5358902"', '"5437753"', '"4922344"', '"5184284"', '"720029"'], 'var_name': 'patient_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ID', 'new_name': 'attribute'}]}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'patient_id', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'patient_id', 'new_name': 'ID'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Birthday', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Description', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'SEX', 'Birthday', 'Description']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = tmp_0['ID'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['WBC'] = pd.to_numeric(tmp_1['WBC'], errors='coerce').astype(float)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Date'] = pd.to_datetime(tmp_2['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ID', 'Date', 'WBC']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'ID': 'ID'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['"4526214"'] = tmp_1['"4526214"'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['"1747469"'] = tmp_2['"1747469"'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['"5174645"'] = tmp_3['"5174645"'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['"5358902"'] = tmp_4['"5358902"'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['"5437753"'] = tmp_5['"5437753"'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_6['"4922344"'] = tmp_6['"4922344"'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_7['"5184284"'] = tmp_7['"5184284"'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip().strip(\'"\')', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_8['"720029"'] = tmp_8['"720029"'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 10: Stack
    tmp_9 = tmp_8.melt(id_vars=['ID'], value_vars=['"4526214"', '"1747469"', '"5174645"', '"5358902"', '"5437753"', '"4922344"', '"5184284"', '"720029"'], var_name='patient_id', value_name='value')
    # Step 11: Rename
    tmp_10 = tmp_9.rename(columns={'ID': 'attribute'})
    # Step 12: Pivot
    tmp_11 = pd.pivot_table(tmp_10, index='patient_id', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 13: Rename
    tmp_12 = tmp_11.rename(columns={'patient_id': 'ID'})
    # Step 14: CastType
    tmp_13 = tmp_12.copy()
    tmp_13['ID'] = tmp_13['ID'].astype(str)
    # Step 15: StandardizeDatetime
    tmp_14 = tmp_13.copy()
    tmp_14['Birthday'] = pd.to_datetime(tmp_14['Birthday'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 16: StandardizeDatetime
    tmp_15 = tmp_14.copy()
    tmp_15['Description'] = pd.to_datetime(tmp_15['Description'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 17: SelectCol
    result = tmp_15.loc[:, ['ID', 'SEX', 'Birthday', 'Description']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='ID', how='left')
# Define normal WBC range (10^3/µL) as commonly used in labs: 4.0 to 11.0 inclusive.
# Count unique patients accepted (present in lab table) whose WBC is within normal range.
normal_mask = integrated['WBC'].between(4.0, 11.0, inclusive='both')
result = integrated.loc[normal_mask, ['ID']].drop_duplicates()
count_df = result.agg({'ID': 'count'}).to_frame().T
count_df.columns = ['normal_wbc_patient_count']
target = count_df

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

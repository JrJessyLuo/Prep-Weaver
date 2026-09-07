import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'student_address_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 11, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 15, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 20, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 23, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 33, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 35, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 45, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 56, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 59, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 67, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 73, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 80, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 84, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 91, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 92, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['student_address_id'], 'value_vars': [11, 15, 20, 23, 33, 35, 45, 56, 59, 67, 73, 80, 84, 91, 92], 'var_name': 'col_key', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'student_address_id', 'new_name': 'field_name'}]}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'col_key', 'columns': 'field_name', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'address_id', 'new_name': 'student_address_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'student_address_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'student_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['student_address_id', 'student_id', 'address_type_code']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'address_type_code', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s.upper()\n"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'address_type_description', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s\n"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['address_type_code', 'address_type_description']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['student_address_id'] = tmp_0['student_address_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1[11] = tmp_1[11].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2[15] = tmp_2[15].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3[20] = tmp_3[20].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4[23] = tmp_4[23].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5[33] = tmp_5[33].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6[35] = tmp_6[35].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_7[45] = tmp_7[45].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_9 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_9)
    _std_func_9 = _ns_9.get('transform') or _ns_9.get('transform')
    tmp_8[56] = tmp_8[56].apply(lambda s: _std_func_9(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_10 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_10)
    _std_func_10 = _ns_10.get('transform') or _ns_10.get('transform')
    tmp_9[59] = tmp_9[59].apply(lambda s: _std_func_10(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_11 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_11)
    _std_func_11 = _ns_11.get('transform') or _ns_11.get('transform')
    tmp_10[67] = tmp_10[67].apply(lambda s: _std_func_11(s) if pd.notna(s) else s)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_12 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_12)
    _std_func_12 = _ns_12.get('transform') or _ns_12.get('transform')
    tmp_11[73] = tmp_11[73].apply(lambda s: _std_func_12(s) if pd.notna(s) else s)
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_13 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_13)
    _std_func_13 = _ns_13.get('transform') or _ns_13.get('transform')
    tmp_12[80] = tmp_12[80].apply(lambda s: _std_func_13(s) if pd.notna(s) else s)
    # Step 14: StandardizeString
    tmp_13 = tmp_12.copy()
    _ns_14 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_14)
    _std_func_14 = _ns_14.get('transform') or _ns_14.get('transform')
    tmp_13[84] = tmp_13[84].apply(lambda s: _std_func_14(s) if pd.notna(s) else s)
    # Step 15: StandardizeString
    tmp_14 = tmp_13.copy()
    _ns_15 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_15)
    _std_func_15 = _ns_15.get('transform') or _ns_15.get('transform')
    tmp_14[91] = tmp_14[91].apply(lambda s: _std_func_15(s) if pd.notna(s) else s)
    # Step 16: StandardizeString
    tmp_15 = tmp_14.copy()
    _ns_16 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_16)
    _std_func_16 = _ns_16.get('transform') or _ns_16.get('transform')
    tmp_15[92] = tmp_15[92].apply(lambda s: _std_func_16(s) if pd.notna(s) else s)
    # Step 17: Stack
    tmp_16 = tmp_15.melt(id_vars=['student_address_id'], value_vars=[11, 15, 20, 23, 33, 35, 45, 56, 59, 67, 73, 80, 84, 91, 92], var_name='col_key', value_name='value')
    # Step 18: Rename
    tmp_17 = tmp_16.rename(columns={'student_address_id': 'field_name'})
    # Step 19: Pivot
    tmp_18 = pd.pivot_table(tmp_17, index='col_key', columns='field_name', values='value', aggfunc='first').reset_index()
    # Step 20: Rename
    tmp_19 = tmp_18.rename(columns={'address_id': 'student_address_id'})
    # Step 21: CastType
    tmp_20 = tmp_19.copy()
    tmp_20['student_address_id'] = pd.to_numeric(tmp_20['student_address_id'], errors='coerce').fillna(0).astype(int)
    # Step 22: CastType
    tmp_21 = tmp_20.copy()
    tmp_21['student_id'] = pd.to_numeric(tmp_21['student_id'], errors='coerce').fillna(0).astype(int)
    # Step 23: SelectCol
    result = tmp_21.loc[:, ['student_address_id', 'student_id', 'address_type_code']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s.upper()\n", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['address_type_code'] = tmp_0['address_type_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s\n", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['address_type_description'] = tmp_1['address_type_description'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['address_type_code', 'address_type_description']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='address_type_code', how='inner')
counts = integrated.groupby(['address_type_code', 'address_type_description'], dropna=False).size().reset_index(name='cnt')
counts = counts.sort_values(['cnt', 'address_type_code'], ascending=[False, True])
target = counts.head(1)[['address_type_code', 'address_type_description']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

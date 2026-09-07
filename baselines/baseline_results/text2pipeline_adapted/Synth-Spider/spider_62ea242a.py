import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Rank', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Reputation_point', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Research_point', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Citation_point', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Total', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ID_Tens', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ID_Units', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['ID_Tens', 'ID_Units'], 'target_column': 'University_ID', 'func': "def transform(row):\n    return str(row['ID_Tens']) + str(row['ID_Units'])"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'University_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['University_ID', 'Research_point']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'University_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Uni_Name_Prefix', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Uni_Name_Suffix', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Uni_Name_Prefix', 'Uni_Name_Suffix'], 'target_column': 'University_Name', 'func': 'def transform(row):\n    prefix = str(row[\'Uni_Name_Prefix\']).strip()\n    suffix = str(row[\'Uni_Name_Suffix\']).strip()\n    if prefix and suffix:\n        return f"{prefix} {suffix}"\n    return prefix or suffix'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['University_ID', 'University_Name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Rank'] = pd.to_numeric(tmp_0['Rank'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Reputation_point'] = pd.to_numeric(tmp_1['Reputation_point'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Research_point'] = pd.to_numeric(tmp_2['Research_point'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Citation_point'] = pd.to_numeric(tmp_3['Citation_point'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Total'] = pd.to_numeric(tmp_4['Total'], errors='coerce').fillna(0).astype(int)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['ID_Tens'] = tmp_5['ID_Tens'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_6['ID_Units'] = tmp_6['ID_Units'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 8: Concatenate
    tmp_7 = tmp_6.copy()
    _ns_3 = {}
    exec("def transform(row):\n    return str(row['ID_Tens']) + str(row['ID_Units'])", globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_7['University_ID'] = tmp_7[['ID_Tens', 'ID_Units']].apply(_concat_func_3, axis=1)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['University_ID'] = pd.to_numeric(tmp_8['University_ID'], errors='coerce').fillna(0).astype(int)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['University_ID', 'Research_point']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['University_ID'] = pd.to_numeric(tmp_0['University_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Uni_Name_Prefix'] = tmp_1['Uni_Name_Prefix'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Uni_Name_Suffix'] = tmp_2['Uni_Name_Suffix'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Concatenate
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(row):\n    prefix = str(row[\'Uni_Name_Prefix\']).strip()\n    suffix = str(row[\'Uni_Name_Suffix\']).strip()\n    if prefix and suffix:\n        return f"{prefix} {suffix}"\n    return prefix or suffix', globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_3['University_Name'] = tmp_3[['Uni_Name_Prefix', 'Uni_Name_Suffix']].apply(_concat_func_3, axis=1)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['University_ID', 'University_Name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='University_ID', how='inner')
# Identify the maximum research points
max_rp = integrated['Research_point'].max() if len(integrated) > 0 else None
# Filter to universities with the maximum research points
if max_rp is not None:
    target = integrated[integrated['Research_point'] == max_rp][['University_Name', 'Research_point']].drop_duplicates()
else:
    # Fallback: preserve rows most plausibly connected (all joined rows), project name
    target = integrated[['University_Name', 'Research_point']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

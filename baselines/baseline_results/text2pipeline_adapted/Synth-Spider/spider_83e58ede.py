import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Player_ID', 'new_name': 'row_label'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['row_label'], 'value_vars': [1976, 1977, 1978, 1980, 1981, 1982, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1993, 1994, 1995, 1996, 1997, 2004, 2005, 2006], 'var_name': 'Player_ID', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'row_label', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'Player_ID', 'columns': 'row_label', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Player_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Player_name', 'func': "def transform(s):\n    s = str(s).strip()\n    for suf in [' *', ' †']:\n        if s.endswith(suf):\n            s = s[:-len(suf)].rstrip()\n    return s"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Rank_of_the_year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Player_ID', 'Player_name', 'Rank_of_the_year']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'Player_ID', 'func': 'def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Player_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Game_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'If_active', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Player_ID', 'Game_ID', 'If_active']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Game_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Title', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Release_Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'Platform_Units_Combined', 'target_columns': ['Platform_ID', 'Units_Millions'], 'func': "def transform(s):\n    parts = str(s).split('|', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Platform_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Units_Millions', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Game_ID', 'Title']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Player_ID': 'row_label'})
    # Step 2: Stack
    tmp_1 = tmp_0.melt(id_vars=['row_label'], value_vars=[1976, 1977, 1978, 1980, 1981, 1982, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1993, 1994, 1995, 1996, 1997, 2004, 2005, 2006], var_name='Player_ID', value_name='value')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['row_label'] = tmp_2['row_label'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Pivot
    tmp_3 = pd.pivot_table(tmp_2, index='Player_ID', columns='row_label', values='value', aggfunc='first').reset_index()
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Player_ID'] = tmp_4['Player_ID'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = str(s).strip()\n    for suf in [' *', ' †']:\n        if s.endswith(suf):\n            s = s[:-len(suf)].rstrip()\n    return s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['Player_name'] = tmp_5['Player_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['Rank_of_the_year'] = pd.to_numeric(tmp_6['Rank_of_the_year'], errors='coerce').fillna(0).astype(int)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['Player_ID', 'Player_name', 'Rank_of_the_year']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['Player_ID'] = tmp_0['Player_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Player_ID'] = tmp_1['Player_ID'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Game_ID'] = pd.to_numeric(tmp_2['Game_ID'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['If_active'] = tmp_3['If_active'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Player_ID', 'Game_ID', 'If_active']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Game_ID'] = pd.to_numeric(tmp_0['Game_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Title'] = tmp_1['Title'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Release_Date'] = pd.to_datetime(tmp_2['Release_Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec("def transform(s):\n    parts = str(s).split('|', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_3['Platform_Units_Combined'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['Platform_ID'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['Units_Millions'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Platform_ID'] = pd.to_numeric(tmp_4['Platform_ID'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Units_Millions'] = pd.to_numeric(tmp_5['Units_Millions'], errors='coerce').astype(float)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['Game_ID', 'Title']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_3, on='Game_ID', how='inner').merge(prepared_table_1, on='Player_ID', how='inner')
filtered = integrated[integrated['Title'] == 'Super Mario World']
target = filtered[['Player_name', 'Rank_of_the_year']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

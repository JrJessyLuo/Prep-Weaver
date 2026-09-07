import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NON_ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'BUILDING_KEY', 'new_name': 'BUILDING_KEY'}, {'old_name': 'FLOOR', 'new_name': 'FLOOR'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FAC_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME_LONG', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_OF_ROOMS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FAC_BUILDING_KEY', 'new_name': 'BUILDING_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'NUM_OF_ROOMS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'AREA']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ASSIGNABLE_AREA'] = pd.to_numeric(tmp_0['ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['NON_ASSIGNABLE_AREA'] = pd.to_numeric(tmp_1['NON_ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['EXT_GROSS_AREA'] = pd.to_numeric(tmp_2['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['BUILDING_KEY'] = tmp_3['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['FLOOR_KEY'] = tmp_4['FLOOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'BUILDING_KEY': 'BUILDING_KEY', 'FLOOR': 'FLOOR'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FAC_BUILDING_KEY'] = tmp_0['FAC_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['BUILDING_NAME'] = tmp_2['BUILDING_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['BUILDING_NAME_LONG'] = tmp_3['BUILDING_NAME_LONG'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['NUM_OF_ROOMS'] = pd.to_numeric(tmp_4['NUM_OF_ROOMS'], errors='coerce').fillna(0).astype(int)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'FAC_BUILDING_KEY': 'BUILDING_KEY'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'NUM_OF_ROOMS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'AREA']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
agg = prepared_table_1.groupby('BUILDING_KEY', as_index=False).agg({'ASSIGNABLE_AREA':'sum','NON_ASSIGNABLE_AREA':'sum'})
integrated = agg.merge(prepared_table_2, on='BUILDING_KEY', how='left')
# Choose a human-readable building name: prefer BUILDING_NAME, fallback to BUILDING_NAME_LONG, else use BUILDING_NUMBER
name_col = integrated['BUILDING_NAME'].where(integrated['BUILDING_NAME'].notna() & (integrated['BUILDING_NAME'].astype(str).str.strip()!=''), integrated['BUILDING_NAME_LONG'])
name_col = name_col.where(name_col.notna() & (name_col.astype(str).str.strip()!=''), integrated['BUILDING_NUMBER'])
integrated['BUILDING_NAME_DISPLAY'] = name_col
result = integrated[['BUILDING_NAME_DISPLAY','BUILDING_NUMBER','ASSIGNABLE_AREA','NON_ASSIGNABLE_AREA','NUM_OF_ROOMS']].copy()
result = result.rename(columns={'BUILDING_NAME_DISPLAY':'BUILDING_NAME','ASSIGNABLE_AREA':'TOTAL_ASSIGNABLE_AREA','NON_ASSIGNABLE_AREA':'TOTAL_NON_ASSIGNABLE_AREA','NUM_OF_ROOMS':'TOTAL_ROOM_COUNT'})
result = result.sort_values(by='TOTAL_ASSIGNABLE_AREA', ascending=False)
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

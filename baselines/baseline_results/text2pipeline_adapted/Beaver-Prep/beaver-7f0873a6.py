import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FLOOR', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FLOOR_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ROOM', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SPACE_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ORGANIZATION_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ROOM_FULL_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'WAREHOUSE_LOAD_DATE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACCESS_LEVEL', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'AREA', 'ACCESS_LEVEL', 'ORGANIZATION_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FLOOR', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FLOOR_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_WINGS_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'WAREHOUSE_LOAD_DATE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NON_ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FLOOR_SORT_SEQUENCE', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACCESS_LEVEL', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'LEVEL_ID', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FLOOR_KEY', 'BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA', 'ACCESS_LEVEL']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'FAC_BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NAME_LONG', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'WAREHOUSE_LOAD_DATE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_OF_ROOMS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FAC_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FAC_BUILDING_KEY', 'new_name': 'BUILDING_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NAME', 'NUM_OF_ROOMS']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_STREET_ADDRESS', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'WAREHOUSE_LOAD_DATE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_STREET_ADDRESS', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'BUILDING_STREET_ADDRESS', 'target_columns': ['CITY', 'ZIP_CODE'], 'func': 'def transform(s):\n    import re\n    if s is None:\n        return [None, None]\n    txt = str(s).strip()\n    if not txt:\n        return [None, None]\n    # Normalize internal spaces\n    norm = re.sub(r"\\s+", " ", txt)\n    parts = norm.split(\' \')\n    # Heuristic: last token 5-digit ZIP\n    zip_code = None\n    if re.fullmatch(r"\\d{5}", parts[-1] if parts else \'\'):\n        zip_code = parts[-1]\n        parts = parts[:-1]\n    # City: tokens after the street number segment; try to detect street number at start\n    city = None\n    if parts:\n        # If starts with number, assume everything except the first token(s) that are street number is city is not present in this dataset; leave None\n        # But if there\'s a comma, use text after the last comma as city\n        if \',\' in norm:\n            after_comma = norm.split(\',\')[-1].strip()\n            # remove trailing ZIP if duplicated\n            toks = after_comma.split()\n            if toks and re.fullmatch(r"\\d{5}", toks[-1]):\n                toks = toks[:-1]\n            city = \' \'.join(toks).strip() or None\n        else:\n            # If there is no comma and address contains at least 3 tokens and ends with common suffix like \'MA\' or state code, avoid guessing city; set None\n            city = None\n    return [city, zip_code]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_STREET_ADDRESS', 'ZIP_CODE', 'CITY']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['FLOOR'] = tmp_1['FLOOR'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['FLOOR_KEY'] = tmp_2['FLOOR_KEY'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['ROOM'] = tmp_3['ROOM'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['SPACE_ID'] = tmp_4['SPACE_ID'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['ORGANIZATION_NAME'] = tmp_5['ORGANIZATION_NAME'].astype(str)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['ROOM_FULL_NAME'] = tmp_6['ROOM_FULL_NAME'].astype(str)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['WAREHOUSE_LOAD_DATE'] = tmp_7['WAREHOUSE_LOAD_DATE'].astype(str)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['AREA'] = pd.to_numeric(tmp_8['AREA'], errors='coerce').astype(float)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['ACCESS_LEVEL'] = pd.to_numeric(tmp_9['ACCESS_LEVEL'], errors='coerce').fillna(0).astype(int)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_10['BUILDING_KEY'] = tmp_10['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_11['FLOOR_KEY'] = tmp_11['FLOOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_12['FLOOR'] = tmp_12['FLOOR'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 14: SelectCol
    result = tmp_12.loc[:, ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'AREA', 'ACCESS_LEVEL', 'ORGANIZATION_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['FLOOR'] = tmp_1['FLOOR'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['FLOOR_KEY'] = tmp_2['FLOOR_KEY'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['BUILDING_WINGS_ID'] = tmp_3['BUILDING_WINGS_ID'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['WAREHOUSE_LOAD_DATE'] = tmp_4['WAREHOUSE_LOAD_DATE'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['EXT_GROSS_AREA'] = pd.to_numeric(tmp_5['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['ASSIGNABLE_AREA'] = pd.to_numeric(tmp_6['ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['NON_ASSIGNABLE_AREA'] = pd.to_numeric(tmp_7['NON_ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['FLOOR_SORT_SEQUENCE'] = pd.to_numeric(tmp_8['FLOOR_SORT_SEQUENCE'], errors='coerce').fillna(0).astype(int)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['ACCESS_LEVEL'] = pd.to_numeric(tmp_9['ACCESS_LEVEL'], errors='coerce').fillna(0).astype(int)
    # Step 11: CastType
    tmp_10 = tmp_9.copy()
    tmp_10['LEVEL_ID'] = pd.to_numeric(tmp_10['LEVEL_ID'], errors='coerce').astype(float)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_11['BUILDING_KEY'] = tmp_11['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_12['FLOOR_KEY'] = tmp_12['FLOOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 14: SelectCol
    result = tmp_12.loc[:, ['FLOOR_KEY', 'BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA', 'ACCESS_LEVEL']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FAC_BUILDING_KEY'] = tmp_0['FAC_BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['BUILDING_NAME'] = tmp_2['BUILDING_NAME'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['BUILDING_NAME_LONG'] = tmp_3['BUILDING_NAME_LONG'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['WAREHOUSE_LOAD_DATE'] = tmp_4['WAREHOUSE_LOAD_DATE'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['NUM_OF_ROOMS'] = pd.to_numeric(tmp_5['NUM_OF_ROOMS'], errors='coerce').fillna(0).astype(int)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_6['FAC_BUILDING_KEY'] = tmp_6['FAC_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_7['BUILDING_NUMBER'] = tmp_7['BUILDING_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 9: Rename
    tmp_8 = tmp_7.rename(columns={'FAC_BUILDING_KEY': 'BUILDING_KEY'})
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['BUILDING_KEY', 'BUILDING_NAME', 'NUM_OF_ROOMS']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['BUILDING_NAME'] = tmp_2['BUILDING_NAME'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['BUILDING_STREET_ADDRESS'] = tmp_3['BUILDING_STREET_ADDRESS'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['WAREHOUSE_LOAD_DATE'] = tmp_4['WAREHOUSE_LOAD_DATE'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['BUILDING_KEY'] = tmp_5['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_6['BUILDING_STREET_ADDRESS'] = tmp_6['BUILDING_STREET_ADDRESS'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 8: SplitColumn
    tmp_7 = tmp_6.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return [None, None]\n    txt = str(s).strip()\n    if not txt:\n        return [None, None]\n    # Normalize internal spaces\n    norm = re.sub(r"\\s+", " ", txt)\n    parts = norm.split(\' \')\n    # Heuristic: last token 5-digit ZIP\n    zip_code = None\n    if re.fullmatch(r"\\d{5}", parts[-1] if parts else \'\'):\n        zip_code = parts[-1]\n        parts = parts[:-1]\n    # City: tokens after the street number segment; try to detect street number at start\n    city = None\n    if parts:\n        # If starts with number, assume everything except the first token(s) that are street number is city is not present in this dataset; leave None\n        # But if there\'s a comma, use text after the last comma as city\n        if \',\' in norm:\n            after_comma = norm.split(\',\')[-1].strip()\n            # remove trailing ZIP if duplicated\n            toks = after_comma.split()\n            if toks and re.fullmatch(r"\\d{5}", toks[-1]):\n                toks = toks[:-1]\n            city = \' \'.join(toks).strip() or None\n        else:\n            # If there is no comma and address contains at least 3 tokens and ends with common suffix like \'MA\' or state code, avoid guessing city; set None\n            city = None\n    return [city, zip_code]', globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_7['BUILDING_STREET_ADDRESS'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_7['CITY'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_7['ZIP_CODE'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['BUILDING_KEY', 'BUILDING_STREET_ADDRESS', 'ZIP_CODE', 'CITY']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_10', pd.DataFrame()))

# Stage-2 program over the prepared tables.
rooms = prepared_table_1.copy()
# Relaxed filter for Department of Facilities using broader case-insensitive matching
org_col = 'ORGANIZATION_NAME'
rooms_dof = rooms[rooms[org_col].astype(str).str.upper().str.contains('FACIL|FACILIT|FACILITIES|DOF|DEPT OF FACIL', na=False)].copy()
# Merge in floor metadata for access level consistency
floors = prepared_table_2.copy()
rooms_f = rooms_dof.merge(floors[['FLOOR_KEY','ACCESS_LEVEL']].rename(columns={'ACCESS_LEVEL':'ACCESS_LEVEL_floor'}), on='FLOOR_KEY', how='left')
# Choose room access level when available, else floor access level
rooms_f['ACCESS_LEVEL_FINAL'] = rooms_f['ACCESS_LEVEL']
rooms_f.loc[rooms_f['ACCESS_LEVEL_FINAL'].isna(), 'ACCESS_LEVEL_FINAL'] = rooms_f['ACCESS_LEVEL_floor']
# Merge in building names
bldg_names = prepared_table_3.copy()
rooms_fb = rooms_f.merge(bldg_names[['BUILDING_KEY','BUILDING_NAME']], on='BUILDING_KEY', how='left')
# Merge in building address for ZIP and CITY
baddr = prepared_table_4.copy()
rooms_full = rooms_fb.merge(baddr[['BUILDING_KEY','ZIP_CODE','CITY']], on='BUILDING_KEY', how='left')
# Aggregate per building-floor
grp_cols = ['BUILDING_KEY','FLOOR_KEY']
agg = rooms_full.groupby(grp_cols, as_index=False).agg(
    num_rooms=('ROOM','nunique'),
    total_area=('AREA','sum'),
    ACCESS_LEVEL=('ACCESS_LEVEL_FINAL','max')
)
# Add descriptive fields from a representative row per group
first_fields = rooms_full.groupby(grp_cols, as_index=False).agg(
    BUILDING_NAME=('BUILDING_NAME','first'),
    ZIP_CODE=('ZIP_CODE','first'),
    CITY=('CITY','first'),
    FLOOR=('FLOOR','first')
)
agg = agg.merge(first_fields, on=grp_cols, how='left')
# Average area per floor at the building level (mean of floor totals)
bldg_floor_avg = agg.groupby('BUILDING_KEY', as_index=False).agg(avg_area_per_floor=('total_area','mean'))
agg = agg.merge(bldg_floor_avg, on='BUILDING_KEY', how='left')
# Detail rows
detail = agg.copy()
detail['level'] = 'detail'
# Subtotals per building (exclude ZIP and CITY from aggregation)
b_sub = agg.groupby('BUILDING_KEY', as_index=False).agg(
    num_rooms=('num_rooms','sum'),
    total_area=('total_area','sum'),
    ACCESS_LEVEL=('ACCESS_LEVEL','max'),
    BUILDING_NAME=('BUILDING_NAME','first'),
    avg_area_per_floor=('total_area','mean')
)
b_sub['FLOOR_KEY'] = ''
b_sub['FLOOR'] = ''
b_sub['ZIP_CODE'] = ''
b_sub['CITY'] = ''
b_sub['level'] = 'subtotal'
# Grand total across all buildings (exclude ZIP/CITY)
grand = pd.DataFrame({
    'BUILDING_KEY': ['ALL BUILDINGS'],
    'FLOOR_KEY': [''],
    'FLOOR': [''],
    'num_rooms': [b_sub['num_rooms'].sum()],
    'total_area': [b_sub['total_area'].sum()],
    'avg_area_per_floor': [b_sub['avg_area_per_floor'].mean()],
    'ACCESS_LEVEL': [b_sub['ACCESS_LEVEL'].max()],
    'BUILDING_NAME': ['ALL BUILDINGS'],
    'ZIP_CODE': [''],
    'CITY': [''],
    'level': ['grand total']
})
# Align columns
cols = ['BUILDING_KEY','FLOOR_KEY','FLOOR','num_rooms','total_area','avg_area_per_floor','BUILDING_NAME','ACCESS_LEVEL','ZIP_CODE','CITY','level']
detail = detail[cols]
b_sub = b_sub[cols]
grand = grand[cols]
# Concatenate all rows
out = pd.concat([detail, b_sub, grand], ignore_index=True, sort=False)
# Round and format numeric outputs with commas
for c in ['num_rooms','total_area','avg_area_per_floor']:
    out[c] = out[c].round(0)
    out[c] = out[c].apply(lambda v: f"{int(v):,}" if pd.notnull(v) else None)
# Rename to requested output names
out = out.rename(columns={
    'BUILDING_KEY':'building_key',
    'FLOOR_KEY':'floor_key',
    'FLOOR':'floor',
    'num_rooms':'number_of_rooms',
    'total_area':'total_area',
    'avg_area_per_floor':'average_area_per_floor',
    'BUILDING_NAME':'building_name',
    'ACCESS_LEVEL':'access_level',
    'ZIP_CODE':'zip_code',
    'CITY':'city'
})
# Final selection
target = out[['building_key','floor_key','floor','number_of_rooms','total_area','average_area_per_floor','building_name','access_level','zip_code','city','level']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

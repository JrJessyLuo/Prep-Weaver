import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SPACE_UNIT_KEY', 'target_columns': ['SPACE_UNIT_KEY', 'drop_helper_1'], 'func': "def transform(s):\n    try:\n        if s is None or (isinstance(s, float) and pd.isna(s)):\n            return [None, None]\n        txt = str(s).strip()\n        if txt.endswith('.0'):\n            txt = txt[:-2]\n        # If still float-like, cast via int\n        try:\n            v = int(float(txt))\n            return [str(v), None]\n        except Exception:\n            return [txt, None]\n    except Exception:\n        return [str(s), None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['drop_helper_1']}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SPACE_USAGE_KEY', 'target_columns': ['SPACE_USAGE_KEY', 'drop_helper_2'], 'func': "def transform(s):\n    try:\n        if s is None or (isinstance(s, float) and pd.isna(s)):\n            return [None, None]\n        txt = str(s).strip()\n        if txt.endswith('.0'):\n            txt = txt[:-2]\n        try:\n            v = int(float(txt))\n            return [str(v), None]\n        except Exception:\n            return [txt, None]\n    except Exception:\n        return [str(s), None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['drop_helper_2']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR_KEY', 'SPACE_UNIT_KEY', 'SPACE_USAGE_KEY', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_STREET_ADDRESS', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FLOOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FLOOR_KEY', 'FLOOR', 'FLOOR_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'space_usage_key', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'space_usage_key', 'new_name': 'SPACE_USAGE_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SPACE_USAGE_KEY', 'SPACE_USAGE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'SPACE_UNIT_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SPACE_UNIT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fclt_organization_key', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SPACE_UNIT_KEY', 'func': "def transform(s):\n    s = str(s)\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SPACE_UNIT_CODE', 'func': "def transform(s):\n    s = str(s)\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SPACE_UNIT_KEY', 'fclt_organization_key']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'SPACE_ID']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['FLOOR_KEY'] = tmp_1['FLOOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    try:\n        if s is None or (isinstance(s, float) and pd.isna(s)):\n            return [None, None]\n        txt = str(s).strip()\n        if txt.endswith('.0'):\n            txt = txt[:-2]\n        # If still float-like, cast via int\n        try:\n            v = int(float(txt))\n            return [str(v), None]\n        except Exception:\n            return [txt, None]\n    except Exception:\n        return [str(s), None]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_2['SPACE_UNIT_KEY'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['SPACE_UNIT_KEY'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['drop_helper_1'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['drop_helper_1'], errors='ignore').copy()
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(s):\n    try:\n        if s is None or (isinstance(s, float) and pd.isna(s)):\n            return [None, None]\n        txt = str(s).strip()\n        if txt.endswith('.0'):\n            txt = txt[:-2]\n        try:\n            v = int(float(txt))\n            return [str(v), None]\n        except Exception:\n            return [txt, None]\n    except Exception:\n        return [str(s), None]", globals(), _ns_4)
    _split_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('split')
    _split_values_4 = tmp_4['SPACE_USAGE_KEY'].apply(_split_func_4)
    _split_values_4 = _split_values_4.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['SPACE_USAGE_KEY'] = _split_values_4.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['drop_helper_2'] = _split_values_4.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: DropColumn
    tmp_5 = tmp_4.drop(columns=['drop_helper_2'], errors='ignore').copy()
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['BUILDING_KEY', 'FLOOR_KEY', 'SPACE_UNIT_KEY', 'SPACE_USAGE_KEY', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
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
    tmp_3['BUILDING_STREET_ADDRESS'] = tmp_3['BUILDING_STREET_ADDRESS'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FLOOR_KEY'] = tmp_0['FLOOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['FLOOR_KEY', 'FLOOR', 'FLOOR_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_9', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['space_usage_key'] = tmp_0['space_usage_key'].astype(str)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'space_usage_key': 'SPACE_USAGE_KEY'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['SPACE_USAGE_KEY', 'SPACE_USAGE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_10', pd.DataFrame()))

def _prepare_table_5(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['SPACE_UNIT_KEY'] = tmp_0['SPACE_UNIT_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SPACE_UNIT_CODE'] = tmp_1['SPACE_UNIT_CODE'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['fclt_organization_key'] = tmp_2['fclt_organization_key'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['SPACE_UNIT_KEY'] = tmp_3['SPACE_UNIT_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = str(s)\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['SPACE_UNIT_CODE'] = tmp_4['SPACE_UNIT_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['SPACE_UNIT_KEY', 'fclt_organization_key']].copy()
    return result

prepared_table_5 = _prepare_table_5(tables.get('table_6', pd.DataFrame()))

def _prepare_table_6(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['FLOOR'] = tmp_1['FLOOR'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'SPACE_ID']].copy()
    return result

prepared_table_6 = _prepare_table_6(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
b = prepared_table_2.copy()
# Identify building 36 by matching building number/name that contains '36' and plausible variants. Prefer exact '36' then building numbers ending with 36, otherwise any containing '36'.
cand = b[b['BUILDING_NUMBER'].str.strip().str.upper().eq('36')]
if cand.empty:
    cand = b[b['BUILDING_NUMBER'].str.strip().str.upper().str.endswith('36')]
if cand.empty:
    cand = b[b['BUILDING_NUMBER'].str.strip().str.upper().str.contains('36', na=False)]
# If still empty, fall back to rows where name contains '36'
if cand.empty:
    cand = b[b['BUILDING_NAME'].str.strip().str.upper().str.contains('36', na=False)]
# Use all candidate buildings (in case multiple codes like 'NW36')
b_keys = cand[['BUILDING_KEY']].drop_duplicates()
# Join space units to building and floor
su = prepared_table_1.merge(b_keys, on='BUILDING_KEY', how='inner')
# Join floor dimension for human-readable floor
su = su.merge(prepared_table_3, on='FLOOR_KEY', how='left')
# Join space usage description
su = su.merge(prepared_table_4, on='SPACE_USAGE_KEY', how='left')
# Count organizations per space unit
org_counts = prepared_table_5.groupby('SPACE_UNIT_KEY', as_index=False)['fclt_organization_key'].nunique().rename(columns={'fclt_organization_key':'num_organizations'})
su = su.merge(org_counts, on='SPACE_UNIT_KEY', how='left')
# Compute number of space units on the same building and floor (based on SPACE_UNIT_KEY distinct within BUILDING_KEY + FLOOR_KEY)
su['SPACE_UNIT_KEY_tmp'] = su['SPACE_UNIT_KEY']
floor_counts = su.groupby(['BUILDING_KEY','FLOOR_KEY'], as_index=False)['SPACE_UNIT_KEY_tmp'].nunique().rename(columns={'SPACE_UNIT_KEY_tmp':'num_space_units_same_floor'})
su = su.merge(floor_counts, on=['BUILDING_KEY','FLOOR_KEY'], how='left')
# Attach building name and street address
su = su.merge(cand[['BUILDING_KEY','BUILDING_NAME','BUILDING_STREET_ADDRESS']], on='BUILDING_KEY', how='left')
# Final projection and ordering
cols = ['SPACE_UNIT_KEY','ROOM_NUMBER','BUILDING_ROOM','FLOOR','BUILDING_NAME','BUILDING_STREET_ADDRESS','SPACE_USAGE','num_organizations','num_space_units_same_floor']
# Ensure columns exist
for c in cols:
    if c not in su.columns:
        su[c] = su.get(c)
# Sort by SPACE_UNIT_KEY then ROOM_NUMBER for readability
su_sorted = su[cols].drop_duplicates().sort_values(by=['SPACE_UNIT_KEY','ROOM_NUMBER'], kind='mergesort')
target = su_sorted

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

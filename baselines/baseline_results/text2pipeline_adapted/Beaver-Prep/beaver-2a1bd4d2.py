import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'PARENT_BUILDING_NUMBER', 'func': "def transform(s):\n    # keep original value semantics but standardize for emptiness checks\n    return '' if s is None or str(s).lower() == 'nan' else str(s).strip()"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'PARENT_BUILDING_NUMBER', 'target_columns': ['IS_SUBDIVISION'], 'func': "def transform(s):\n    val = '' if s is None else str(s).strip()\n    is_sub = bool(val)\n    return [is_sub]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'PARENT_BUILDING_NUMBER', 'BUILDING_TYPE', 'EXT_GROSS_AREA', 'IS_SUBDIVISION']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else ''"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'POSTAL_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL'], 'target_column': 'STREET_ADDRESS', 'func': 'def transform(row):\n    parts = []\n    for col in ["STREET_NUMBER","STREET_NUMBER_SUFFIX","PRE_DIRECTIONAL","STREET_NAME","STREET_SUFFIX","POST_DIRECTIONAL"]:\n        val = row.get(col)\n        if val is None:\n            continue\n        s = str(val).strip()\n        if s and s.lower() != \'nan\':\n            parts.append(s)\n    return \' \'.join(parts).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE', 'STREET_ADDRESS']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'FULL_NAME', 'EMPLOYEE_GROUP', 'EMPLOYEE_TYPE', 'OFFICE_LOCATION', 'HR_ORG_UNIT_ID']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFICE_LOCATION', 'func': "def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return None\n    try:\n        return str(s).strip().upper()\n    except Exception:\n        return None"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'OFFICE_LOCATION', 'target_columns': ['BUILDING_NUMBER', 'ROOM_SEGMENT'], 'func': "def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return [None, None]\n    txt = str(s)\n    if '-' in txt:\n        parts = txt.split('-', 1)\n        return [parts[0], parts[1] if parts[1] != '' else None]\n    else:\n        return [txt, None]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': "def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return None\n    return str(s).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'FULL_NAME', 'EMPLOYEE_GROUP', 'EMPLOYEE_TYPE', 'OFFICE_LOCATION', 'BUILDING_NUMBER', 'ROOM_SEGMENT']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['BUILDING_ROOM', 'BUILDING_COMPONENT', 'FLOOR', 'SPACE_USAGE', 'SPACE_UNIT_CODE', 'HR_ORG_UNIT_ID', 'ACCESS_LEVEL']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else ''", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    # keep original value semantics but standardize for emptiness checks\n    return '' if s is None or str(s).lower() == 'nan' else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['PARENT_BUILDING_NUMBER'] = tmp_2['PARENT_BUILDING_NUMBER'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['EXT_GROSS_AREA'] = pd.to_numeric(tmp_3['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(s):\n    val = '' if s is None else str(s).strip()\n    is_sub = bool(val)\n    return [is_sub]", globals(), _ns_4)
    _split_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('split')
    _split_values_4 = tmp_4['PARENT_BUILDING_NUMBER'].apply(_split_func_4)
    _split_values_4 = _split_values_4.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['IS_SUBDIVISION'] = _split_values_4.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'PARENT_BUILDING_NUMBER', 'BUILDING_TYPE', 'EXT_GROSS_AREA', 'IS_SUBDIVISION']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_6', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else ''", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['POSTAL_CODE'] = tmp_2['POSTAL_CODE'].astype(str)
    # Step 4: Concatenate
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(row):\n    parts = []\n    for col in ["STREET_NUMBER","STREET_NUMBER_SUFFIX","PRE_DIRECTIONAL","STREET_NAME","STREET_SUFFIX","POST_DIRECTIONAL"]:\n        val = row.get(col)\n        if val is None:\n            continue\n        s = str(val).strip()\n        if s and s.lower() != \'nan\':\n            parts.append(s)\n    return \' \'.join(parts).strip()', globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_3['STREET_ADDRESS'] = tmp_3[['STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL']].apply(_concat_func_3, axis=1)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE', 'STREET_ADDRESS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    tmp_0 = df.loc[:, ['MIT_ID', 'FULL_NAME', 'EMPLOYEE_GROUP', 'EMPLOYEE_TYPE', 'OFFICE_LOCATION', 'HR_ORG_UNIT_ID']].copy()
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return None\n    try:\n        return str(s).strip().upper()\n    except Exception:\n        return None", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['OFFICE_LOCATION'] = tmp_1['OFFICE_LOCATION'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return [None, None]\n    txt = str(s)\n    if '-' in txt:\n        parts = txt.split('-', 1)\n        return [parts[0], parts[1] if parts[1] != '' else None]\n    else:\n        return [txt, None]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_2['OFFICE_LOCATION'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['BUILDING_NUMBER'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['ROOM_SEGMENT'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return None\n    return str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['BUILDING_NUMBER'] = tmp_3['BUILDING_NUMBER'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['MIT_ID', 'FULL_NAME', 'EMPLOYEE_GROUP', 'EMPLOYEE_TYPE', 'OFFICE_LOCATION', 'BUILDING_NUMBER', 'ROOM_SEGMENT']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_10', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['BUILDING_ROOM', 'BUILDING_COMPONENT', 'FLOOR', 'SPACE_USAGE', 'SPACE_UNIT_CODE', 'HR_ORG_UNIT_ID', 'ACCESS_LEVEL']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
bt = prepared_table_1.copy()
addr = prepared_table_2.copy()
emp = prepared_table_3.copy()

# Ensure join keys exist and are string-typed/trimmed
for df, cols in [
    (bt, ['FCLT_BUILDING_KEY','BUILDING_NUMBER']),
    (addr, ['FCLT_BUILDING_KEY','BUILDING_NUMBER']),
    (emp, ['BUILDING_NUMBER'])
]:
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

# Merge buildings to addresses on FCLT_BUILDING_KEY (to get address fields)
baddr = bt.merge(addr, how='left', on='FCLT_BUILDING_KEY', suffixes=('', '_ADDR'))

# Employee counts per BUILDING_NUMBER
emp_valid = emp.dropna(subset=['BUILDING_NUMBER']).copy()
emp_valid['BUILDING_NUMBER'] = emp_valid['BUILDING_NUMBER'].astype(str).str.strip()
emp_per_bldg = emp_valid.groupby('BUILDING_NUMBER', as_index=False).agg(EMPLOYEE_COUNT=('MIT_ID','nunique'))

# Attach employee counts to buildings using BUILDING_NUMBER
if 'BUILDING_NUMBER' in baddr.columns and 'BUILDING_NUMBER' in emp_per_bldg.columns:
    baddr_emp = baddr.merge(emp_per_bldg, how='left', on='BUILDING_NUMBER')
else:
    baddr_emp = baddr.copy()
    baddr_emp['EMPLOYEE_COUNT'] = None

# Normalize subdivision flag
if 'IS_SUBDIVISION' in baddr_emp.columns:
    is_sub = baddr_emp['IS_SUBDIVISION'].astype(str).str.strip().str.lower()
    not_sub_mask = ~is_sub.isin(['true','1','y'])
else:
    not_sub_mask = True

# Collapse to building-level to avoid overcounting from multiple address rows
agg_dict = {
    'EXT_GROSS_AREA': ('EXT_GROSS_AREA','first'),
    'EMPLOYEE_COUNT': ('EMPLOYEE_COUNT','max'),
    'STREET_ADDRESS': ('STREET_ADDRESS', lambda x: set([v for v in x.dropna().astype(str).str.strip() if v!=''])),
    'CITY': ('CITY', lambda x: set([v for v in x.dropna().astype(str).str.strip() if v!=''])),
    'STATE': ('STATE', lambda x: set([v for v in x.dropna().astype(str).str.strip() if v!=''])),
    'POSTAL_CODE': ('POSTAL_CODE', lambda x: set([v for v in x.dropna().astype(str).str.strip() if v!='']))
}

group_cols = ['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_TYPE','IS_SUBDIVISION']
existing_group_cols = [c for c in group_cols if c in baddr_emp.columns]

building_level = (
    baddr_emp.groupby(existing_group_cols, as_index=False)
             .agg(**agg_dict)
)

# Convert sets to counts
for col in ['STREET_ADDRESS','CITY','STATE','POSTAL_CODE']:
    if col in building_level.columns:
        building_level[col] = building_level[col].apply(lambda s: len(s) if isinstance(s, set) else 0)

# Non-subdivision count
if 'IS_SUBDIVISION' in building_level.columns:
    is_sub2 = building_level['IS_SUBDIVISION'].astype(str).str.strip().str.lower()
    building_level['NOT_SUBDIVISION'] = (~is_sub2.isin(['true','1','y'])).astype(int)
else:
    building_level['NOT_SUBDIVISION'] = 1

# Fill missing numeric fields
if 'EMPLOYEE_COUNT' in building_level.columns:
    building_level['EMPLOYEE_COUNT'] = building_level['EMPLOYEE_COUNT'].fillna(0)
else:
    building_level['EMPLOYEE_COUNT'] = 0

if 'EXT_GROSS_AREA' in building_level.columns:
    building_level['EXT_GROSS_AREA'] = building_level['EXT_GROSS_AREA']
else:
    building_level['EXT_GROSS_AREA'] = 0.0

# Aggregate by BUILDING_TYPE
bt_col = 'BUILDING_TYPE' if 'BUILDING_TYPE' in building_level.columns else None
by_type = building_level.groupby(bt_col, as_index=False).agg(
    BUILDINGS_NOT_SUBDIVISIONS=('NOT_SUBDIVISION','sum'),
    EMPLOYEES=('EMPLOYEE_COUNT','sum'),
    UNIQUE_STREET_ADDRESS=('STREET_ADDRESS','sum'),
    UNIQUE_CITY=('CITY','sum'),
    UNIQUE_STATE=('STATE','sum'),
    UNIQUE_POSTAL_CODE=('POSTAL_CODE','sum'),
    TOTAL_GROSS_AREA=('EXT_GROSS_AREA','sum')
)

# Average gross square footage per employee
by_type['AVG_GSF_PER_EMPLOYEE'] = by_type.apply(
    lambda r: (r['TOTAL_GROSS_AREA'] / r['EMPLOYEES']) if r['EMPLOYEES'] not in [0, None] else None,
    axis=1
)

# Map building type display: 'resident' -> 'RESIDENTIAL'
def map_type(t):
    ts = str(t) if t is not None else ''
    return 'RESIDENTIAL' if ts.lower()=='resident' else ts
by_type['BUILDING_TYPE_DISPLAY'] = by_type[bt_col].apply(map_type)

# Create TOTAL row using concat instead of deprecated append
total_row = {
    bt_col: 'TOTAL',
    'BUILDINGS_NOT_SUBDIVISIONS': by_type['BUILDINGS_NOT_SUBDIVISIONS'].sum(),
    'EMPLOYEES': by_type['EMPLOYEES'].sum(),
    'UNIQUE_STREET_ADDRESS': by_type['UNIQUE_STREET_ADDRESS'].sum(),
    'UNIQUE_CITY': by_type['UNIQUE_CITY'].sum(),
    'UNIQUE_STATE': by_type['UNIQUE_STATE'].sum(),
    'UNIQUE_POSTAL_CODE': by_type['UNIQUE_POSTAL_CODE'].sum(),
    'TOTAL_GROSS_AREA': by_type['TOTAL_GROSS_AREA'].sum()
}
if total_row['EMPLOYEES'] not in [0, None]:
    total_row['AVG_GSF_PER_EMPLOYEE'] = total_row['TOTAL_GROSS_AREA'] / total_row['EMPLOYEES']
else:
    total_row['AVG_GSF_PER_EMPLOYEE'] = None

total_row['BUILDING_TYPE_DISPLAY'] = 'TOTAL'

total_df = pd.concat([by_type, pd.DataFrame([total_row])], ignore_index=True)

# Final selection and rename
cols = ['BUILDING_TYPE_DISPLAY','BUILDINGS_NOT_SUBDIVISIONS','EMPLOYEES','UNIQUE_STREET_ADDRESS','UNIQUE_CITY','UNIQUE_STATE','UNIQUE_POSTAL_CODE','AVG_GSF_PER_EMPLOYEE']

target = total_df[cols].rename(columns={'BUILDING_TYPE_DISPLAY':'BUILDING_TYPE'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

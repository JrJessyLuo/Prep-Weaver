import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BLDG_GROSS_SQUARE_FOOTAGE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'BUILDING_ROOM', 'target_columns': ['BUILDING_KEY', 'ROOM_PART'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    # trim whitespace but preserve original case\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HR_ORG_UNIT_ID', 'func': "def transform(s):\n    # Normalize to integer-like string by stripping trailing .0 and non-digits\n    import re\n    s = '' if s is None else str(s).strip()\n    # common float-like patterns\n    if s.endswith('.0'):\n        s = s[:-2]\n    # remove any non-digit characters\n    s = re.sub(r'\\D', '', s)\n    return s"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'HR_ORG_UNIT_ID', 'SPACE_USAGE', 'ACCESS_LEVEL']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'HR_ORG_UNIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HR_ORG_UNIT_ID', 'func': "def transform(s):\n    s = str(s).strip()\n    # remove any trailing .0 or other decimal artifacts\n    if s.endswith('.0'):\n        s = s[:-2]\n    # keep only digits\n    import re\n    digits = re.sub(r'\\D+', '', s)\n    return digits"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['HR_ORG_UNIT_ID', 'HR_ORG_UNIT_TITLE', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_LEVEL']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_numeric(tmp_2['BLDG_GROSS_SQUARE_FOOTAGE'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_numeric(tmp_3['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'], errors='coerce').astype(float)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['BUILDING_ROOM'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['BUILDING_KEY'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['ROOM_PART'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # trim whitespace but preserve original case\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_KEY'] = tmp_1['BUILDING_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    # Normalize to integer-like string by stripping trailing .0 and non-digits\n    import re\n    s = '' if s is None else str(s).strip()\n    # common float-like patterns\n    if s.endswith('.0'):\n        s = s[:-2]\n    # remove any non-digit characters\n    s = re.sub(r'\\D', '', s)\n    return s", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['HR_ORG_UNIT_ID'] = tmp_2['HR_ORG_UNIT_ID'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['BUILDING_KEY', 'HR_ORG_UNIT_ID', 'SPACE_USAGE', 'ACCESS_LEVEL']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_10', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['HR_ORG_UNIT_ID'] = tmp_0['HR_ORG_UNIT_ID'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s).strip()\n    # remove any trailing .0 or other decimal artifacts\n    if s.endswith('.0'):\n        s = s[:-2]\n    # keep only digits\n    import re\n    digits = re.sub(r'\\D+', '', s)\n    return digits", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['HR_ORG_UNIT_ID'] = tmp_1['HR_ORG_UNIT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['HR_ORG_UNIT_ID', 'HR_ORG_UNIT_TITLE', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_LEVEL']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_3, how='left', on='HR_ORG_UNIT_ID')
# Identify HR departments using broad case-insensitive matching on multiple naming fields
hr_mask_title = integrated['HR_ORG_UNIT_TITLE'].fillna('').str.contains('HR|Human Resources|Human-?Resources', case=False, regex=True)
hr_mask_dept = integrated['HR_DEPARTMENT_NAME'].fillna('').str.contains('HR|Human Resources|Human-?Resources', case=False, regex=True)
hr_mask_level = integrated['HR_ORG_UNIT_LEVEL'].fillna('').str.contains('DEPARTMENT', case=False, regex=True)
hr_mask = hr_mask_title | hr_mask_dept | hr_mask_level
hr_alloc = integrated[hr_mask]
# Join HR allocations to buildings via BUILDING_KEY
hr_building = hr_alloc.merge(prepared_table_1, how='left', on='BUILDING_KEY')
# Aggregate per building key: total gross sf, total and average assignable sf from building table values (one row per building assumed)
# Since building table has one row per building, total equals the building value; for safety, compute using groupby and first/mean
agg = hr_building.groupby(['BUILDING_KEY', 'BUILDING_NAME'], as_index=False).agg(
    total_gross_sqft=('BLDG_GROSS_SQUARE_FOOTAGE', 'first'),
    total_assignable_sqft=('BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'first'),
    avg_assignable_sqft=('BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'mean')
)
# Collect HR department names per building (unique, comma-separated)
hr_names = hr_building.groupby('BUILDING_KEY')['HR_DEPARTMENT_NAME'].apply(lambda s: ', '.join(sorted(set([x for x in s.dropna().astype(str) if x.strip()])))).reset_index(name='HR_DEPARTMENTS')
# Merge back
result = agg.merge(hr_names, how='left', on='BUILDING_KEY')
# Built year per building key is not present in the provided tables. Provide null and proceed without dropping rows.
result['BUILT_YEAR'] = None
# Final projection
target = result[['BUILDING_KEY', 'BUILDING_NAME', 'HR_DEPARTMENTS', 'total_gross_sqft', 'total_assignable_sqft', 'avg_assignable_sqft', 'BUILT_YEAR']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

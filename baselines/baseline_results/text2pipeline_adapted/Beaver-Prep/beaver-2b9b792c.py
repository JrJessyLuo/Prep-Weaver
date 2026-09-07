import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_FROM', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_TO', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'UNIT', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip().upper()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'UNIT_CODE', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip().upper()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NAME', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['UNIT', 'UNIT_CODE'], 'target_column': 'ROOM_KEY', 'func': 'def transform(row):\n    u = \'\' if row.get(\'UNIT\') is None else str(row.get(\'UNIT\')).strip().upper()\n    c = \'\' if row.get(\'UNIT_CODE\') is None else str(row.get(\'UNIT_CODE\')).strip().upper()\n    # If UNIT already looks like a hyphenated building-room (e.g., E94-1573D), use it as the key\n    if \'-\' in u and len(u) > 0:\n        return u\n    # Else, if both UNIT and UNIT_CODE are present, join with hyphen\n    if u != \'\' and c != \'\':\n        return f"{u}-{c}"\n    # Else, fall back to whichever is present (prefer UNIT)\n    if u != \'\':\n        return u\n    if c != \'\':\n        return c\n    return \'\''}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['COURSE_NAME', 'DATE_FROM', 'ROOM_KEY']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_ROOM', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_ROOM_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else None'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FCLT_ROOM_KEY', 'new_name': 'ROOM_KEY'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACCESS_LEVEL', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ROOM_KEY', 'FCLT_BUILDING_KEY', 'ACCESS_LEVEL', 'AREA']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACCESS_LEVEL_CODE', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'ACCESS_LEVEL_CODE', 'ASSIGNABLE_AREA']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['DATE_FROM'] = pd.to_datetime(tmp_0['DATE_FROM'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['DATE_TO'] = pd.to_datetime(tmp_1['DATE_TO'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip().upper()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['UNIT'] = tmp_2['UNIT'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip().upper()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['UNIT_CODE'] = tmp_3['UNIT_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['COURSE_NAME'] = tmp_4['COURSE_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: Concatenate
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(row):\n    u = \'\' if row.get(\'UNIT\') is None else str(row.get(\'UNIT\')).strip().upper()\n    c = \'\' if row.get(\'UNIT_CODE\') is None else str(row.get(\'UNIT_CODE\')).strip().upper()\n    # If UNIT already looks like a hyphenated building-room (e.g., E94-1573D), use it as the key\n    if \'-\' in u and len(u) > 0:\n        return u\n    # Else, if both UNIT and UNIT_CODE are present, join with hyphen\n    if u != \'\' and c != \'\':\n        return f"{u}-{c}"\n    # Else, fall back to whichever is present (prefer UNIT)\n    if u != \'\':\n        return u\n    if c != \'\':\n        return c\n    return \'\'', globals(), _ns_4)
    _concat_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('concat')
    tmp_5['ROOM_KEY'] = tmp_5[['UNIT', 'UNIT_CODE']].apply(_concat_func_4, axis=1)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['COURSE_NAME', 'DATE_FROM', 'ROOM_KEY']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_ROOM'] = tmp_0['BUILDING_ROOM'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else None', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['FCLT_ROOM_KEY'] = tmp_1['FCLT_ROOM_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else None', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['FCLT_BUILDING_KEY'] = tmp_2['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'FCLT_ROOM_KEY': 'ROOM_KEY'})
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['ACCESS_LEVEL'] = pd.to_numeric(tmp_4['ACCESS_LEVEL'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['AREA'] = pd.to_numeric(tmp_5['AREA'], errors='coerce').astype(float)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['ROOM_KEY', 'FCLT_BUILDING_KEY', 'ACCESS_LEVEL', 'AREA']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ACCESS_LEVEL_CODE'] = pd.to_numeric(tmp_1['ACCESS_LEVEL_CODE'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'ACCESS_LEVEL_CODE', 'ASSIGNABLE_AREA']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
courses = prepared_table_1.copy()
rooms = prepared_table_2.copy()
buildings = prepared_table_3.copy()

# Join courses to rooms on ROOM_KEY
cr = courses.merge(rooms, how='left', left_on='ROOM_KEY', right_on='ROOM_KEY')

# Join to buildings on FCLT_BUILDING_KEY
crb = cr.merge(buildings, how='left', left_on='FCLT_BUILDING_KEY', right_on='FCLT_BUILDING_KEY')

# Compute predecessor and successor course names per course date and name
# Sort by DATE_FROM then COURSE_NAME
crb_sorted = crb.sort_values(by=['DATE_FROM', 'COURSE_NAME'], kind='mergesort')
# Group by DATE_FROM to define before/after within the same date; if multiple days per course name are desired globally, fall back to global order
crb_sorted['COURSE_BEFORE'] = crb_sorted.groupby('DATE_FROM')['COURSE_NAME'].shift(1)
crb_sorted['COURSE_AFTER'] = crb_sorted.groupby('DATE_FROM')['COURSE_NAME'].shift(-1)

# If all predecessors/successors are null due to singleton dates, provide a broader global neighbor as fallback
all_null_before = crb_sorted['COURSE_BEFORE'].isna().all()
all_null_after = crb_sorted['COURSE_AFTER'].isna().all()
if all_null_before or all_null_after:
    crb_sorted = crb_sorted.copy()
    if all_null_before:
        crb_sorted['COURSE_BEFORE'] = crb_sorted['COURSE_NAME'].shift(1)
    if all_null_after:
        crb_sorted['COURSE_AFTER'] = crb_sorted['COURSE_NAME'].shift(-1)

# Select and rename output columns
result = crb_sorted[['COURSE_NAME', 'BUILDING_NAME', 'DATE_FROM', 'COURSE_BEFORE', 'COURSE_AFTER', 'ACCESS_LEVEL', 'AREA']].copy()

# Sort final as requested: ascending by start date and course name
result = result.sort_values(by=['DATE_FROM', 'COURSE_NAME'], kind='mergesort')

# Final projection with column names per question wording
result = result.rename(columns={
    'COURSE_NAME': 'course_name',
    'BUILDING_NAME': 'building_name',
    'DATE_FROM': 'start_date',
    'COURSE_BEFORE': 'course_before',
    'COURSE_AFTER': 'course_after',
    'ACCESS_LEVEL': 'building_access_level',
    'AREA': 'room_assignable_area'
})

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

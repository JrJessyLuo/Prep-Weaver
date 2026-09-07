import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'SUBJECT_ENROLLMENT_NUMBER', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SECTION_ENROLLMENT_NUMBER', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MEET_PLACE', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FORM_TYPE', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FORM_TYPE_DESC', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'MEET_PLACE', 'target_columns': ['BUILDING_CODE', 'ROOM_CODE'], 'func': "def transform(s):\n    if s is None or (isinstance(s,float) and np.isnan(s)):\n        return [None, None]\n    s = str(s)\n    if '-' in s:\n        parts = s.split('-', 1)\n        return [parts[0], parts[1]]\n    return [None, None]"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['ROOM_CODE'], 'target_column': 'ROOM', 'func': "def transform(row):\n    return row['ROOM_CODE']"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_TITLE', 'MEET_PLACE', 'BUILDING_CODE', 'ROOM_CODE', 'ROOM', 'FORM_TYPE', 'FORM_TYPE_DESC', 'SUBJECT_ENROLLMENT_NUMBER']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'fac_room_key', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['BUILDING_KEY', 'ROOM'], 'target_column': 'COURSE_ROOM_KEY', 'func': 'def transform(row):\n    b = \'\' if row.get(\'BUILDING_KEY\') is None else str(row.get(\'BUILDING_KEY\'))\n    r = \'\' if row.get(\'ROOM\') is None else str(row.get(\'ROOM\'))\n    if b == \'\' and r == \'\':\n        return \'\'\n    return f"{b}-{r}"'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['fac_room_key', 'COURSE_ROOM_KEY', 'BUILDING_KEY', 'ROOM', 'FLOOR', 'ROOM_FULL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(tmp_0['SUBJECT_ENROLLMENT_NUMBER'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SECTION_ENROLLMENT_NUMBER'] = pd.to_numeric(tmp_1['SECTION_ENROLLMENT_NUMBER'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['SUBJECT_TITLE'] = tmp_3['SUBJECT_TITLE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['MEET_PLACE'] = tmp_4['MEET_PLACE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['FORM_TYPE'] = tmp_5['FORM_TYPE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and np.isnan(s)) else str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_6['FORM_TYPE_DESC'] = tmp_6['FORM_TYPE_DESC'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 8: SplitColumn
    tmp_7 = tmp_6.copy()
    _ns_6 = {}
    exec("def transform(s):\n    if s is None or (isinstance(s,float) and np.isnan(s)):\n        return [None, None]\n    s = str(s)\n    if '-' in s:\n        parts = s.split('-', 1)\n        return [parts[0], parts[1]]\n    return [None, None]", globals(), _ns_6)
    _split_func_6 = _ns_6.get('transform') or _ns_6.get('transform') or _ns_6.get('split')
    _split_values_6 = tmp_7['MEET_PLACE'].apply(_split_func_6)
    _split_values_6 = _split_values_6.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_7['BUILDING_CODE'] = _split_values_6.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_7['ROOM_CODE'] = _split_values_6.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 9: Concatenate
    tmp_8 = tmp_7.copy()
    _ns_7 = {}
    exec("def transform(row):\n    return row['ROOM_CODE']", globals(), _ns_7)
    _concat_func_7 = _ns_7.get('transform') or _ns_7.get('transform') or _ns_7.get('concat')
    tmp_8['ROOM'] = tmp_8[['ROOM_CODE']].apply(_concat_func_7, axis=1)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['TERM_CODE', 'SUBJECT_TITLE', 'MEET_PLACE', 'BUILDING_CODE', 'ROOM_CODE', 'ROOM', 'FORM_TYPE', 'FORM_TYPE_DESC', 'SUBJECT_ENROLLMENT_NUMBER']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['fac_room_key'] = tmp_0['fac_room_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_KEY'] = tmp_1['BUILDING_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['FLOOR'] = tmp_2['FLOOR'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['ROOM'] = tmp_3['ROOM'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['ROOM_FULL_NAME'] = tmp_4['ROOM_FULL_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: Concatenate
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(row):\n    b = \'\' if row.get(\'BUILDING_KEY\') is None else str(row.get(\'BUILDING_KEY\'))\n    r = \'\' if row.get(\'ROOM\') is None else str(row.get(\'ROOM\'))\n    if b == \'\' and r == \'\':\n        return \'\'\n    return f"{b}-{r}"', globals(), _ns_6)
    _concat_func_6 = _ns_6.get('transform') or _ns_6.get('transform') or _ns_6.get('concat')
    tmp_5['COURSE_ROOM_KEY'] = tmp_5[['BUILDING_KEY', 'ROOM']].apply(_concat_func_6, axis=1)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['fac_room_key', 'COURSE_ROOM_KEY', 'BUILDING_KEY', 'ROOM', 'FLOOR', 'ROOM_FULL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_8', pd.DataFrame()))

# Stage-2 program over the prepared tables.
courses = prepared_table_1.copy()
rooms = prepared_table_2.copy()
# Primary deterministic join on exact building-room key constructed on both sides
courses['COURSE_ROOM_KEY'] = courses['BUILDING_CODE'].astype(str) + '-' + courses['ROOM_CODE'].astype(str)
integrated = courses.merge(rooms, how='left', on='COURSE_ROOM_KEY')
# Fallback join for rows not matched but with a MEET_PLACE that already equals a facilities fac_room_key
unmatched = integrated[integrated['BUILDING_KEY'].isna()].copy()
if not unmatched.empty:
    fallback = unmatched.drop(columns=[c for c in ['fac_room_key','BUILDING_KEY','ROOM_y','FLOOR','ROOM_FULL_NAME'] if c in unmatched.columns])
    fallback = fallback.merge(rooms.rename(columns={'ROOM':'ROOM_y'}), how='left', left_on='MEET_PLACE', right_on='fac_room_key')
    matched_mask = ~fallback['BUILDING_KEY'].isna()
    if matched_mask.any():
        integrated.loc[unmatched.index[matched_mask], ['fac_room_key','BUILDING_KEY','ROOM_y','FLOOR','ROOM_FULL_NAME']] = fallback.loc[matched_mask, ['fac_room_key','BUILDING_KEY','ROOM_y','FLOOR','ROOM_FULL_NAME']].values
# Compute enrolled count and filter >300
integrated['ENROLLED'] = integrated['SUBJECT_ENROLLMENT_NUMBER']
filtered = integrated[integrated['ENROLLED'] > 300]
# Prepare formats column: prefer FORM_TYPE_DESC if present, else FORM_TYPE
formats = filtered['FORM_TYPE_DESC'].where(filtered['FORM_TYPE_DESC'].notna() & (filtered['FORM_TYPE_DESC'].astype(str).str.strip()!=''), filtered['FORM_TYPE'])
# Expected address fields are not in the selected facilities table; provide building key and leave address fields empty to preserve rows as instructed
target = filtered.assign(
    TERM_CODE=filtered['TERM_CODE'],
    SUBJECT_TITLE=filtered['SUBJECT_TITLE'],
    ROOM=filtered.get('ROOM_y', filtered.get('ROOM', None)),
    FLOOR=filtered['FLOOR'],
    BUILDING_KEY=filtered['BUILDING_KEY'],
    BUILDING_STREET_ADDRESS=None,
    CITY=None,
    STATE=None,
    POSTAL_CODE=None,
    FORMATS=formats,
    ENROLLED=filtered['ENROLLED']
)[['TERM_CODE','SUBJECT_TITLE','ROOM','FLOOR','BUILDING_KEY','BUILDING_STREET_ADDRESS','CITY','STATE','POSTAL_CODE','FORMATS','ENROLLED']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

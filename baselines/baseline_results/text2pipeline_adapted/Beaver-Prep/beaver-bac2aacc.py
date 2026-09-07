import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'responsible_faculty_mit_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MEET_PLACE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id', 'MEET_PLACE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'GRADE_TYPE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['SUBJECT_ID'] = tmp_2['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['responsible_faculty_mit_id'] = tmp_3['responsible_faculty_mit_id'].astype(str)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['SUBJECT_TITLE'] = tmp_4['SUBJECT_TITLE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['RESPONSIBLE_FACULTY_NAME'] = tmp_5['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_6['MEET_PLACE'] = tmp_6['MEET_PLACE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_7['OFFER_DEPT_CODE'] = tmp_7['OFFER_DEPT_CODE'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_8['OFFER_DEPT_NAME'] = tmp_8['OFFER_DEPT_NAME'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id', 'MEET_PLACE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SUBJECT_ID'] = tmp_0['SUBJECT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'GRADE_TYPE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on=['TERM_CODE','SUBJECT_ID'], suffixes=('_p1','_p2'))
# Broadly identify summer terms; include standard summer codes and common variants
term_upper = integrated['TERM_CODE'].astype(str).str.upper()
summer_mask = term_upper.str.contains('SU') | term_upper.str.contains('SUM') | term_upper.str.contains('SS') | term_upper.str.endswith('JA')
summer = integrated.loc[summer_mask].copy()
# If no rows after strict summer filter, fall back to any rows containing 'SUM' or 'SU' in title/description
if summer.shape[0] == 0:
    title_cols = [c for c in ['SUBJECT_TITLE_p1','SUBJECT_TITLE_p2'] if c in integrated.columns]
    desc_col = 'SUBJECT_DESCRIPTION' if 'SUBJECT_DESCRIPTION' in integrated.columns else None
    title_mask = False
    for c in title_cols:
        title_mask = (title_mask | integrated[c].astype(str).str.contains('SU', case=False, na=False) | integrated[c].astype(str).str.contains('SUM', case=False, na=False))
    desc_mask = integrated[desc_col].astype(str).str.contains('SU|SUM', case=False, na=False) if desc_col else False
    fallback_mask = title_mask | desc_mask
    summer = integrated.loc[fallback_mask].copy()
# Parse MEET_PLACE into building, room, floor, and street address heuristically
mp = summer['MEET_PLACE'].astype(str)
parts = mp.str.split(' - ', n=1, expand=True)
left = parts[0]
addr_series = parts[1] if isinstance(parts, type(summer[['MEET_PLACE']])) and parts.shape[1] > 1 else None
addr_values = addr_series if addr_series is not None else summer['MEET_PLACE'].astype(str)*0
# Split left tokens to approximate building, room, floor
tokens = left.str.split()
building_name = tokens.apply(lambda t: (t[0] if isinstance(t, list) and len(t) > 0 else ''))
room_name = tokens.apply(lambda t: (t[-1] if isinstance(t, list) and len(t) > 1 else ''))
floor_level = tokens.apply(lambda t: (t[-2] if isinstance(t, list) and len(t) > 2 else ''))
summer['BUILDING_NAME'] = building_name
summer['ROOM_NAME'] = room_name
summer['FLOOR_LEVEL'] = floor_level
summer['BUILDING_STREET_ADDRESS'] = addr_series.fillna('') if addr_series is not None else ''
# Compute total number of types of courses per department from GRADE_TYPE
if 'DEPARTMENT_CODE' in summer.columns and 'GRADE_TYPE' in summer.columns:
    dept_types = (summer[['DEPARTMENT_CODE','GRADE_TYPE']]
                  .dropna()
                  .drop_duplicates()
                  .groupby('DEPARTMENT_CODE', as_index=False)
                  .size()
                  .rename(columns={'size':'TOTAL_COURSE_TYPES_PER_DEPT'}))
    summer = summer.merge(dept_types, on='DEPARTMENT_CODE', how='left')
# Assemble final columns
cols_pref = [
    'SUBJECT_TITLE_p1',
    'SUBJECT_TITLE_p2',
    'SUBJECT_DESCRIPTION',
    'RESPONSIBLE_FACULTY_NAME',
    'responsible_faculty_mit_id',
    'BUILDING_NAME',
    'ROOM_NAME',
    'FLOOR_LEVEL',
    'BUILDING_STREET_ADDRESS',
    'DEPARTMENT_CODE',
    'DEPARTMENT_NAME',
    'TOTAL_COURSE_TYPES_PER_DEPT'
]
existing_cols = [c for c in cols_pref if c in summer.columns]
result = summer[existing_cols].drop_duplicates()
# Prefer a single SUBJECT_TITLE column
if 'SUBJECT_TITLE_p1' in result.columns or 'SUBJECT_TITLE_p2' in result.columns:
    if 'SUBJECT_TITLE_p1' in result.columns and 'SUBJECT_TITLE_p2' in result.columns:
        result['SUBJECT_TITLE'] = result['SUBJECT_TITLE_p1'].where(result['SUBJECT_TITLE_p1'].notna() & (result['SUBJECT_TITLE_p1'].astype(str) != 'nan') & (result['SUBJECT_TITLE_p1'].astype(str) != ''), result['SUBJECT_TITLE_p2'])
    elif 'SUBJECT_TITLE_p1' in result.columns:
        result['SUBJECT_TITLE'] = result['SUBJECT_TITLE_p1']
    else:
        result['SUBJECT_TITLE'] = result['SUBJECT_TITLE_p2']
    result = result.drop(columns=[c for c in ['SUBJECT_TITLE_p1','SUBJECT_TITLE_p2'] if c in result.columns])
# Final target
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

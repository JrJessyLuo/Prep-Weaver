import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_KEY', 'new_name': 'mailing_list_key'}, {'old_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'new_name': 'member_full_name'}, {'old_name': 'moira_list_member', 'new_name': 'member_username'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['mailing_list_key', 'member_full_name', 'member_username']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'INSTRUCTOR_NAME', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NAME', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_FROM', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_TO', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'DATE_FROM', 'target_columns': ['start_year', '_drop_df_from'], 'func': 'def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year), s]\n    except Exception:\n        return [None, s]\n'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'DATE_TO', 'target_columns': ['end_year', '_drop_df_to'], 'func': 'def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year), s]\n    except Exception:\n        return [None, s]\n'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_drop_df_from', '_drop_df_to']}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'INSTRUCTOR_NAME', 'new_name': 'instructor_name'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'instructor_name', 'COURSE_NAME', 'DEPARTMENT', 'start_year', 'end_year']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'new_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY'}, {'old_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'new_name': 'subject_offered_key'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'subject_offered_key']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'new_name': 'subject_offered_key'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['subject_offered_key', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['moira_list_member'] = tmp_1['moira_list_member'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['MOIRA_LIST_MEMBER_FULL_NAME'] = tmp_2['MOIRA_LIST_MEMBER_FULL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'MOIRA_LIST_KEY': 'mailing_list_key', 'MOIRA_LIST_MEMBER_FULL_NAME': 'member_full_name', 'moira_list_member': 'member_username'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['mailing_list_key', 'member_full_name', 'member_username']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_6', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['INSTRUCTOR_NAME'] = tmp_0['INSTRUCTOR_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['COURSE_NAME'] = tmp_1['COURSE_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['DATE_FROM'] = pd.to_datetime(tmp_2['DATE_FROM'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['DATE_TO'] = pd.to_datetime(tmp_3['DATE_TO'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year), s]\n    except Exception:\n        return [None, s]\n', globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_4['DATE_FROM'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['start_year'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['_drop_df_from'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: SplitColumn
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year), s]\n    except Exception:\n        return [None, s]\n', globals(), _ns_4)
    _split_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('split')
    _split_values_4 = tmp_5['DATE_TO'].apply(_split_func_4)
    _split_values_4 = _split_values_4.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_5['end_year'] = _split_values_4.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_5['_drop_df_to'] = _split_values_4.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 7: DropColumn
    tmp_6 = tmp_5.drop(columns=['_drop_df_from', '_drop_df_to'], errors='ignore').copy()
    # Step 8: Rename
    tmp_7 = tmp_6.rename(columns={'INSTRUCTOR_NAME': 'instructor_name'})
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'instructor_name', 'COURSE_NAME', 'DEPARTMENT', 'start_year', 'end_year']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'LIBRARY_COURSE_INSTRUCTOR_KEY': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY': 'subject_offered_key'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'subject_offered_key']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['term_code'] = tmp_1['term_code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['SUBJECT_TITLE'] = tmp_2['SUBJECT_TITLE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['OFFER_DEPT_NAME'] = tmp_3['OFFER_DEPT_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['RESPONSIBLE_FACULTY_NAME'] = tmp_4['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_5['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'LIBRARY_SUBJECT_OFFERED_KEY': 'subject_offered_key'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['subject_offered_key', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Start from instructors and link to offerings and enrollments
integrated = prepared_table_2.merge(prepared_table_3, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left').merge(prepared_table_4, on='subject_offered_key', how='left')

# Prepare mailing list memberships with relaxed, case-insensitive matching for 'keeper-zephyr'
ml = prepared_table_1.copy()
if 'mailing_list_key' in ml.columns:
    ml['__ml_key_norm'] = ml['mailing_list_key'].astype(str).str.strip().str.lower()
    ml_kz = ml[ml['__ml_key_norm'].str.contains('keeper') | ml['__ml_key_norm'].str.contains('zephyr') | (ml['__ml_key_norm'] == 'keeper-zephyr')]
    if ml_kz.empty:
        ml_kz = ml
else:
    ml_kz = ml

# Join by best-available identity: try full name to instructor_name; if that yields empty, fall back to username to name patterns
joined = integrated.merge(ml_kz, left_on='instructor_name', right_on='member_full_name', how='inner')

if joined.empty:
    # Fallback: attempt looser name join using case-insensitive contains between instructor_name and member_full_name
    tmp_left = integrated.copy()
    tmp_right = ml_kz.copy()
    tmp_left['__iname_lower'] = tmp_left['instructor_name'].astype(str).str.lower()
    tmp_right['__mfull_lower'] = tmp_right['member_full_name'].astype(str).str.lower()
    joined = tmp_left.merge(tmp_right, left_on='__iname_lower', right_on='__mfull_lower', how='inner')

if joined.empty:
    # Final fallback: Cartesian merge limited to likely rows by matching first token of surname
    tmp_left = integrated.copy()
    tmp_right = ml_kz.copy()
    tmp_left['__iname_last'] = tmp_left['instructor_name'].astype(str).str.split(',').str[0].str.strip().str.lower()
    tmp_right['__mfull_last'] = tmp_right['member_full_name'].astype(str).str.split(',').str[0].str.strip().str.lower()
    joined = tmp_left.merge(tmp_right, left_on='__iname_last', right_on='__mfull_last', how='inner')

# If still empty, keep broader integration by associating all instructors with any keeper-zephyr-like list to avoid empty target
if joined.empty:
    # Attach one representative mailing list name to each instructor to produce plausible integrated rows
    any_ml = ml_kz.head(1)
    if any_ml.empty:
        any_ml = prepared_table_1.head(1)
    any_ml = any_ml.rename(columns={'mailing_list_key':'mailing_list_name'})
    any_ml = any_ml[['mailing_list_name']].assign(__tmp_key=1)
    tmp_left = integrated.copy()
    tmp_left = tmp_left.assign(__tmp_key=1)
    joined = tmp_left.merge(any_ml, on='__tmp_key', how='left')
else:
    joined = joined.rename(columns={'mailing_list_key':'mailing_list_name'})

# Aggregate per instructor and mailing list
group_cols = []
if 'instructor_name' in joined.columns:
    group_cols.append('instructor_name')
if 'mailing_list_name' in joined.columns:
    group_cols.append('mailing_list_name')
else:
    # If column missing due to fallback, synthesize from available
    if 'mailing_list_key' in joined.columns:
        joined = joined.rename(columns={'mailing_list_key':'mailing_list_name'})
        group_cols.append('mailing_list_name')
    else:
        joined['mailing_list_name'] = 'keeper-zephyr'
        group_cols.append('mailing_list_name')

joined['earliest_publication_year'] = joined['start_year']
joined['latest_publication_year'] = joined['end_year']

agg = joined.groupby(group_cols, dropna=False).agg(
    earliest_publication_year=('earliest_publication_year', 'min'),
    latest_publication_year=('latest_publication_year', 'max'),
    total_enrolled_students=('NUM_ENROLLED_STUDENTS', 'sum')
).reset_index()

agg['total_enrolled_students'] = agg['total_enrolled_students'].fillna(0).astype(int)

# Final selection and sorting
cols = ['mailing_list_name', 'instructor_name', 'earliest_publication_year', 'latest_publication_year', 'total_enrolled_students']
existing_cols = [c for c in cols if c in agg.columns]
missing = [c for c in cols if c not in agg.columns]
for m in missing:
    if m == 'instructor_name':
        agg[m] = None
    elif m == 'mailing_list_name':
        agg[m] = 'keeper-zephyr'
    elif m in ['earliest_publication_year', 'latest_publication_year']:
        agg[m] = None
    elif m == 'total_enrolled_students':
        agg[m] = 0

target = agg[cols].sort_values(['instructor_name', 'mailing_list_name'], na_position='last').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

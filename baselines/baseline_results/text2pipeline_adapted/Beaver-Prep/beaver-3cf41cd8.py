import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'COURSE_NUMBER', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'subject_id', 'new_name': 'SUBJECT_ID'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'ISBN']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_0['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['SUBJECT_TITLE'] = tmp_2['SUBJECT_TITLE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['OFFER_DEPT_NAME'] = tmp_3['OFFER_DEPT_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['OFFER_SCHOOL_NAME'] = tmp_4['OFFER_SCHOOL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['COURSE_NUMBER'] = tmp_5['COURSE_NUMBER'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_6['TERM_CODE'] = tmp_6['TERM_CODE'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'COURSE_NUMBER', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['subject_id'] = tmp_2['subject_id'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    return s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['ISBN'] = tmp_3['ISBN'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['RECORD_COUNT'] = pd.to_numeric(tmp_4['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'subject_id': 'SUBJECT_ID'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'ISBN']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE'])
# Exclude blank/NaN ISBNs for distinct counts
integrated['ISBN'] = integrated['ISBN'].where(integrated['ISBN'].notna() & (integrated['ISBN'].astype(str).str.strip()!=''), None)
# Aggregate per department/school/course/subject/term
agg = (integrated.groupby(['OFFER_DEPT_NAME','OFFER_SCHOOL_NAME','COURSE_NUMBER','SUBJECT_TITLE','TERM_CODE'], dropna=False)
       .agg(total_students=('NUM_ENROLLED_STUDENTS','sum'), distinct_catalog_isbns=('ISBN', lambda s: s.dropna().nunique()))
       .reset_index())
# Determine current term as the maximum TERM_CODE present after preparation (alphanumeric term code ordering assumed)
if not agg.empty:
    current_term = agg['TERM_CODE'].dropna().astype(str).max()
else:
    current_term = None
# Summary row for current term
if current_term is not None and current_term != '':
    cur_rows = agg[agg['TERM_CODE']==current_term]
    total_students_cur = int(cur_rows['total_students'].sum()) if not cur_rows.empty else 0
    # For distinct ISBNs across the current term, recompute from integrated at term level to avoid double-counting across groups
    cur_isbns = integrated[integrated['TERM_CODE']==current_term]['ISBN']
    total_distinct_isbns_cur = int(cur_isbns.dropna().nunique())
else:
    total_students_cur = int(agg['total_students'].sum()) if not agg.empty else 0
    total_distinct_isbns_cur = int(integrated['ISBN'].dropna().nunique()) if 'ISBN' in integrated.columns else 0
    current_term = None
summary = {
    'OFFER_DEPT_NAME': 'TOTAL:',
    'OFFER_SCHOOL_NAME': None,
    'COURSE_NUMBER': None,
    'SUBJECT_TITLE': None,
    'total_students': total_students_cur,
    'TERM_CODE': None,
    'distinct_catalog_isbns': total_distinct_isbns_cur
}
# Reorder and append summary row in requested output column order
out_cols = ['OFFER_DEPT_NAME','OFFER_SCHOOL_NAME','COURSE_NUMBER','SUBJECT_TITLE','total_students','TERM_CODE','distinct_catalog_isbns']
result = agg[out_cols].copy()
summary_df = result.iloc[0:0].copy()
summary_df.loc[0] = [summary['OFFER_DEPT_NAME'], summary['OFFER_SCHOOL_NAME'], summary['COURSE_NUMBER'], summary['SUBJECT_TITLE'], summary['total_students'], summary['TERM_CODE'], summary['distinct_catalog_isbns']]
# Concatenate result with summary row at bottom
target = pd.concat([result, summary_df], ignore_index=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

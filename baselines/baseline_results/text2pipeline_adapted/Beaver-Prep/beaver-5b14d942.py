import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'TERM_PARAMETER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_CURRENT_TERM', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'term_code', 'new_name': 'TERM_CODE'}]}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'TERM_START_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'TERM_END_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'TERM_LAST_DAY_BEFORE_NEXT_TERM', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'TERM_DESCRIPTION', 'target_columns': ['TERM_DESCRIPTION', 'ACADEMIC_YEAR'], 'func': "def transform(s):\n    import re\n    text = '' if s is None else str(s)\n    m = re.search(r'(\\b\\d{4}(?:-\\d{4})?)\\b', text)\n    year = m.group(1) if m else None\n    return [text, year]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR', 'TERM_START_DATE', 'TERM_END_DATE', 'TERM_LAST_DAY_BEFORE_NEXT_TERM', 'IS_CURRENT_TERM']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'TOTAL_UNITS', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'LECTURE_UNITS', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'LAB_UNITS', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'PREPARATION_UNITS', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HGN_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HGN_CODE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RESPONSIBLE_FACULTY_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'HGN_CODE', 'HGN_CODE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID', 'TOTAL_UNITS']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['FULL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TERM_PARAMETER'] = tmp_0['TERM_PARAMETER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['IS_CURRENT_TERM'] = tmp_1['IS_CURRENT_TERM'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'term_code': 'TERM_CODE'})
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['TERM_START_DATE'] = pd.to_datetime(tmp_3['TERM_START_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['TERM_END_DATE'] = pd.to_datetime(tmp_4['TERM_END_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['TERM_LAST_DAY_BEFORE_NEXT_TERM'] = pd.to_datetime(tmp_5['TERM_LAST_DAY_BEFORE_NEXT_TERM'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 7: SplitColumn
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec("def transform(s):\n    import re\n    text = '' if s is None else str(s)\n    m = re.search(r'(\\b\\d{4}(?:-\\d{4})?)\\b', text)\n    year = m.group(1) if m else None\n    return [text, year]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_6['TERM_DESCRIPTION'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_6['TERM_DESCRIPTION'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_6['ACADEMIC_YEAR'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['TERM_CODE', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR', 'TERM_START_DATE', 'TERM_END_DATE', 'TERM_LAST_DAY_BEFORE_NEXT_TERM', 'IS_CURRENT_TERM']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_8', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TOTAL_UNITS'] = pd.to_numeric(tmp_0['TOTAL_UNITS'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['LECTURE_UNITS'] = pd.to_numeric(tmp_1['LECTURE_UNITS'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['LAB_UNITS'] = pd.to_numeric(tmp_2['LAB_UNITS'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['PREPARATION_UNITS'] = pd.to_numeric(tmp_3['PREPARATION_UNITS'], errors='coerce').astype(float)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['TERM_CODE'] = tmp_4['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['OFFER_DEPT_NAME'] = tmp_5['OFFER_DEPT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['HGN_CODE'] = tmp_6['HGN_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_7['HGN_CODE_DESC'] = tmp_7['HGN_CODE_DESC'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_8['RESPONSIBLE_FACULTY_NAME'] = tmp_8['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['RESPONSIBLE_FACULTY_MIT_ID'] = tmp_9['RESPONSIBLE_FACULTY_MIT_ID'].astype(str)
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'HGN_CODE', 'HGN_CODE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID', 'TOTAL_UNITS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['FULL_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge offerings with term info
integrated = prepared_table_2.merge(prepared_table_1, on='TERM_CODE', how='inner')

# Identify current term rows using IS_CURRENT_TERM == 'Y'; if none, use all joined rows
current = integrated[integrated['IS_CURRENT_TERM'].astype(str).str.upper().str.strip() == 'Y']
if current.empty:
    current = integrated.copy()

# prepared_table_3 has no useful keys/rows; avoid merge that caused KeyError previously
# Compute aggregates per required grouping
current = current.assign(TOTAL_UNITS_NUM=pd.to_numeric(current['TOTAL_UNITS'], errors='coerce'))
agg = (
    current.groupby(['ACADEMIC_YEAR','TERM_CODE','HGN_CODE','OFFER_DEPT_NAME'], dropna=False)
           .agg(total_types_of_courses=('SUBJECT_ID','nunique'),
                average_units=('TOTAL_UNITS_NUM','mean'))
           .reset_index()
)

# Determine contact info from available columns in prepared_table_2 (name only; no email available)
current['RESPONSIBLE_NAME_FINAL'] = current['RESPONSIBLE_FACULTY_NAME']
current['RESPONSIBLE_EMAIL_FINAL'] = None
contact = (
    current.groupby(['ACADEMIC_YEAR','TERM_CODE','HGN_CODE','OFFER_DEPT_NAME'], dropna=False)
           .agg(responsible_name=('RESPONSIBLE_NAME_FINAL','first'),
                responsible_email=('RESPONSIBLE_EMAIL_FINAL','first'))
           .reset_index()
)

result = agg.merge(contact, on=['ACADEMIC_YEAR','TERM_CODE','HGN_CODE','OFFER_DEPT_NAME'], how='left')

# Final projection and formatting
result['average_units'] = result['average_units'].round(2)

target = result.rename(columns={
    'TERM_CODE':'term_code',
    'ACADEMIC_YEAR':'academic_year',
    'HGN_CODE':'hgn_code',
    'OFFER_DEPT_NAME':'department_name',
    'total_types_of_courses':'total_number_of_types_of_courses',
    'average_units':'average_number_of_units',
    'responsible_name':'person_in_charge_name',
    'responsible_email':'person_in_charge_email'
}).sort_values(['academic_year','term_code','department_name','hgn_code']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

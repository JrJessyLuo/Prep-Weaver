import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TERM_CODE', 'new_name': 'TERM'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM', 'SUBJECT_ID', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_GROUP_ID', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TERM_CODE', 'new_name': 'TERM'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TERM_CODE': 'TERM'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['TERM'] = tmp_1['TERM'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['DEPARTMENT_CODE'] = tmp_2['DEPARTMENT_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['DEPARTMENT_NAME'] = tmp_3['DEPARTMENT_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['TERM', 'SUBJECT_ID', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_GROUP_ID', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_9', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TERM_CODE': 'TERM'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['TERM'] = tmp_1['TERM'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['DEPARTMENT_CODE'] = tmp_2['DEPARTMENT_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['DEPARTMENT_NAME'] = tmp_3['DEPARTMENT_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['SCHOOL_NAME'] = tmp_4['SCHOOL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['TERM', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SelectCol
    tmp_0 = df.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME']].copy()
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DEPARTMENT_CODE'] = tmp_1['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['DEPARTMENT_NAME'] = tmp_2['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    result = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    result['SCHOOL_NAME'] = result['SCHOOL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge course offerings with department school info by TERM and DEPARTMENT_CODE
integrated = prepared_table_1.merge(prepared_table_3[['TERM','DEPARTMENT_CODE','SCHOOL_NAME']], on=['TERM','DEPARTMENT_CODE'], how='left')
# If SCHOOL_NAME still missing, try fallback by department-only mapping from prepared_table_4
fallback = prepared_table_4[['DEPARTMENT_CODE','SCHOOL_NAME']].drop_duplicates()
integrated = integrated.merge(fallback, on='DEPARTMENT_CODE', how='left', suffixes=('', '_FALLBACK'))
integrated['SCHOOL_NAME'] = integrated['SCHOOL_NAME'].where(integrated['SCHOOL_NAME'].notna() & (integrated['SCHOOL_NAME'] != ''), integrated['SCHOOL_NAME_FALLBACK'])
integrated = integrated.drop(columns=[c for c in ['SCHOOL_NAME_FALLBACK'] if c in integrated.columns])

# Per term, per department aggregation
per_td = (
    integrated
    .groupby(['TERM','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME'], dropna=False)
    .agg(NUMBER_OF_COURSES=('SUBJECT_ID','nunique'))
    .reset_index()
)
# Without an explicit equivalency mapping table, use 1.0 as the consistent proxy
per_td['AVERAGE_EQUIVALENT_SUBJECTS'] = 1.0

# Subtotals per term
subtot = (
    per_td
    .groupby(['TERM'], dropna=False)
    .agg(NUMBER_OF_COURSES=('NUMBER_OF_COURSES','sum'), AVERAGE_EQUIVALENT_SUBJECTS=('AVERAGE_EQUIVALENT_SUBJECTS','mean'))
    .reset_index()
)
subtot['DEPARTMENT_NAME'] = 'SUBTOTAL'
subtot['SCHOOL_NAME'] = ''

# Grand total across all terms
grand = (
    per_td[['NUMBER_OF_COURSES','AVERAGE_EQUIVALENT_SUBJECTS']]
    .agg({'NUMBER_OF_COURSES':'sum', 'AVERAGE_EQUIVALENT_SUBJECTS':'mean'})
)
grand = grand.to_frame().T
grand['TERM'] = 'TOTAL'
grand['DEPARTMENT_NAME'] = 'TOTAL'
grand['SCHOOL_NAME'] = ''

# Detail rows and sorting
detail = per_td[['TERM','DEPARTMENT_NAME','NUMBER_OF_COURSES','AVERAGE_EQUIVALENT_SUBJECTS','SCHOOL_NAME']].copy()
detail = detail.sort_values(['TERM','DEPARTMENT_NAME'], kind='mergesort')

# Combine detail with subtotals and grand total
subtot_detail = subtot[['TERM','DEPARTMENT_NAME','NUMBER_OF_COURSES','AVERAGE_EQUIVALENT_SUBJECTS','SCHOOL_NAME']].copy()
combined = (
    pd.concat([detail, subtot_detail, grand[['TERM','DEPARTMENT_NAME','NUMBER_OF_COURSES','AVERAGE_EQUIVALENT_SUBJECTS','SCHOOL_NAME']]], ignore_index=True)
)
combined = combined.sort_values(['TERM','DEPARTMENT_NAME'], kind='mergesort').reset_index(drop=True)

# Suppress repeated TERM display
terms = combined['TERM'].tolist()
term_display = []
prev = None
for t in terms:
    if t == prev:
        term_display.append('')
    else:
        term_display.append(t)
        prev = t
combined.insert(0, 'TERM_DISPLAY', term_display)

# Department phone number not present in prepared tables; include blank column for schema completeness
combined['DEPARTMENT_PHONE'] = ''

# Final projection and rename
target = combined.rename(columns={'TERM_DISPLAY':'TERM','DEPARTMENT_NAME':'DEPARTMENT'})[['TERM','DEPARTMENT','NUMBER_OF_COURSES','AVERAGE_EQUIVALENT_SUBJECTS','SCHOOL_NAME','DEPARTMENT_PHONE']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

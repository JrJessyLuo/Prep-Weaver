import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'CIP_PROGRAM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'CIP_PROGRAM_CODE', 'new_name': 'CIP_PROGRAM_CODE_STR'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_LEVEL', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_DEGREE_GRANTING', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_DESCRIPTION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_OPTION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CIP_PROGRAM_CODE_STR', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'PROGRAM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'PROGRAM_CODE', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    s = s.strip()\n    # Remove any decimal part while preserving leading zeros\n    if '.' in s:\n        s = s.split('.')[0]\n    # Remove any non-digit characters except leading zeros\n    s = ''.join(ch for ch in s if ch.isdigit())\n    return s"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'PROGRAM_CODE', 'new_name': 'PROGRAM_CODE_STR'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'VERSION', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CATEGORY_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'VERSION', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CATEGORY_CODE', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CATEGORY_TITLE', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'PROGRAM_TITLE', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['PROGRAM_CODE_STR', 'VERSION', 'CATEGORY_CODE', 'CATEGORY_TITLE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['CIP_PROGRAM_CODE'] = tmp_0['CIP_PROGRAM_CODE'].astype(str)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'CIP_PROGRAM_CODE': 'CIP_PROGRAM_CODE_STR'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['COURSE_LEVEL'] = tmp_2['COURSE_LEVEL'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['DEPARTMENT_NAME'] = tmp_3['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['SCHOOL_NAME'] = tmp_4['SCHOOL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['IS_DEGREE_GRANTING'] = tmp_5['IS_DEGREE_GRANTING'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_6['COURSE'] = tmp_6['COURSE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_7['COURSE_DESCRIPTION'] = tmp_7['COURSE_DESCRIPTION'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_8['COURSE_OPTION'] = tmp_8['COURSE_OPTION'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['CIP_PROGRAM_CODE_STR', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['PROGRAM_CODE'] = tmp_0['PROGRAM_CODE'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    s = s.strip()\n    # Remove any decimal part while preserving leading zeros\n    if '.' in s:\n        s = s.split('.')[0]\n    # Remove any non-digit characters except leading zeros\n    s = ''.join(ch for ch in s if ch.isdigit())\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['PROGRAM_CODE'] = tmp_1['PROGRAM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'PROGRAM_CODE': 'PROGRAM_CODE_STR'})
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['VERSION'] = tmp_3['VERSION'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['CATEGORY_CODE'] = tmp_4['CATEGORY_CODE'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['VERSION'] = tmp_5['VERSION'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['CATEGORY_CODE'] = tmp_6['CATEGORY_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_4 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_7['CATEGORY_TITLE'] = tmp_7['CATEGORY_TITLE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_5 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_8['PROGRAM_TITLE'] = tmp_8['PROGRAM_TITLE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['PROGRAM_CODE_STR', 'VERSION', 'CATEGORY_CODE', 'CATEGORY_TITLE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', left_on='CIP_PROGRAM_CODE_STR', right_on='PROGRAM_CODE_STR')
# Compute totals per course level within each CIP category code
lvl_counts = (integrated
    .groupby(['CATEGORY_CODE', 'COURSE_LEVEL'], dropna=False)
    .size()
    .reset_index(name='total_courses_per_level'))
# Pivot course level counts to wide form so each level has its own column
lvl_pivot = lvl_counts.pivot(index='CATEGORY_CODE', columns='COURSE_LEVEL', values='total_courses_per_level').reset_index()
# Ensure pivoted columns exist; fill NaN with 0 and cast to int
lvl_pivot = lvl_pivot.fillna(0)
for c in lvl_pivot.columns:
    if c != 'CATEGORY_CODE':
        lvl_pivot[c] = lvl_pivot[c].astype(int)
# Total number of degree-granting courses per CIP category code (Y only)
deg_counts = (integrated[integrated['IS_DEGREE_GRANTING'].str.upper() == 'Y']
    .groupby('CATEGORY_CODE', as_index=False)
    .size()
    .rename(columns={'size': 'total_degree_granting_courses'}))
# Representative metadata per category: category title, version, department/school names are not uniquely defined per category across all rows,
# so we aggregate by taking the first observed non-null for display while keeping category-level granularity.
meta = (integrated
    .groupby('CATEGORY_CODE', as_index=False)
    .agg({
        'CATEGORY_TITLE': 'first',
        'VERSION': 'first',
        'DEPARTMENT_NAME': 'first',
        'SCHOOL_NAME': 'first'
    }))
# Merge all pieces
ans = meta.merge(lvl_pivot, on='CATEGORY_CODE', how='left').merge(deg_counts, on='CATEGORY_CODE', how='left')
ans['total_degree_granting_courses'] = ans['total_degree_granting_courses'].fillna(0).astype(int)
# Final projection: include category title, version, department name, school name, category code, per-level totals (all present level columns), and degree-granting total
level_cols = [c for c in ans.columns if c not in ['CATEGORY_TITLE','VERSION','DEPARTMENT_NAME','SCHOOL_NAME','CATEGORY_CODE','total_degree_granting_courses']]
ordered_cols = ['CATEGORY_TITLE','VERSION','DEPARTMENT_NAME','SCHOOL_NAME','CATEGORY_CODE'] + level_cols + ['total_degree_granting_courses']
# Ensure deterministic order: sort by CATEGORY_CODE
ans = ans[ordered_cols].sort_values(by='CATEGORY_CODE', kind='mergesort')
target = ans

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}

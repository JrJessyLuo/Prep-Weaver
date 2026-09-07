import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DEPARTMENT', 'new_name': 'DEPARTMENT_CODE'}, {'old_name': 'DEPARTMENT_NAME', 'new_name': 'DEPARTMENT_NAME_SHORT'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COURSE_LEVEL', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_DEGREE_GRANTING', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SCHOOL_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_LEVEL', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME_SHORT', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME_SHORT', 'SCHOOL_NAME', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SCHOOL_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'department_full_name', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'DEPARTMENT': 'DEPARTMENT_CODE', 'DEPARTMENT_NAME': 'DEPARTMENT_NAME_SHORT'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['DEPARTMENT_CODE'] = tmp_1['DEPARTMENT_CODE'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['COURSE_LEVEL'] = tmp_2['COURSE_LEVEL'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['IS_DEGREE_GRANTING'] = tmp_3['IS_DEGREE_GRANTING'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['SCHOOL_NAME'] = tmp_4['SCHOOL_NAME'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['DEPARTMENT_CODE'] = tmp_5['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_6['COURSE_LEVEL'] = tmp_6['COURSE_LEVEL'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_7['SCHOOL_NAME'] = tmp_7['SCHOOL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_8['DEPARTMENT_NAME_SHORT'] = tmp_8['DEPARTMENT_NAME_SHORT'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME_SHORT', 'SCHOOL_NAME', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    tmp_0 = df.loc[:, ['DEPARTMENT_CODE', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME']].copy()
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['DEPARTMENT_CODE'] = tmp_1['DEPARTMENT_CODE'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['SCHOOL_CODE'] = tmp_2['SCHOOL_CODE'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['DEPARTMENT_CODE'] = tmp_3['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['SCHOOL_CODE'] = tmp_4['SCHOOL_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_5['SCHOOL_NAME'] = tmp_5['SCHOOL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_6['department_full_name'] = tmp_6['department_full_name'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['DEPARTMENT_CODE', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='DEPARTMENT_CODE')
# Compute totals per school code, department full name, and course level
integrated['is_deg_numeric'] = integrated['IS_DEGREE_GRANTING'].str.upper().eq('Y').astype(int)
agg = (
    integrated.groupby(['SCHOOL_CODE', 'SCHOOL_NAME_y', 'department_full_name', 'COURSE_LEVEL'], dropna=False)
    .agg(total_courses=('DEPARTMENT_CODE', 'size'), total_degree_granting=('is_deg_numeric', 'sum'))
    .reset_index()
)
# Rename SCHOOL_NAME_y to SCHOOL_NAME for final clarity
agg = agg.rename(columns={'SCHOOL_NAME_y': 'SCHOOL_NAME'})
target = agg[['SCHOOL_CODE', 'SCHOOL_NAME', 'department_full_name', 'COURSE_LEVEL', 'total_courses', 'total_degree_granting']].sort_values(['SCHOOL_CODE', 'department_full_name', 'COURSE_LEVEL'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
